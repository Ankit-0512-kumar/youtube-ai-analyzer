# # import streamlit as st
# # from googleapiclient.discovery import build
# # import pandas as pd
# # import plotly.express as px
# # import nltk
# # from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # # --- Config ---
# # st.set_page_config(page_title="YT Pulse", page_icon="⚡", layout="wide")
# # nltk.download('vader_lexicon', quiet=True)
# # sia = SentimentIntensityAnalyzer()

# # # --- Load CSS ---
# # def local_css(file_name):
# #     with open(file_name) as f:
# #         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # local_css("style.css")

# # # --- Helpers ---
# # def get_video_id(url):
# #     if "v=" in url: return url.split("v=")[1].split("&")[0]
# #     elif "youtu.be" in url: return url.split("/")[-1]
# #     return None

# # def get_comments(video_id, api_key):
# #     try:
# #         youtube = build('youtube', 'v3', developerKey=api_key)
# #         req = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=50, textFormat="plainText")
# #         res = req.execute()
# #         data = []
# #         for item in res['items']:
# #             c = item['snippet']['topLevelComment']['snippet']
# #             data.append([c['authorDisplayName'], c['textDisplay']])
# #         return pd.DataFrame(data, columns=['Author', 'Comment'])
# #     except: return None

# # def analyze(df):
# #     res = []
# #     for c in df['Comment']:
# #         score = sia.polarity_scores(c)['compound']
# #         if score > 0.05: label = "Positive"
# #         elif score < -0.05: label = "Negative"
# #         else: label = "Neutral"
# #         res.append({'Score': score, 'Sentiment': label})
# #     return pd.concat([df, pd.DataFrame(res)], axis=1)

# # # --- UI START ---

# # # Title Section
# # st.markdown("<h1 style='text-align: center; color: white;'>⚡ YouTube Pulse Analyzer</h1>", unsafe_allow_html=True)
# # st.markdown("<p style='text-align: center; color: #888;'>Copy a link, paste it below, and see the magic.</p>", unsafe_allow_html=True)

# # st.write("") # Gap

# # # Sidebar
# # with st.sidebar:
# #     st.header("🔐 Settings")
# #     api_key = st.text_input("Paste Google API Key", type="password", help="Required to fetch data")
# #     st.markdown("---")
# #     st.info("Tip: Dark mode is ON by default.")

# # # Main Input
# # col1, col2 = st.columns([4, 1])
# # with col1:
# #     # Label ab dikhega taaki pata chale box kahan hai
# #     url = st.text_input("Paste YouTube Video Link Here:", placeholder="https://www.youtube.com/watch?v=...")
# # with col2:
# #     st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True) # Alignment fix
# #     btn = st.button("ANALYZE 🚀", use_container_width=True)

# # # Processing
# # if btn:
# #     if not api_key:
# #         st.error("⚠️ Please enter your API Key in the Sidebar first!")
# #     elif not url:
# #         st.warning("⚠️ Video Link cannot be empty.")
# #     else:
# #         vid_id = get_video_id(url)
# #         if vid_id:
# #             with st.spinner("🔄 Analyzing Comments..."):
# #                 df = get_comments(vid_id, api_key)
# #                 if df is not None:
# #                     df_new = analyze(df)
                    
# #                     # Metrics Section
# #                     st.markdown("### 📊 Result Overview")
# #                     m1, m2, m3, m4 = st.columns(4)
                    
# #                     total = len(df_new)
# #                     pos = len(df_new[df_new['Sentiment']=='Positive'])
# #                     neg = len(df_new[df_new['Sentiment']=='Negative'])
                    
# #                     # Metrics ab bright white honge CSS ki wajah se
# #                     m1.metric("Total Comments", total)
# #                     m2.metric("Positive", pos, f"{(pos/total)*100:.0f}%")
# #                     m3.metric("Negative", neg, f"-{(neg/total)*100:.0f}%", delta_color="inverse")
                    
# #                     avg = df_new['Score'].mean()
# #                     mood = "😐 Neutral"
# #                     if avg > 0.1: mood = "😁 Happy"
# #                     if avg < -0.1: mood = "😡 Angry"
# #                     m4.metric("Overall Mood", mood)
                    
# #                     st.markdown("---")
                    
