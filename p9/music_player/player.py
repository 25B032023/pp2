import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.music_folder = music_folder

        self.playlist = [
            f for f in os.listdir(music_folder)
            if f.endswith(".mp3") or f.endswith(".wav")
        ]

        if not self.playlist:
            raise FileNotFoundError("No music files found in 'music' folder")

        self.index = 0
        self.paused = False

    def current_path(self):
        return os.path.join(self.music_folder, self.playlist[self.index])

    def current_track(self):
        return self.playlist[self.index]

    def play(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.load(self.current_path())
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
        self.paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_track(self):
        self.index = (self.index + 1) % len(self.playlist)
        pygame.mixer.music.load(self.current_path())
        pygame.mixer.music.play()
        self.paused = False

    def previous_track(self):
        self.index = (self.index - 1) % len(self.playlist)
        pygame.mixer.music.load(self.current_path())
        pygame.mixer.music.play()
        self.paused = False