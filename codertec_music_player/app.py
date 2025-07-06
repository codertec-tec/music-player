import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

class CodertecMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Codertec Music Player")
        self.root.geometry("1000x600")
        self.root.configure(bg="#0b0b0b")
        self.current_song = ""
        self.playlist = []

        self.create_ui()

    def create_ui(self):
        # Left sidebar (playlist)
        self.sidebar = tk.Frame(self.root, bg="#111", width=250)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Playlist", bg="#111", fg="#00ffe1", font=("Consolas", 14, "bold")).pack(pady=10)

        self.song_listbox = tk.Listbox(self.sidebar, bg="#0f0f0f", fg="#39ff14", font=("Consolas", 12), selectbackground="#00ffe1", height=25)
        self.song_listbox.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Button(self.sidebar, text="Add Songs", command=self.add_songs, bg="#00ffe1", fg="#000", font=("Consolas", 11, "bold")).pack(pady=10)

        # Album Art Frame
        self.album_frame = tk.Frame(self.root, bg="#0b0b0b")
        self.album_frame.pack(side="top", fill="x", padx=20, pady=20)

        self.album_art = tk.Label(self.album_frame, bg="#0b0b0b")
        self.album_art.pack()

        self.song_title = tk.Label(self.album_frame, text="Now Playing", fg="#39ff14", bg="#0b0b0b", font=("Consolas", 18, "bold"))
        self.song_title.pack(pady=5)

        # Controls
        self.controls_frame = tk.Frame(self.root, bg="#0b0b0b")
        self.controls_frame.pack(side="bottom", fill="x", pady=30)

        self.play_btn = tk.Button(self.controls_frame, text="▶", command=self.play_song, font=("Consolas", 16), width=5, bg="#111", fg="#00ffe1", relief="flat")
        self.play_btn.pack(side="left", padx=20)

        self.pause_btn = tk.Button(self.controls_frame, text="⏸", command=self.pause_song, font=("Consolas", 16), width=5, bg="#111", fg="#00ffe1", relief="flat")
        self.pause_btn.pack(side="left", padx=20)

        self.stop_btn = tk.Button(self.controls_frame, text="⏹", command=self.stop_song, font=("Consolas", 16), width=5, bg="#111", fg="#00ffe1", relief="flat")
        self.stop_btn.pack(side="left", padx=20)

        self.volume_slider = ttk.Scale(self.controls_frame, from_=0, to=1, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="right", padx=20)

        # Placeholder waveform visual
        self.waveform = tk.Canvas(self.root, height=120, bg="#0b0b0b", highlightthickness=0)
        self.waveform.pack(fill="x", padx=20)
        self.draw_waveform()

    def draw_waveform(self):
        width = 960
        height = 100
        bars = 80
        bar_width = width / bars
        for i in range(bars):
            x0 = i * bar_width
            x1 = x0 + 4
            y = height / 2
            y1 = y - (i % 7 + 5) * 4
            y2 = y + (i % 7 + 5) * 4
            self.waveform.create_line(x0, y1, x0, y2, fill="#00ffe1", width=2)

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        for file in files:
            self.song_listbox.insert("end", os.path.basename(file))
            self.playlist.append(file)

    def play_song(self):
        try:
            selected = self.song_listbox.curselection()
            if selected:
                index = selected[0]
                self.current_song = self.playlist[index]
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
                self.song_title.config(text=os.path.basename(self.current_song))
        except Exception as e:
            print("Error playing song:", e)

    def pause_song(self):
        pygame.mixer.music.pause()

    def stop_song(self):
        pygame.mixer.music.stop()

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodertecMusicPlayer(root)
    root.mainloop()
