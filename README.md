# 📈 EquiSense: AI Market Sentiment Analyzer

**Live Demo:** https://equisense.streamlit.app/

## 📌 Overview
EquiSense is an end-to-end Machine Learning web dashboard designed to bridge the gap between quantitative price action and qualitative market sentiment. By leveraging a specialized NLP Transformer model, the application reads live financial news and provides instant sentiment analysis (Positive/Negative/Neutral) alongside interactive historical price charts.

## ⚙️ Architecture & Tech Stack
* **Data Engine:** `yfinance` API for real-time OHLC price tracking and live news extraction.
* **NLP Brain:** Hugging Face `Transformers` running **FinBERT** (`ProsusAI/finbert`), a BERT model fine-tuned specifically on financial text and analyst reports.
* **Data Visualization:** `Plotly` for interactive, dynamic candlestick charting.
* **Deployment:** `Streamlit` Community Cloud for seamless web hosting and UI rendering.

## 🚀 Key Features
* **Live Sentiment Scoring:** Automatically extracts text from raw Yahoo Finance news JSONs and passes it through the Transformer model to generate confidence-weighted market sentiment.
* **Defensive Data Handling:** Engineered to safely handle dynamic and nested JSON structures from live API endpoints without breaking the pipeline.
* **Interactive Analytics:** Side-by-side comparison of 6-month historical price trends against today's breaking news.

## 💻 How to Run Locally
1. Clone the repository:
   ```Bash
   git clone [https://github.com/anshksonker04/EquiSense.git](https://github.com/anshksonker04/EquiSense.git)
   

2. Install the required dependencies:
    Bash
    ```
    pip install -r requirements.txt
    ```

3. Launch the Streamlit application:
    Bash
    ```
    streamlit run app.py
    ```

