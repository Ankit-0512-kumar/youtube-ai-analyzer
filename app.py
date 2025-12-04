import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="YT Pulse AI", page_icon="🧠", layout="wide")

# --- 2. LOAD CSS ---
def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

local_css("style.css")

# --- 3. LOAD AI MODEL (CACHED) ---
@st.cache_resource
def load_model():
    # Using RoBERTa model trained on Tweets (similar to YT comments)
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    return tokenizer, model

# Download/Load Model
with st.spinner("🧠 Waking up the AI Brain... (First load takes 30s)"):
    tokenizer, model = load_model()

# --- 4. HELPER FUNCTIONS ---
def get_video_id(url):
    if "v=" in url: return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url: return url.split("/")[-1]
    return None

def get_comments(video_id, api_key, target_limit):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        all_comments = []
        next_page_token = None
        
        # Progress Bar Setup
        progress_text = "Fetching comments from YouTube..."
        my_bar = st.progress(0, text=progress_text)
        
        while len(all_comments) < target_limit:
            request = youtube.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=100, 
                textFormat="plainText", pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                c = item['snippet']['topLevelComment']['snippet']
                all_comments.append([c['authorDisplayName'], c['textDisplay']])
                if len(all_comments) >= target_limit: break
            
            # Update Progress Bar
            current = len(all_comments)
            my_bar.progress(min(current / target_limit, 1.0), text=f"Fetched {current} / {target_limit} comments...")
            
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
                time.sleep(0.1) # Safety delay
            else:
                break 
                
        my_bar.empty() # Remove bar when done
        return pd.DataFrame(all_comments, columns=['Author', 'Comment'])
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def analyze_with_roberta(df):
    res = []
    total = len(df)
    
    # Progress Bar for AI Analysis
    bar = st.progress(0, text="AI is reading & understanding comments...")
    
    for i, text in enumerate(df['Comment']):
        try:
            text = str(text)
            # 1. Tokenize
            encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            # 2. Predict
            output = model(**encoded_input)
            scores = output.logits[0].detach().numpy()
            # 3. Softmax
            scores = softmax(scores)
            
            # RoBERTa Labels: 0=Negative, 1=Neutral, 2=Positive
            neg, neu, pos = scores[0], scores[1], scores[2]
            
            if pos > neg and pos > neu:
                label = "Positive"
                final_score = pos
            elif neg > pos and neg > neu:
                label = "Negative"
                final_score = -neg # Negative score for visualization
            else:
                label = "Neutral"
                final_score = 0.0
                
            res.append({'Score': final_score, 'Sentiment': label})
        except:
            res.append({'Score': 0, 'Sentiment': "Neutral"})
            
        # Update Progress every 10 comments
        if i % 5 == 0:
            bar.progress(min((i+1)/total, 1.0), text=f"Analyzing {i+1}/{total}...")
            
    bar.empty()
    return pd.concat([df, pd.DataFrame(res)], axis=1)

def highlight_sentiment(val):
    color = 'white'
    weight = 'normal'
    if val == 'Positive': color = '#00FF9D'; weight = 'bold'
    elif val == 'Negative': color = '#FF4B4B'; weight = 'bold'
    elif val == 'Neutral': color = '#AAAAAA'
    return f'color: {color}; font-weight: {weight}'

# --- 5. SIDEBAR (AUTO KEY DETECTION) ---
with st.sidebar:
    st.header("🔐 Settings")
    
    # Check if key exists in Streamlit Secrets
    if 'YOUTUBE_API_KEY' in st.secrets:
        st.success("✅ API Key Loaded from Server")
        api_key = st.secrets['YOUTUBE_API_KEY']
    else:
        api_key = st.text_input("Paste Google API Key", type="password")
        st.caption("Enter key manually if not configured on server.")

    st.markdown("---")
    st.header("📊 AI Depth")
    limit = st.slider("Comment Limit:", 20, 200, 50, step=10)
    st.caption(f"Analyzing {limit} comments using Deep Learning.")

# --- 6. MAIN UI ---
st.markdown("<h1 style='text-align: center; color: white;'>🧠 YouTube Pulse AI (RoBERTa)</h1>", unsafe_allow_html=True)
st.write("") 

col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("Paste YouTube Video Link Here:", placeholder="https://...")
with col2:
    st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)
    btn = st.button("ANALYZE 🚀", use_container_width=True)

# --- 7. EXECUTION LOGIC ---
if btn:
    if not api_key:
        st.error("⚠️ API Key not found. Please add it in Settings or Secrets.")
    elif not url:
        st.warning("⚠️ Please enter a YouTube URL.")
    else:
        vid_id = get_video_id(url)
        if vid_id:
            df = get_comments(vid_id, api_key, target_limit=limit)
            if df is not None and not df.empty:
                
                # Run AI Analysis
                df_new = analyze_with_roberta(df)
                
                # --- METRICS ---
                st.markdown("### 📊 Analysis Results")
                m1, m2, m3, m4 = st.columns(4)
                total = len(df_new)
                pos = len(df_new[df_new['Sentiment']=='Positive'])
                neg = len(df_new[df_new['Sentiment']=='Negative'])
                
                m1.metric("Total", total)
                m2.metric("Positive", pos, f"{(pos/total)*100:.0f}%")
                m3.metric("Negative", neg, f"-{(neg/total)*100:.0f}%", delta_color="inverse")
                avg_score = df_new['Score'].mean()
                mood = "😐 Neutral"
                if avg_score > 0.1: mood = "😁 Happy"
                elif avg_score < -0.1: mood = "😡 Angry"
                m4.metric("Overall Mood", mood)
                
                st.markdown("---")

                # --- CHARTS ---
                c1, c2 = st.columns(2)
                with c1:
                    fig = px.pie(df_new, names='Sentiment', hole=0.5,
                                 color='Sentiment',
                                 color_discrete_map={'Positive':'#00FF9D', 'Negative':'#FF4B4B', 'Neutral':'#888888'})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    fig2 = px.histogram(df_new, x="Score", nbins=20, color_discrete_sequence=['#00D4FF'])
                    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig2, use_container_width=True)
                    
                # --- TABLE ---
                st.markdown("### 📝 Detailed Insights")
                display_df = df_new[['Sentiment', 'Score', 'Comment', 'Author']]
                styled_df = display_df.style.map(highlight_sentiment, subset=['Sentiment']) \
                                            .format("{:.4f}", subset=['Score'])

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=500,
                    column_config={
                        "Sentiment": st.column_config.TextColumn("Sentiment", width="medium"),
                        "Score": st.column_config.NumberColumn("Confidence", format="%.4f", width="small"),
                        "Comment": st.column_config.TextColumn("Comment Text", width="large"),
                    },
                    hide_index=True
                )
            else:
                st.warning("No comments found or API limit reached.")
        else:
            st.error("Invalid YouTube URL.")
