import asyncio
import random, string
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from create_anki_card import create_anki_card
from get_audio import download_audio_segment
from get_screenshot import download_video, capture_screenshot
from get_subtitles import get_subtitles_text
from translate import translate_text


def generate_random_filename(file_extensions=None, length=10):
    if file_extensions is None:
        file_extensions = ['.txt', '.jpg', '.png', '.mp3', '.pdf']
    file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    file_extension = random.choice(file_extensions)
    return file_name + file_extension

def process_video():
    youtube_url = youtube_url_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    try:
        start_time = int(start_time)
        end_time = int(end_time)
        if start_time < 0 or end_time < 0 or start_time >= end_time:
            raise ValueError("Invalid start or end times.")


        MP3_OUTPUT_FILENAME = "C:\\Users\\kirab\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\" + generate_random_filename(['.mp3'])
        SCREENSHOT_OUTPUT_FILENAME = "C:\\Users\\kirab\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\" + generate_random_filename(['.png'])
        DECK_FILENAME = generate_random_filename(['.apkg'])

        download_audio_segment(youtube_url, start_time, end_time, MP3_OUTPUT_FILENAME)
        SUBTITLE_TEXT = get_subtitles_text(youtube_url, start_time, end_time, 'de')
        download_video(youtube_url)
        capture_screenshot('video.mp4', (start_time + end_time) / 2, SCREENSHOT_OUTPUT_FILENAME)
        TRANSLATED_TEXT = asyncio.run(translate_text(SUBTITLE_TEXT, 'en', 'de'))
        create_anki_card(SUBTITLE_TEXT, TRANSLATED_TEXT, MP3_OUTPUT_FILENAME, SCREENSHOT_OUTPUT_FILENAME, deck_filename=DECK_FILENAME)
        os.remove('video.mp4')

        messagebox.showinfo("Success", "Anki card created successfully!")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


root = tk.Tk()
root.title("Anki Card Creator")

# Labels and Entry fields
youtube_url_label = ttk.Label(root, text="YouTube URL:")
youtube_url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
youtube_url_entry = ttk.Entry(root, width=50)
youtube_url_entry.grid(row=0, column=1, padx=5, pady=5)

start_time_label = ttk.Label(root, text="Start Time (seconds):")
start_time_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
start_time_entry = ttk.Entry(root, width=10)
start_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

end_time_label = ttk.Label(root, text="End Time (seconds):")
end_time_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
end_time_entry = ttk.Entry(root, width=10)
end_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Process Button
process_button = ttk.Button(root, text="Create Anki Card", command=process_video)
process_button.grid(row=3, column=0, columnspan=2, pady=10)


root.mainloop()