import streamlit as st
import yt_dlp
import os

# 設定網頁標題
st.title("🎬 智慧影音下載神器")
st.write("貼上影音網址，系統會自動在雲端解析並提供 MP4 下載連結。")

# 建立一個文字輸入框
url = st.text_input("請貼上想要下載的影音網址：")

# 建立一個下載按鈕
if st.button("開始解析並下載"):
    if url:
        # 顯示載入中的動畫
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
                # 執行下載
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 抓取影片資訊，以便取得檔名
                    info = ydl.extract_info(url, download=True)
                    # 組合出檔案儲存的完整路徑
                    filename = ydl.prepare_filename(info)

                st.success("解析成功！請點擊下方按鈕儲存至你的裝置：")
                
                # 讀取下載好的影片，並提供網頁下載按鈕
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