# #                     # Charts
# #                     c1, c2 = st.columns(2)
# #                     with c1:
# #                         st.subheader("Sentiment Mix")
# #                         fig = px.pie(df_new, names='Sentiment', hole=0.5,
# #                                      color='Sentiment',
# #                                      color_discrete_map={'Positive':'#00FF9D', 'Negative':'#FF4B4B', 'Neutral':'#888888'})
# #                         # Transparent background fix
# #                         fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
# #                                           font=dict(color="white"), showlegend=True)
# #                         st.plotly_chart(fig, use_container_width=True)
                        
# #                     with c2:
# #                         st.subheader("Intensity Level")
# #                         fig2 = px.histogram(df_new, x="Score", nbins=20, color_discrete_sequence=['#00D4FF'])
# #                         fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
# #                                            font=dict(color="white"), xaxis_title="Sentiment Score", yaxis_title="Count")
# #                         st.plotly_chart(fig2, use_container_width=True)
                        
# #                     # Comments Feed
# #                     st.markdown("### 💬 Latest Comments")
# #                     for i, row in df_new.head(10).iterrows():
# #                         st.markdown(f"""
# #                         <div class="comment-card {row['Sentiment'].lower()}">
# #                             <div class="author-name">{row['Author']}</div>
# #                             <div class="comment-text">{row['Comment']}</div>
# #                         </div>
# #                         """, unsafe_allow_html=True)
                        
# #                 else:
# #                     st.error("Error: Check API Key or Video URL.")
# #         else:
# #             st.error("Invalid YouTube URL.")


# import streamlit as st
# from googleapiclient.discovery import build
# import pandas as pd
# import plotly.express as px
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # --- Config ---
# st.set_page_config(page_title="YT Pulse", page_icon="⚡", layout="wide")
# nltk.download('vader_lexicon', quiet=True)
# sia = SentimentIntensityAnalyzer()

# # --- Load CSS ---
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("style.css")

# # --- Helpers ---
# def get_video_id(url):
#     if "v=" in url: return url.split("v=")[1].split("&")[0]
#     elif "youtu.be" in url: return url.split("/")[-1]
#     return None

# def get_comments(video_id, api_key):
#     try:
#         youtube = build('youtube', 'v3', developerKey=api_key)
#         req = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=500, textFormat="plainText")
#         res = req.execute()
#         data = []
#         for item in res['items']:
#             c = item['snippet']['topLevelComment']['snippet']
#             data.append([c['authorDisplayName'], c['textDisplay']])
#         return pd.DataFrame(data, columns=['Author', 'Comment'])
#     except: return None

# def analyze(df):
#     res = []
#     for c in df['Comment']:
#         score = sia.polarity_scores(c)['compound']
#         if score > 0.05: label = "Positive"
#         elif score < -0.05: label = "Negative"
#         else: label = "Neutral"
#         res.append({'Score': score, 'Sentiment': label})
#     return pd.concat([df, pd.DataFrame(res)], axis=1)

# # --- COLOR FUNCTION FOR TABLE ---
# def highlight_sentiment(val):
#     color = 'white'
#     weight = 'normal'
#     if val == 'Positive':
#         color = '#00FF9D' # Neon Green
#         weight = 'bold'
#     elif val == 'Negative':
#         color = '#FF4B4B' # Neon Red
#         weight = 'bold'
#     elif val == 'Neutral':
#         color = '#AAAAAA' # Grey
#     return f'color: {color}; font-weight: {weight}'

# # --- UI START ---
# st.markdown("<h1 style='text-align: center; color: white;'>⚡ YouTube Pulse Analyzer</h1>", unsafe_allow_html=True)
# st.write("") 

# # Sidebar
# with st.sidebar:
#     st.header("🔐 Settings")
#     api_key = st.text_input("Paste Google API Key", type="password")

# # Main Input
# col1, col2 = st.columns([4, 1])
# with col1:
#     url = st.text_input("Paste YouTube Video Link Here:", placeholder="https://...")
# with col2:
#     st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)
#     btn = st.button("ANALYZE 🚀", use_container_width=True)

# # Processing
# if btn:
#     if not api_key or not url:
#         st.error("⚠️ Check API Key and URL.")
#     else:
#         vid_id = get_video_id(url)
#         if vid_id:
#             with st.spinner("Analyzing..."):
#                 df = get_comments(vid_id, api_key)
#                 if df is not None:
#                     df_new = analyze(df)
                    
