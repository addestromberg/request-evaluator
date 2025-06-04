# RequestEvaluator Tentacle

The `RequestEvaluator` is a custom OctoBot evaluator that performs off-platform evaluations by sending indicator data to an external webhook (e.g. an n8n workflow). The webhook processes the data and returns a score between `-1` (strong sell) and `1` (strong buy), which is used to influence trading decisions.

---

## 🔧 How It Works

1. OctoBot collects indicator values (e.g. RSI, MACD, etc.).
2. `RequestEvaluator` sends a POST request to your configured webhook URL with the indicator data.
3. The external service returns a JSON payload with a `score` key.
4. The score is clamped to the range `[-1, 1]` and used as the evaluator's result.