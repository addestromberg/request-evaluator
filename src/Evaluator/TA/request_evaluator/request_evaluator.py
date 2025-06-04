
import typing
import numpy as np
import httpx
import octobot_commons.enums as enums
import octobot_evaluators.evaluators as evaluators
import octobot_evaluators.util as evaluators_util
import octobot_trading.api as trading_api

class RequestEvaluator(evaluators.TAEvaluator):

    HISTORY_LENGTH = "history_length"
    URL = "url"

    def __init__(self, tentacles_setup_config):
        super().__init__(tentacles_setup_config)
        self.history_length = 30

        self._client = httpx.AsyncClient(timeout=5.0)


    def init_user_inputs(self, inputs: dict) -> None:
        """
        Called right before starting the evaluator, should define all the evaluator's user inputs
        """
        default_config = self.get_default_config()
        self.period_length = self.UI.user_input(
            self.HISTORY_LENGTH, enums.UserInputTypes.INT, default_config["history_length"],
            inputs, min_val=1, title="History Length"
        )
        self.url = self.UI.user_input(
            self.URL, enums.UserInputTypes.TEXT, default_config["url"],
            inputs, title="Request URL"
        )

    @classmethod
    def get_default_config(
        cls, 
        history_length: typing.Optional[float] = None,
        url: typing.Optional[str] = None
    ):
        return {
            cls.HISTORY_LENGTH: history_length or 2,
            cls.URL: url or 2,
        }

    async def ohlcv_callback(self, exchange: str, exchange_id: str,
                             cryptocurrency: str, symbol: str, time_frame, candle, inc_in_construction_data):
        candle_data = trading_api.get_symbol_close_candles(self.get_exchange_symbol_data(exchange, exchange_id, symbol),
                                                           time_frame,
                                                           limit=self.history_length,
                                                           include_in_construction=inc_in_construction_data)
        await self.evaluate(cryptocurrency, symbol, time_frame, candle_data, candle)

    async def evaluate(self, cryptocurrency, symbol, time_frame, candle_data, candle):
        """ Send request to external API and await response. """

        payload = {
            "symbol": self.symbol,
            "time_frame": time_frame,
            "candle": candle,
            "candle_data": candle_data,
        }
        try:
            response = await self._client.post(str(self.url), json=serialize_payload(payload))
            response.raise_for_status()
            score = float(response.json().get("score", 0))
            self.eval_note = max(-1.0, min(score, 1.0))

        except Exception as e:
            self.logger.exception(e)
            self.eval_note = 0


        await self.evaluation_completed(cryptocurrency, symbol, time_frame, eval_time=evaluators_util.get_eval_time(full_candle=candle, time_frame=time_frame) )
        
def serialize_payload(obj: dict) -> dict:
    """
    Recursively serializes a dictionary object to ensure all values are JSON serializable.
    Handles conversion of numpy arrays to lists and processes nested dictionaries and lists.
    Args:
        obj (dict): The dictionary object to serialize.
    Returns:
        dict: A dictionary with all values converted to JSON serializable formats.
    Example:
        >>> import numpy as np
        >>> data = {'array': np.array([1, 2, 3]), 'nested': {'value': np.array([4, 5])}}
        >>> serialize_payload(data)
        {'array': [1, 2, 3], 'nested': {'value': [4, 5]}}
    """

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: serialize_payload(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_payload(v) for v in obj]
    else:
        return obj