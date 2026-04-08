import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from transformers import pipeline

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Financial Analyzer", page_icon="📈", layout="wide")
st.title("📈 EquiSense-The Real Time Market Analyzer")
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
        st.subheader("Interactive Price Analysis")
        with st.spinner("Calculating indicators..."):
            hist_data = stock.history(period="6mo")
            
            if not hist_data.empty:
                # --- CALCULATION ENGINE ---
                # 20-Day Moving Average
                hist_data['SMA20'] = hist_data['Close'].rolling(window=20).mean()
                
                # RSI Calculation (Standard 14-day)
                delta = hist_data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                hist_data['RSI'] = 100 - (100 / (1 + rs))

                # --- PLOTTING ENGINE ---
                fig = go.Figure()

                # 1. Add the Candlesticks
                fig.add_trace(go.Candlestick(
                    x=hist_data.index,
                    open=hist_data['Open'], high=hist_data['High'],
                    low=hist_data['Low'], close=hist_data['Close'],
                    name="Market Price"
                ))

                # 2. Add the SMA Line (The Trend)
                fig.add_trace(go.Scatter(
                    x=hist_data.index, y=hist_data['SMA20'],
                    line=dict(color='gold', width=1.5),
                    name="20-Day Trend (SMA)"
                ))

                fig.update_layout(
                    height=600,
                    template="plotly_dark",
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=0, r=0, t=30, b=0)
                )

                st.plotly_chart(fig, width="stretch")
                
                # 3. Display RSI Gauge
                latest_rsi = hist_data['RSI'].iloc[-1]
                st.write(f"**Current Momentum (RSI):** {latest_rsi:.2f}")
                if latest_rsi > 70:
                    st.warning("⚠️ Overbought (Market might be too hyped)")
                elif latest_rsi < 30:
                    st.success("✅ Oversold (Potential buying opportunity)")
                else:
                    st.info("⚖️ Neutral Momentum")

    with col2:
        st.subheader("Live AI News Sentiment")
        with st.spinner("Reading the news..."):
            live_news = stock.news
            
            if not live_news:
                st.warning("No recent news found on Yahoo Finance.")
                bullish_percent = 50 # Default to neutral if no news
            else:
                real_headlines = []
                for article in live_news:
                    if 'title' in article:
                        real_headlines.append(article['title'])
                    elif 'content' in article and 'title' in article['content']:
                        real_headlines.append(article['content']['title'])
                
                # --- NEW AGGREGATION LOGIC ---
                pos_count = 0
                neg_count = 0

                for headline in real_headlines[:30]:
                    result = sentiment_analyzer(headline)[0]
                    # Note: FinBERT sometimes returns lowercase labels, so we use .lower() just to be safe
                    label = result['label'].lower() 
                    
                    if label == 'positive':
                        pos_count += 1
                    elif label == 'negative':
                        neg_count += 1

                total = pos_count + neg_count
                if total > 0:
                    bullish_percent = (pos_count / total) * 100
                    # st.metric makes a large, beautiful dashboard number!
                    st.metric(label="Bullish Sentiment Score", value=f"{bullish_percent:.1f}%")
                    st.write(f"*Analyzed {total} recent financial articles.*")
                else:
                    bullish_percent = 50
                    st.info("Mostly neutral news recently.")
        
    # --- THE FINAL VERDICT (AI + MATH) ---
    st.divider()
    st.subheader("🤖 EquiSense Final Verdict")

    # 1. Score the Technicals (Math)
    if latest_rsi < 45:
        tech_state = "Oversold (Cheap)"
        tech_score = 1
    elif latest_rsi > 55:
        tech_state = "Overbought (Expensive)"
        tech_score = -1
    else:
        tech_state = "Neutral"
        tech_score = 0
    
    # 2. Score the Sentiment (AI)
    if bullish_percent >= 60:
        ai_state = "Bullish"
        ai_score = 1
    elif bullish_percent <= 40:
        ai_state = "Bearish"
        ai_score = -1
    else:
        ai_state = "Mixed/Neutral"
        ai_score = 0

    # 3. Calculate Final Convergence
    final_score = tech_score + ai_score

    # 4. Display the nuanced result
    if final_score >= 2:
        st.success(f"🚀 **STRONG BUY:** AI is {ai_state} AND Chart is {tech_state}.")
    elif final_score == 1:
        st.success(f"📈 **LEAN BUY:** At least one indicator is positive (Chart: {tech_state} | AI: {ai_state}).")
    elif final_score <= -2:
        st.error(f"📉 **STRONG SELL:** AI is {ai_state} AND Chart is {tech_state}.")
    elif final_score == -1:
        st.error(f"⚠️ **LEAN SELL:** At least one indicator is negative (Chart: {tech_state} | AI: {ai_state}).")
    else:
        st.warning(f"⚖️ **NEUTRAL:** Both indicators are flat (Chart: {tech_state} | AI: {ai_state}).")