#                     # Metrics
#                     st.markdown("### 📊 Result Overview")
#                     m1, m2, m3, m4 = st.columns(4)
#                     total = len(df_new)
#                     pos = len(df_new[df_new['Sentiment']=='Positive'])
#                     neg = len(df_new[df_new['Sentiment']=='Negative'])
                    
#                     m1.metric("Total", total)
#                     m2.metric("Positive", pos, f"{(pos/total)*100:.0f}%")
#                     m3.metric("Negative", neg, f"-{(neg/total)*100:.0f}%", delta_color="inverse")
#                     m4.metric("Mood", "😁 Happy" if df_new['Score'].mean() > 0 else "😐 Neutral")
                    
#                     st.markdown("---")

#                     # Charts
#                     c1, c2 = st.columns(2)
#                     with c1:
#                         fig = px.pie(df_new, names='Sentiment', hole=0.5,
#                                      color='Sentiment',
#                                      color_discrete_map={'Positive':'#00FF9D', 'Negative':'#FF4B4B', 'Neutral':'#888888'})
#                         fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
#                         st.plotly_chart(fig, use_container_width=True)
#                     with c2:
#                         fig2 = px.histogram(df_new, x="Score", nbins=20, color_discrete_sequence=['#00D4FF'])
#                         fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
#                         st.plotly_chart(fig2, use_container_width=True)
                        
#                     # --- TABLE VIEW START (YEH CHANGE KIYA HAI) ---
#                     st.markdown("### 📝 Detailed Data Table")
#                     st.markdown("Sort by clicking on headers (Score, Sentiment, etc.)")

#                     # 1. Columns reorder kar rahe hain taaki Sentiment pehle dikhe
#                     display_df = df_new[['Sentiment', 'Score', 'Comment', 'Author']]

#                     # 2. Table par Color Logic lagana (Pandas Styler)
#                     styled_df = display_df.style.map(highlight_sentiment, subset=['Sentiment']) \
#                                                 .format("{:.2f}", subset=['Score']) # Score ko 2 decimal tak dikhana

#                     # 3. Streamlit Table Display
#                     st.dataframe(
#                         styled_df,
#                         use_container_width=True,
#                         height=500, # Height fix taaki scroll kar sako
#                         column_config={
#                             "Sentiment": st.column_config.TextColumn("Sentiment", help="Mood of the comment", width="medium"),
#                             "Score": st.column_config.NumberColumn("Score (-1 to +1)", format="%.2f", width="small"),
#                             "Comment": st.column_config.TextColumn("Comment Text", width="large"),
#                         },
#                         hide_index=True # 0,1,2 hata diya
#                     )
#                     # --- TABLE VIEW END ---
                        
#                 else:
#                     st.error("Error fetching comments.")
#         else:
#             st.error("Invalid URL.")


import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time

# --- Config ---
st.set_page_config(page_title="YT Pulse", page_icon="⚡", layout="wide")
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

# --- Load CSS ---
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# CSS file honi zaruri hai folder mein
try:
    local_css("style.css")
except:
    pass # Agar css file nahi mili toh crash nahi hoga

# --- Helpers ---
def get_video_id(url):
    if "v=" in url: return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url: return url.split("/")[-1]
    return None

