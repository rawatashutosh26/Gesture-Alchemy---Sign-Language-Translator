import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import os
import string
import threading 

class ImageLabel(tk.Label):
    def load(self, im_path):
        if not os.path.exists(im_path):
            print(f"Error: File not found at {im_path}")
            self.stop_animation()
            self.config(image='', text="Image not found.")
            return
        im = Image.open(im_path)
        self.loc = 0
        self.frames = []
        try:
            for i in count(1):
                resized_frame = im.copy().resize((470, 325), Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                im.seek(i)
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(self.frames) > 1:
            self.next_frame()
        else:
            self.stop_animation()
            self.config(image=self.frames[0])

    def next_frame(self):
        if hasattr(self, 'frames') and self.frames:
            self.loc = (self.loc + 1) % len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after_id = self.after(self.delay, self.next_frame)

    def stop_animation(self):
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)
            delattr(self, 'after_id')

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hearing Impairment Assistant")
        self.root.geometry("700x600")
        self.media_folder = "SignMedia"
        self.recognizer = sr.Recognizer()
        self.is_listening = False 

        try:
            all_files = os.listdir(self.media_folder)
            self.phrase_map = {
                filename[:-4].replace(" ", "").lower(): filename 
                for filename in all_files if filename.endswith(".gif")
            }
            print(f"Loaded {len(self.phrase_map)} sign language phrases.")
        except FileNotFoundError:
            print(f"Error: Directory '{self.media_folder}' not found.")
            self.phrase_map = {}
        
        self.info_label = tk.Label(root, text="Click 'Start Listening' to begin.", font=("Helvetica", 14))
        self.info_label.pack(pady=10)
        self.spoken_text_label = tk.Label(root, text="You said: ...", font=("Helvetica", 12), fg="blue")
        self.spoken_text_label.pack(pady=10)
        self.image_display = ImageLabel(root, bg='lightgray')
        self.image_display.pack(pady=20, expand=True, fill='both')
        self.listen_button = tk.Button(root, text="Start Listening", command=self.start_listening_thread)
        self.listen_button.pack(pady=20)

        self.load_initial_logo()

    def load_initial_logo(self):
        logo_path = os.path.join(self.media_folder, 'signlang.png')
        self.image_display.load(logo_path)

    def start_listening_thread(self):
        if not self.is_listening:
            self.is_listening = True
            thread = threading.Thread(target=self.listen_loop, daemon=True)
            thread.start()
            self.listen_button.config(text="Listening...", state=tk.DISABLED)
            self.info_label.config(text="Listening continuously... Say 'Good Bye' to stop.")

    def listen_loop(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    self.root.after(0, self.update_spoken_text, text)
                    self.process_text(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"API Error: {e}")

    def update_spoken_text(self, text):
        self.spoken_text_label.config(text=f"You said: {text}")

    def process_text(self, text):
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).replace(" ", "")
        
        if clean_text in ["goodbye", "close", "exit", "stoplistening"]:
            self.info_label.config(text="Stopping... Click 'Start Listening' to begin again.")
            self.spoken_text_label.config(text="You said: ...")
            self.is_listening = False 
            self.listen_button.config(text="Start Listening", state=tk.NORMAL)
            self.root.after(0, self.load_initial_logo) 
            return

        if clean_text in self.phrase_map:
            original_filename = self.phrase_map[clean_text]
            gif_path = os.path.join(self.media_folder, original_filename)
            self.root.after(0, self.image_display.load, gif_path)
        else:
            self.root.after(0, self.spell_out_word, text)

    def spell_out_word(self, text):
        self.image_display.stop_animation()
        letters_to_show = [char for char in text if char.isalpha()]
        if not letters_to_show:
            self.image_display.config(image='', text="No letters to display.")
            return
        self.show_next_letter(letters_to_show, 0)

    def show_next_letter(self, letters, index):
        if index < len(letters):
            char = letters[index]
            image_path = os.path.join(self.media_folder, f"{char.upper()}.jpg")
            self.image_display.load(image_path)
            self.root.after(1000, lambda: self.show_next_letter(letters, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()