import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from transformers import pipeline

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Financial Analyzer", page_icon="📈", layout="wide")
st.title("📈 Live Stock Sentiment & Price Analyzer")
st.write("Select an asset to view its recent price action and analyze today's news using an NLP Transformer.")

# --- LOAD AI BRAIN ---
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

sentiment_analyzer = load_model()

# --- USER INTERFACE ---
popular_tickers = [
    "AAPL - Apple Inc.", "MSFT - Microsoft Corp.", "NVDA - NVIDIA Corp.", 
    "GOOGL - Alphabet (Google)", "AMZN - Amazon.com", "TSLA - Tesla Inc.", 
    "META - Meta Platforms", "JPM - JPMorgan Chase", "WMT - Walmart Inc.",
    "DIS - The Walt Disney Co.", "NFLX - Netflix Inc.", "RELIANCE.NS - Reliance Industries", 
    "TCS.NS - Tata Consultancy Services", "INFY.NS - Infosys Limited", "BTC-USD - Bitcoin"
]

selected_option = st.selectbox("Select a Stock or Asset to Analyze:", popular_tickers)
ticker = selected_option.split(" - ")[0]

if st.button(f"Analyze {ticker}"):
    
    # We use Streamlit columns to put the chart on the left and news on the right
    col1, col2 = st.columns([2, 1]) 
    
    stock = yf.Ticker(ticker)
    
    with col1:
        st.subheader("Interactive Price Chart (Last 6 Months)")
        with st.spinner("Loading chart data..."):
            # Fetch historical data for the chart
            hist_data = stock.history(period="6mo")
            
            if not hist_data.empty:
                # Create a professional Candlestick chart using Plotly
                fig = go.Figure(data=[go.Candlestick(
                    x=hist_data.index,
                    open=hist_data['Open'],
                    high=hist_data['High'],
                    low=hist_data['Low'],
                    close=hist_data['Close'],
                    name="Price"
                )])
                
                # Make the chart look clean and dark-mode friendly
                fig.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=500,
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig, width="stretch")
            else:
                st.error("Could not fetch price data for this ticker.")

    with col2:
        st.subheader("Live AI News Sentiment")
        with st.spinner("Reading the news..."):
            live_news = stock.news
            
            if not live_news:
                st.warning("No recent news found on Yahoo Finance.")
            else:
                real_headlines = []
                for article in live_news:
                    if 'title' in article:
                        real_headlines.append(article['title'])
                    elif 'content' in article and 'title' in article['content']:
                        real_headlines.append(article['content']['title'])
                
                for headline in real_headlines[:5]:
                    result = sentiment_analyzer(headline)[0]
                    label = result['label'].upper()
                    confidence = result['score'] * 100
                    
                    if label == "POSITIVE":
                        st.success(f"**{label}** ({confidence:.1f}%)  \n*{headline}*")
                    elif label == "NEGATIVE":
                        st.error(f"**{label}** ({confidence:.1f}%)  \n*{headline}*")
                    else:
                        st.info(f"**{label}** ({confidence:.1f}%)  \n*{headline}*")