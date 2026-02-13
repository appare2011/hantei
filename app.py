from flask import Flask, render_template, request, jsonify
import re
import unicodedata
import os

app = Flask(__name__)

class LanguageDetector:
    def __init__(self):
        self.hiragana_pattern = re.compile(r'[\u3040-\u309F]')
        self.katakana_pattern = re.compile(r'[\u30A0-\u30FF]')
        self.kanji_pattern = re.compile(r'[\u4E00-\u9FAF]')
        self.english_pattern = re.compile(r'[a-zA-Z]')
        
    def detect_language(self, text):
        text = unicodedata.normalize('NFKC', text)
        if not text.strip():
            return {"language": "unknown", "confidence": 0, "details": "テキストが空です"}
        
        hiragana_count = len(self.hiragana_pattern.findall(text))
        katakana_count = len(self.katakana_pattern.findall(text))
        kanji_count = len(self.kanji_pattern.findall(text))
        english_count = len(self.english_pattern.findall(text))
        
        japanese_count = hiragana_count + katakana_count + kanji_count
        total_chars = len(re.sub(r'\s+', '', text))
        
        if total_chars == 0:
            return {"language": "unknown", "confidence": 0, "details": "有効な文字がありません"}
        
        japanese_ratio = japanese_count / total_chars
        english_ratio = english_count / total_chars
        
        if japanese_ratio > 0.3:
            confidence = min(japanese_ratio * 100, 95)
            details = f"ひらがな: {hiragana_count}, カタカナ: {katakana_count}, 漢字: {kanji_count}"
            return {"language": "japanese", "confidence": confidence, "details": details}
        elif english_ratio > 0.7:
            confidence = min(english_ratio * 100, 95)
            details = f"英字: {english_count}文字"
            return {"language": "english", "confidence": confidence, "details": details}
        else:
            return {"language": "mixed", "confidence": 50, "details": "日本語と英語が混在しています"}

detector = LanguageDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')
    result = detector.detect_language(text)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)