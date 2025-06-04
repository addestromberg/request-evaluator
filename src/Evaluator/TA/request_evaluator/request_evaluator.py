
import typing

import octobot_commons.enums as enums
import octobot_evaluators.evaluators as evaluators
import octobot_trading.api as trading_api

class RequestEvaluator(evaluators.TAEvaluator):

    HISTORY_LENGTH = "history_length"
    URL = "url"

    def __init__(self, tentacles_setup_config):
        super().__init__(tentacles_setup_config)
        self.history_length = 30


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
        
        pass
        # updated_value = False
        # if candle_data is not None and len(candle_data) > self.period_length: # type: ignore
        #     rsi_v = tulipy.rsi(candle_data, period=self.period_length)
        #     if len(rsi_v) and not math.isnan(rsi_v[-1]):
        #         is condition:
        #             self.set_eval_note((rsi_v[-1] - 100) / 200)
        #         else:
        #             self.eval_note = 0
        #             if rsi_v[-1] >= self.short_threshold:
        #                 self.eval_note = 1
        #             elif rsi_v[-1] <= self.long_threshold:
        #                 self.eval_note = -1
        #         updated_value = True
        # else:
        #     self.eval_note = 0
        # await self.evaluation_completed(cryptocurrency, symbol, time_frame,
        #                                 eval_time=evaluators_util.get_eval_time(full_candle=candle,
        #                                                                         time_frame=time_frame))