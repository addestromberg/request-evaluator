import typing
import numpy as np
import httpx
import octobot_commons.enums as enums
import octobot_evaluators.evaluators as evaluators
import octobot_evaluators.util as evaluators_util
import octobot_trading.api as trading_api
import tulipy


class RequestEvaluator(evaluators.TAEvaluator):
    HISTORY_LENGTH = "history_length"
    URL = "url"
    TIMEOUT = "timeout"
    BASIC_AUTH = "basic_auth"
    BASIC_AUTH_USERNAME = "auth_username"
    BASIC_AUTH_PASSWORD = "auth_password"
    SCORE_FIELD= "score_field"
    RSI_PERIOD = "rsi_period"
    BB_PERIOD = "bb_period"
    BB_STD = "bb_std"
    MACD_FAST = "macd_fast"
    MACD_SLOW = "macd_slow"
    MACD_SIGNAL = "macd_signal"
    ATR_PERIOD = "atr_period"
    SHORT_MA_PERIOD = "short_ma_period"
    LONG_MA_PERIOD = "long_ma_period"

    def __init__(self, tentacles_setup_config):
        super().__init__(tentacles_setup_config)
        self.history_length = 60
        self.timeout = 5.0
        self.score_field = "score"
        self.rsi_period = 14
        self.bb_period = 20
        self.bb_std = 2
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.atr_period = 5
        self.short_ma_period = 20
        self.long_ma_period = 50

    def init_user_inputs(self, inputs: dict) -> None:
        """
        Called right before starting the evaluator, should define all the evaluator's user inputs
        """
        default_config = self.get_default_config()
        self.period_length = self.UI.user_input(
            self.HISTORY_LENGTH,
            enums.UserInputTypes.INT,
            default_config["history_length"],
            inputs,
            min_val=1,
            title="History Length",
        )
        self.url = self.UI.user_input(
            self.URL, enums.UserInputTypes.TEXT, default_config["url"], inputs, title="Request URL"
        )

        self.is_basic_auth = self.UI.user_input(
            self.BASIC_AUTH,
            enums.UserInputTypes.BOOLEAN,
            default_config["basic_auth"],
            inputs,
            title="Use Basic Auth",
        )

        self.username = self.UI.user_input(
            self.BASIC_AUTH_USERNAME,
            enums.UserInputTypes.TEXT,
            default_config["auth_username"],
            inputs,
            show_in_summary=False,
            show_in_optimizer=False,
            title="Username",
        )
        self.password = self.UI.user_input(
            self.BASIC_AUTH_PASSWORD,
            enums.UserInputTypes.TEXT,
            default_config["auth_password"],
            inputs,
            show_in_summary=False,
            show_in_optimizer=False,
            title="Password",
        )

        self.timeout = self.UI.user_input(
            self.TIMEOUT,
            enums.UserInputTypes.FLOAT,
            default_config["timeout"],
            inputs,
            min_val=1,
            max_val=120,
            title="Request Timeout",
        )

        self.rsi_period = self.UI.user_input(
            self.RSI_PERIOD,
            enums.UserInputTypes.INT,
            default_config["rsi_period"],
            inputs,
            min_val=1,
            max_val=100,
            title="Stochastic RSI Period",
        )

        self.bb_period = self.UI.user_input(
            self.BB_PERIOD,
            enums.UserInputTypes.INT,
            default_config["bb_period"],
            inputs,
            min_val=1,
            max_val=100,
            title="Bollinger Band Period",
        )

        self.bb_std = self.UI.user_input(
            self.BB_STD,
            enums.UserInputTypes.INT,
            default_config["bb_std"],
            inputs,
            min_val=0,
            max_val=100,
            title="Bollinger Band Multiplier",
        )

        self.score_field = self.UI.user_input(
            self.SCORE_FIELD,
            enums.UserInputTypes.TEXT,
            default_config["score_field"],
            inputs,
            show_in_summary=False,
            show_in_optimizer=False,
            title="Score Field",
        )

        self.macd_fast = self.UI.user_input(
            self.MACD_FAST,
            enums.UserInputTypes.INT,
            default_config["macd_fast"],
            inputs,
            min_val=0,
            max_val=100,
            title="MACD Fast",
        )
        self.macd_slow = self.UI.user_input(
            self.MACD_SLOW,
            enums.UserInputTypes.INT,
            default_config["macd_slow"],
            inputs,
            min_val=0,
            max_val=100,
            title="MACD Slow",
        )

        self.macd_signal = self.UI.user_input(
            self.MACD_SIGNAL,
            enums.UserInputTypes.INT,
            default_config["macd_signal"],
            inputs,
            min_val=0,
            max_val=100,
            title="MACD Signal",
        )

        self.atr_period = self.UI.user_input(
            self.ATR_PERIOD,
            enums.UserInputTypes.INT,
            default_config["atr_period"],
            inputs,
            min_val=0,
            max_val=100,
            title="ATR Period",
        )
        self.short_ma_period = self.UI.user_input(
            self.SHORT_MA_PERIOD,
            enums.UserInputTypes.INT,
            default_config["short_ma_period"],
            inputs,
            min_val=0,
            max_val=100,
            title="Short MA Period",
        )
        self.long_ma_period = self.UI.user_input(
            self.LONG_MA_PERIOD,
            enums.UserInputTypes.INT,
            default_config["long_ma_period"],
            inputs,
            min_val=0,
            max_val=100,
            title="Long MA Period",
        )

    @classmethod
    def get_default_config(
        cls,
        history_length: typing.Optional[float] = None,
        url: typing.Optional[str] = None,
        basic_auth: bool = False,
        username: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        timeout: float = 2.0,
        rsi_period: int = 14,
        bb_period: int = 20,
        bb_std: int = 2,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
        atr_period: int = 5,
        short_ma_period: int = 20,
        long_ma_period: int = 50,
        score_field: str = "score"
    ):
        return {
            cls.HISTORY_LENGTH: history_length or 2,
            cls.URL: url or "https://",
            cls.BASIC_AUTH: basic_auth or False,
            cls.BASIC_AUTH_USERNAME: username or "",
            cls.BASIC_AUTH_PASSWORD: password or "",
            cls.TIMEOUT:timeout or 2.0,
            cls.RSI_PERIOD:rsi_period or 14,
            cls.BB_PERIOD:bb_period or 20,
            cls.BB_STD:bb_std or 2,
            cls.MACD_FAST:macd_fast or 12,
            cls.MACD_SLOW:macd_slow or 26,
            cls.MACD_SIGNAL:macd_signal or 9,
            cls.ATR_PERIOD:atr_period or 5,
            cls.SHORT_MA_PERIOD:short_ma_period or 20,
            cls.LONG_MA_PERIOD:long_ma_period or 50,
            cls.SCORE_FIELD:score_field or "score"
        }

    async def ohlcv_callback(
        self,
        exchange: str,
        exchange_id: str,
        cryptocurrency: str,
        symbol: str,
        time_frame,
        candle,
        inc_in_construction_data,
    ):
        
        # We want to pass all the data.
        timestamp = trading_api.get_symbol_time_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )

        open = trading_api.get_symbol_open_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )
        high = trading_api.get_symbol_high_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )
        low = trading_api.get_symbol_low_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )
        close = trading_api.get_symbol_close_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )
        volume = trading_api.get_symbol_volume_candles(
            self.get_exchange_symbol_data(exchange, exchange_id, symbol),
            time_frame,
            limit=self.history_length,
            include_in_construction=inc_in_construction_data,
        )

        candle_data = {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume}

        await self.evaluate(cryptocurrency, symbol, time_frame, candle_data, candle)

    async def evaluate(self, cryptocurrency, symbol, time_frame, candle_data, candle):
        """Send request to external API and await response."""
        # Check the timeout value
        if isinstance(self.timeout, float):
            to = self.timeout
        else:
            to = 5.0

        if self.is_basic_auth:
            client = httpx.AsyncClient(timeout=to, auth=httpx.BasicAuth(str(self.username), str(self.password)))
        else:
            client = httpx.AsyncClient(timeout=to)

        # Pass selected indicators
        rsi = tulipy.stochrsi(real=candle_data.get("close"), period=self.rsi_period)
        bbands_lower, bbands_middle, bbands_upper = tulipy.bbands(real=candle_data.get("close"),period=self.bb_period, stddev=self.bb_std)
        macd, signal, hist = tulipy.macd(real=candle_data.get("close"), short_period=self.macd_fast, long_period=self.macd_slow, signal_period=self.macd_signal)
        atr = tulipy.atr(high=candle_data.get("high"), low=candle_data.get("low"), close=candle_data.get("close"), period=self.atr_period)
        short_ma = tulipy.sma(real=candle_data.get("close"), period=self.short_ma_period)
        long_ma = tulipy.sma(real=candle_data.get("close"), period=self.long_ma_period)

        payload = {
            "symbol": symbol,
            "time_frame": time_frame,
            "last_candle": candle,
            "history": candle_data,
            "stochastic_rsi": rsi,
            "bollinger_band": {"upper": bbands_upper, "middle": bbands_middle, "lower": bbands_lower},
            "macd": {"macd": macd, "signal": signal, "hist": hist},
            "atr": atr,
            "moving_avg": {f"ma_{self.short_ma_period}": short_ma, f"ma_{self.long_ma_period}": long_ma}
        }

        try:
            response = await client.post(str(self.url), json=serialize_payload(payload))
            response.raise_for_status()
            score = float(response.json().get(self.score_field, 0))
            self.eval_note = max(-1.0, min(score, 1.0))

        except Exception as e:
            self.logger.error(str(e))
            self.eval_note = 0

        await self.evaluation_completed(
            cryptocurrency,
            symbol,
            time_frame,
            eval_time=evaluators_util.get_eval_time(full_candle=candle, time_frame=time_frame),
        )


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
