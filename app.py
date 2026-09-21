import streamlit as st
import yt_dlp
import os

# 1. 設定網頁基本資訊
st.set_page_config(page_title="智慧影音下載神器", page_icon="🎬", layout="centered")

# 2. 升級版 CSS：修復文字顏色衝突、增強卡片立體感
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    
    /* 確保整體背景為淺灰藍色 */
    .stApp {
        background-color: #f4f7fb;
    }
    
    /* 強制所有文字變成深藍灰，避免瀏覽器深色模式干擾 */
    html, body, [class*="st-"] {
        color: #2c3e50 !important;
    }
    
    /* 讓主內容區塊變成一個帶有陰影的立體卡片 */
    [data-testid="block-container"] {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.03);
        margin-top: 3rem;
        max-width: 700px;
    }
    
    /* 👑 修復輸入框：確保背景微灰、文字深色清晰 */
    .stTextInput input {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1.05rem !important;
        color: #0f172a !important; /* 確保輸入的網址是深色的 */
        font-weight: 500 !important;
    }
    .stTextInput input:focus {
        border-color: #3a86ff !important;
        box-shadow: 0 0 0 4px rgba(58, 134, 255, 0.15) !important;
        background-color: #ffffff !important;
    }
    
    /* 升級按鈕質感 */
    .stButton>button {
        background-color: #0ea5e9;
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 14px 24px;
        font-weight: bold;
        font-size: 1.15rem;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.25);
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #0284c7;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(14, 165, 233, 0.35);
    }
    </style>
""", unsafe_allow_html=True)

# 3. 網頁主要內容
st.title("🎬 智慧影音下載神器")
st.markdown("只需貼上影音網址，系統會自動在雲端解析，並提供最高畫質的 MP4 檔案。")

# 加入展開說明區塊，讓畫面不空洞且更專業
with st.expander("💡 支援哪些網站？ (點擊展開)", expanded=False):
    st.write("""
    本神器核心採用強大的開源套件，支援超過百種影音平台，包含：
    * **YouTube** (一般影片與 Shorts)
    * **Instagram** (Reels 短影音、貼文影片)
    * **Facebook** (公開社團或粉專影片)
    * **Bilibili (B站)**、**Twitter / X** 等各大平台
    """)

url = st.text_input("請貼上想要下載的影音網址：", placeholder="例如：https://www.youtube.com/watch?v=...")

if st.button("🚀 開始解析並下載"):
    if url:
        with st.spinner("影片下載與轉檔中，請耐心稍候 (時間取決於影片長短)..."):
            download_folder = 'download'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            # === 以下為新增的防阻擋參數 ===
            'source_address': '0.0.0.0',  # 強制使用 IPv4 避免雲端 IPv6 被封鎖
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']  # 偽裝成 Android 手機版與一般網頁版
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }
        }
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