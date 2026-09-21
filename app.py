import streamlit as st
import yt_dlp
import os

# 1. 設定網頁基本資訊 (必須放在所有 st 指令的最前面)
st.set_page_config(
    page_title="智慧影音下載神器",
    page_icon="🎬",
    layout="centered"
)

# 2. 注入自訂 CSS 來完全對齊你原本的網站風格
st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設的右上角選單、Header 與底部浮水印，讓它看起來像你網站的一部分 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 更改整體背景顏色為淺灰藍色，對齊你原本網站的 --primary-bg */
    .stApp {
        background-color: #f4f7fb;
    }
    
    /* 將主內容區塊包裝成白色卡片風格，加上圓角與陰影 */
    .main .block-container {
        background-color: #ffffff;
        padding: 3rem 4rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
        margin-top: 3rem;
        max-width: 800px;
    }
    
    /* 自訂按鈕樣式 (對齊你網站的 btn-blue 風格) */
    .stButton>button {
        background-color: #0ea5e9;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.2);
    }
    .stButton>button:hover {
        background-color: #0284c7;
        transform: translateY(-2px);
        color: white;
    }
    
    /* 輸入框樣式對齊 */
    .stTextInput>div>div>input {
        background-color: #f8fafc;
        border: 1px solid #dce4ec;
        border-radius: 10px;
        padding: 12px;
        font-size: 1rem;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3a86ff;
        box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.15);
        background-color: #ffffff;
    }
    
    /* 標題文字顏色微調 */
    h1, h2, h3, p {
        color: #2c3e50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 網頁主要內容
st.title("🎬 智慧影音下載神器")
st.write("貼上影音網址，系統會自動在雲端解析並提供 MP4 下載連結。")

url = st.text_input("請貼上想要下載的影音網址：", placeholder="例如：https://www.youtube.com/watch?v=...")

if st.button("開始解析並下載"):
    if url:
        with st.spinner("影片下載與轉檔中，請耐心稍候..."):
            download_folder = 'download'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'noplaylist': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                st.success("✨ 解析成功！請點擊下方按鈕儲存至你的裝置：")
                
                with open(filename, "rb") as file:
                    st.download_button(
                        label="⬇️ 點此下載 MP4 影片",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"發生錯誤，可能是不支援該網址或影片已設為私人：{e}")
    else:
        st.warning("請先輸入網址喔！")