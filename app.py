import streamlit as st
import re
import unicodedata

# 判定ロジック
class LanguageDetector:
    def __init__(self):
        self.hiragana_pattern = re.compile(r'[\u3040-\u309F]')
        self.katakana_pattern = re.compile(r'[\u30A0-\u30FF]')
        self.kanji_pattern = re.compile(r'[\u4E00-\u9FAF]')
        self.english_pattern = re.compile(r'[a-zA-Z]')
        
    def detect_language(self, text):
        text = unicodedata.normalize('NFKC', text)
        if not text.strip():
            return "unknown", 0, "テキストが空です"
        
        hiragana_count = len(self.hiragana_pattern.findall(text))
        katakana_count = len(self.katakana_pattern.findall(text))
        kanji_count = len(self.kanji_pattern.findall(text))
        english_count = len(self.english_pattern.findall(text))
        
        japanese_count = hiragana_count + katakana_count + kanji_count
        total_chars = len(re.sub(r'\s+', '', text))
        
        if total_chars == 0:
            return "unknown", 0, "有効な文字がありません"
        
        japanese_ratio = japanese_count / total_chars
        english_ratio = english_count / total_chars
        
        if japanese_ratio > 0.3:
            return "日本語", min(japanese_ratio * 100, 95), f"ひらがな: {hiragana_count}, 漢字: {kanji_count}"
        elif english_ratio > 0.7:
            return "英語", min(english_ratio * 100, 95), f"英字: {english_count}文字"
        else:
            return "混在", 50, "日本語と英語が混ざっています"

# 画面表示の設定
st.set_page_config(page_title="言語判定ツール", page_icon="🌐")
st.title("🌐 言語判定ツール")
st.write("入力したテキストが日本語か英語かを判定します。")

text_input = st.text_area("テキストを入力してください", height=150)
detector = LanguageDetector()

if st.button("判定する"):
    if text_input:
        lang, confidence, details = detector.detect_language(text_input)
        
        st.subheader(f"結果: {lang}")
        st.progress(int(confidence) / 100)
        st.write(f"信頼度: {int(confidence)}%")
        st.info(details)
    else:
        st.warning("テキストを入力してください。")
