# 🗣 HTML to Speech Converter (macOS, Offline, Edge TTS)

This is a simple desktop app (Tkinter GUI) for **macOS** that converts saved HTML articles into audio using Edge TTS.  

The following are the summary of the major functions.
- 🧹 Cleans and extracts readable text
- 🎧 Adds natural pauses using `.`
- 🔕 Skips citations, figure captions, and boxes
- 🎙 Converts to MP3 (chunked and merged)
- 💾 Works completely **offline**

---

## 💾 How to Save HTML Articles

1. Open the article in your web browser (e.g., Nature, Science).
2. Click **File > Save As…**
3. Choose **Webpage, HTML only** format.
4. Save it to your local machine.

---

## 🖥 How to Use

1. **Open HTML**  
   Click `Open HTML` and select the `.html` file you just saved.

2. **Choose Speed (Optional)**  
   Select from `-20%`, `0%`, or `+25%` for speech rate.

3. **Generate MP3s**  
   Click `Generate MP3s` to:

   - ✅ Clean and extract article content  
   - ✅ Add artificial pauses using `.`  
   - ✅ Remove superscript citations  
   - ✅ Generate MP3 chunks using Edge TTS  
   - ✅ Merge all chunks into a single `full_combined.mp3` file

---

## 📂 Output


All audio files are saved to:  
.../saved_mp3s/<article-title>/
This includes:

- `chunk_01.mp3`, `chunk_02.mp3`, ...
- `full_combined.mp3` — the final result

---

## 🧠 How It Works

- Cleans unwanted HTML tags like `<script>`, `<style>`, `<figure>`, etc.
- Skips captions and box-like sections (`class="box"` or `<figure>`)
- Inserts periods (`.`) after titles/headings to simulate a pause
- Removes in-text citations like superscript `12`
- Splits long text into chunks (~4900 characters)
- Uses `edge-tts` with `--text` mode for compatibility and speed
- Merges audio chunks using `pydub` and `ffmpeg`

---

## ⚠️ Notes

- ⚙️ Designed for **macOS only**
- ✅ Works fully **offline** after setup
- 🧱 Built with Tkinter — no browser or web server needed
- 🎧 Uses Microsoft's high-quality `en-US-AriaNeural` voice
- 📜 Ensure Python, `edge-tts`, `pydub`, and `ffmpeg` are installed

---

## 📦 Dependencies

Install with:

```bash
pip install edge-tts pydub beautifulsoup4
brew install ffmpeg  # for pydub support