# --- 🔥 UPDATED FUNCTION: MULTI-PAGE FETCHER 🔥 ---
def get_comments(video_id, api_key, target_limit):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        all_comments = []
        next_page_token = None
        
        # Progress Bar create karte hain
        progress_text = "Fetching comments..."
        my_bar = st.progress(0, text=progress_text)
        
        while len(all_comments) < target_limit:
            # API Call (Hamesha 100 mangenge)
            request = youtube.commentThreads().list(
                part="snippet", 
                videoId=video_id, 
                maxResults=100, # Official Limit 100 hai
                textFormat="plainText",
                pageToken=next_page_token
            )
            response = request.execute()
            
            # Data nikalna
            for item in response['items']:
                c = item['snippet']['topLevelComment']['snippet']
                all_comments.append([c['authorDisplayName'], c['textDisplay']])
                
                # Agar target pura ho gaya toh turant ruk jao
                if len(all_comments) >= target_limit:
                    break
            
            # Progress Bar Update
            current_count = len(all_comments)
            percent = min(current_count / target_limit, 1.0) # 100% se upar na jaye
            my_bar.progress(percent, text=f"Fetched {current_count} / {target_limit} comments...")
            
            # Check karo aur pages hain kya?
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
                time.sleep(0.1) # Thoda sa break taaki Google block na kare
            else:
                # Agar video mein total comments hi kam hain (e.g. 80 hain aur aapne 500 manga)
                my_bar.progress(1.0, text="No more comments available on this video.")
                break 
                
        my_bar.empty() # Kaam hone ke baad progress bar hata do
        return pd.DataFrame(all_comments, columns=['Author', 'Comment'])
    
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def analyze(df):
    res = []
    for c in df['Comment']:
        # Convert to string to handle numbers/emojis safely
        text = str(c)
        score = sia.polarity_scores(text)['compound']
        
        if score > 0.05: label = "Positive"
        elif score < -0.05: label = "Negative"
        else: label = "Neutral"
        res.append({'Score': score, 'Sentiment': label})
    return pd.concat([df, pd.DataFrame(res)], axis=1)

def highlight_sentiment(val):
    color = 'white'
    weight = 'normal'
    if val == 'Positive':
        color = '#00FF9D'
        weight = 'bold'
    elif val == 'Negative':
        color = '#FF4B4B'
        weight = 'bold'
    elif val == 'Neutral':
        color = '#AAAAAA'
    return f'color: {color}; font-weight: {weight}'

# --- UI START ---
st.markdown("<h1 style='text-align: center; color: white;'>⚡ YouTube Pulse Analyzer</h1>", unsafe_allow_html=True)
st.write("") 

# Sidebar
with st.sidebar:
    st.header("🔐 Settings")
    api_key = st.text_input("Paste Google API Key", type="password")
    st.markdown("---")
    
    st.header("📊 Analysis Depth")
    # Slider: 100 se 1000 tak
    limit = st.slider("Select Limit:", 100, 1000, 100, step=100)
    st.caption(f"Target: {limit} comments")

# Main Input
col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("Paste YouTube Video Link Here:", placeholder="https://...")
with col2:
    st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)
    btn = st.button("ANALYZE 🚀", use_container_width=True)

# Processing
if btn:
    if not api_key or not url:
        st.error("⚠️ Check API Key and URL.")
    else:
        vid_id = get_video_id(url)
        if vid_id:
            # Spinner ab function ke andar progress bar se replace ho gaya hai
            df = get_comments(vid_id, api_key, target_limit=limit)
            
            if df is not None and not df.empty:
                df_new = analyze(df)
                
                # Metrics
                st.markdown("### 📊 Result Overview")
                m1, m2, m3, m4 = st.columns(4)
                total = len(df_new)
                pos = len(df_new[df_new['Sentiment']=='Positive'])
                neg = len(df_new[df_new['Sentiment']=='Negative'])
                
                m1.metric("Total", total)
                m2.metric("Positive", pos, f"{(pos/total)*100:.0f}%")
                m3.metric("Negative", neg, f"-{(neg/total)*100:.0f}%", delta_color="inverse")
                m4.metric("Mood", "😁 Happy" if df_new['Score'].mean() > 0 else "😐 Neutral")
                
                st.markdown("---")

                # Charts
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
                    
                # Table View
                st.markdown("### 📝 Detailed Data Table")
                st.markdown("Sort by clicking on headers")

                display_df = df_new[['Sentiment', 'Score', 'Comment', 'Author']]
                styled_df = display_df.style.map(highlight_sentiment, subset=['Sentiment']) \
                                            .format("{:.2f}", subset=['Score'])

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=500,
                    column_config={
                        "Sentiment": st.column_config.TextColumn("Sentiment", width="medium"),
                        "Score": st.column_config.NumberColumn("Score", format="%.2f", width="small"),
                        "Comment": st.column_config.TextColumn("Comment Text", width="large"),
                    },
                    hide_index=True
                )
                    
            else:
                st.warning("Could not fetch comments. (Check if video has comments or if API Key is valid)")
        else:
            st.error("Invalid URL.")