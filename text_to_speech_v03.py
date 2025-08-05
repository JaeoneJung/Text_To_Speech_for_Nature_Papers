import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import subprocess
import os
import re
import threading
from pathlib import Path
import tempfile

from pydub import AudioSegment


CHUNK_LIMIT = 4900
VOICE = "en-US-AriaNeural"
SAVE_BASE_PATH = "/Users/jjung4/Desktop/saved_mp3s"

class FullHTMLReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Reader with Aria Voice (. Pause Version)")

        self.full_text = ""
        self.article_title = "Untitled"
        self.chunk_files = []
        self.speech_rate = tk.StringVar(value="0%")

        self.build_ui()

    def build_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="Open HTML", command=self.load_html).grid(row=0, column=0, padx=5)
        tk.Label(control_frame, text="Speed: ").grid(row=0, column=1)
        tk.OptionMenu(control_frame, self.speech_rate, "-20%", "0%", "+25%").grid(row=0, column=2)
        tk.Button(control_frame, text="Generate MP3s", command=self.generate_chunks_threaded).grid(row=0, column=3, padx=10)

        self.text_box = tk.Text(self.root, wrap="word", height=25, width=100)
        self.text_box.pack(padx=10, pady=10)

        self.status_label = tk.Label(
            self.root, text="Status: Idle", fg="dark blue", bg="light gray",
            font=("Helvetica", 11, "bold"), anchor="w"
        )
        self.status_label.pack(side="bottom", fill="x")

    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))

    def show_error(self, title, message):
        self.root.after(0, lambda: messagebox.showerror(title, message))

    def load_html(self):
        file_path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "head", "noscript", "meta", "link"]):
            tag.decompose()

        for tag in soup.find_all(["figure", "figcaption"]):
            tag.decompose()

        for tag in soup.find_all(["div", "section"], class_=lambda c: c and ("figure" in c or "box" in c)):
            tag.decompose()
        
        # Remove in-text citation superscripts (e.g., 1, 2, 12)
        for sup in soup.find_all("sup"):
            if sup.find("a", attrs={"data-test": "citation-ref"}):
                sup.decompose()

        # Extract title
        title_tag = soup.find("h1", class_="c-article-title")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        self.article_title = re.sub(r"[\\/*?\"<>|]", "", title)[:50]

        # Extract abstract
        abstract = ""
        abstract_section = soup.find("section", attrs={"aria-labelledby": "Abs1"})
        if abstract_section:
            content = abstract_section.find("div", class_="c-article-section__content")
            if content:
                abstract = content.get_text(separator=" ", strip=True)

        # Extract main content
        main_div = soup.find("div", class_="main-content")
        main_content = main_div if main_div else soup

        # Function to force pause
        def with_dot(tag_or_text):
            text = tag_or_text.get_text(strip=True) if hasattr(tag_or_text, "get_text") else tag_or_text
            return text.strip(".") + ". "

        # Build full text with pauses
        parts = []
        parts.append(with_dot(title))
        if abstract:
            parts.append(with_dot("Abstract"))
            parts.append(with_dot(abstract))

        for elem in main_content.find_all(True):
            if elem.name in ["h1", "h2", "h3"]:
                parts.append(with_dot(elem))
            elif elem.name == "p":
                text = elem.get_text(strip=True)
                if text:
                    parts.append(text)

        self.full_text = re.sub(r'\s+', ' ', ' '.join(parts)).strip()
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, self.full_text)
        self.update_status("HTML loaded.")

    def chunk_text(self, text, limit):
        chunks = []
        while len(text) > limit:
            split_at = text.rfind(" ", 0, limit)
            if split_at == -1:
                split_at = limit
            chunks.append(text[:split_at])
            text = text[split_at:].lstrip()
        if text:
            chunks.append(text)
        return chunks

    def generate_chunks_threaded(self):
        threading.Thread(target=self.generate_chunks, daemon=True).start()

    def generate_chunks(self):
        self.update_status("Generating MP3s...")
        chunks = self.chunk_text(self.full_text, CHUNK_LIMIT)
        rate = self.speech_rate.get()
        if rate == "0%":
            rate = "+0%"

        output_dir = Path(SAVE_BASE_PATH) / self.article_title
        output_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_files = []

        for i, chunk in enumerate(chunks):
            out_file = output_dir / f"chunk_{i+1:02}.mp3"

            result = subprocess.run([
                "python3", "-m", "edge_tts",
                "--voice", VOICE,
                "--text", chunk,
                "--rate", rate,
                "--write-media", str(out_file)
            ], capture_output=True, text=True)

            if result.returncode != 0:
                self.show_error("TTS Error", result.stderr)
                self.update_status("TTS error occurred.")
                return

            self.chunk_files.append(str(out_file))

        self.update_status("Combining MP3 chunks...")

        combined = AudioSegment.empty()
        for path in self.chunk_files:
            combined += AudioSegment.from_mp3(path)

        combined_path = output_dir / "full_combined.mp3"
        combined.export(combined_path, format="mp3")

        self.update_status("MP3 Generation & Merge Complete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FullHTMLReaderApp(root)
    root.mainloop()
