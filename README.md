# 🗣 HTML to Speech Converter  
### (macOS • Offline • Edge TTS)

A simple, offline desktop app built with **Tkinter** for macOS. It converts saved HTML articles into MP3 audio using Microsoft’s `en-US-AriaNeural` voice via **Edge TTS**.

---

### ✨ Key Features

- 🧹 Cleans and extracts readable text  
- 🎧 Adds natural pauses using `. `  
- 🔕 Removes citations, figure captions, and boxes  
- 🎙 Converts to MP3 (chunked and merged)  
- 💾 Works entirely **offline** after setup  

---

## 💾 Saving HTML Articles

To use this app, save the webpage first:

1. Open the article in your browser (e.g., *Nature*, *Science*)
2. Click **File > Save As…**
3. Choose **Webpage, HTML only**
4. Save it to your local machine

---

## 🖥 How to Use

1. **Open HTML**  
   Click `Open HTML` and choose the `.html` file you saved.

2. **Set Speech Speed (Optional)**  
   Select from `-20%`, `0%`, or `+25%` to adjust speech tempo.

3. **Generate MP3s**  
   Click `Generate MP3s` to:
   - ✅ Clean and extract article content  
   - ✅ Add artificial pauses after headings  
   - ✅ Remove superscript citations  
   - ✅ Generate multiple MP3 chunks  
   - ✅ Merge them into `full_combined.mp3`

---

## 📂 Output

All generated files will be saved to:  
`.../saved_mp3s/<article-title>/`  


This includes:

- `chunk_01.mp3`, `chunk_02.mp3`, ...
- `full_combined.mp3` — the final result

---

## 🧠 How It Works

- Removes unwanted tags: `<script>`, `<style>`, `<figure>`, etc.
- Skips "box" sections and figures
- Converts headings into natural pauses using `. `
- Removes citation superscripts like `12`
- Splits long content into ~4900-character chunks
- Uses `edge-tts` with `--text` for fast offline conversion
- Merges chunks using `pydub` + `ffmpeg`

---

## ⚠️ Notes

- 🖥 Designed for **macOS only**
- 🔌 Requires no internet once dependencies are installed
- 💡 GUI built with **Tkinter**
- 🎤 Voice: Microsoft `en-US-AriaNeural`
- 🧰 Requires Python and a few packages (see below)

---

## 📦 Installation

Install dependencies:

```bash
pip install edge-tts pydub beautifulsoup4
brew install ffmpeg  # required for pydub to merge MP3s
