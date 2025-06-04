# Request Evaluator Tentacle

The **Request Evaluator** is a custom OctoBot tentacle that allows your bot to make dynamic trading decisions based on real-time responses from an external evaluation service.

Instead of calculating trading signals internally, this evaluator sends current indicator values (like RSI, MACD, and price) to a remote webhook endpoint — which may run AI models, statistical rules, or other logic — and receives a score between `-1` and `1` in return.

---

## 🧠 Purpose

This tentacle enables:
- Integration with **external decision engines** like n8n, FastAPI, Flask, or cloud-based AI services.
- Centralized or collaborative decision logic shared across multiple OctoBots.
- Real-time signal scoring beyond static TA rules.

---

## 🚀 How It Works

1. OctoBot gathers market indicator data.
2. The Request Evaluator sends this data to your **webhook endpoint**.
3. Your endpoint processes the data and returns a `score`.
4. The score is used by OctoBot to inform buy/sell/hold decisions.

---

## 🧩 Example Use Cases

- Offload trading logic to an AI model or ML pipeline
- Use centralized logic shared across multiple trading bots
- Integrate with your business logic via services like **n8n**, **Zapier**, or **LangChain**

---

## 🗂️ Installation

1. Download the latest `.zip` release of this tentacle.
2. Open the **OctoBot UI**.
3. Navigate to `Tentacles > Install` and upload the `.zip` file.
4. Done!