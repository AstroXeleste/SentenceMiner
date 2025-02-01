import subprocess
import yt_dlp
import os
import genanki
import cv2
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta
from googletrans import Translator
import asyncio

def download_audio_segment(youtube_url, start_time, end_time, output_filename="audio_segment.mp3"):
    """Downloads a segment of audio from a YouTube video using yt-dlp and FFmpeg."""

    temp_audio_filename = None  # Initialize to None

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            temp_audio_filename = ydl.prepare_filename(info_dict)  # Store the filename

        command = [
            "ffmpeg",
            "-i", temp_audio_filename, # Use the stored filename
            "-ss", str(start_time),
            "-to", str(end_time),
            "-vn",
            "-acodec", "mp3",
            "-ab", "192k",
            output_filename
        ]

        subprocess.run(command, check=True)
        print(f"Audio segment saved to {output_filename}")

    except yt_dlp.DownloadError as e:
        print(f"yt-dlp download error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(e)
    except KeyError as e:
        print(f"yt-dlp error, probably invalid URL: {e}")

    finally:  # Ensure cleanup always happens
        if temp_audio_filename and os.path.exists(temp_audio_filename):
            os.remove(temp_audio_filename)
            print(f"Temporary audio file {temp_audio_filename} removed.")

def create_anki_card(german_phrase, english_translation, audio_file, image_file, deck_name="German Phrases Deck", deck_filename='german_english_deck.apkg'):
    """
    Function to create an Anki card with a German phrase, English translation, audio file, and an image.
    """
    
    # Ensure the audio and image files exist
    if not os.path.exists(audio_file) or not os.path.exists(image_file):
        raise FileNotFoundError("Audio file or image file not found!")

    # Create an Anki model - CORRECTED FIELDS DEFINITION
    my_model = genanki.Model(
        1607392319,  # Unique model ID
        'German-English Model',
        fields=[
            {'name': 'German'},
            {'name': 'English'},
            {'name': 'Audio'},
            {'name': 'Image'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{German}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br><audio src="{{Audio}}"></audio><br><img src="{{Image}}"/>',
            },
        ]
    )

    # Create an Anki deck
    my_deck = genanki.Deck(
        2059400110,  # Unique deck ID
        deck_name
    )

    # Create a note with the German phrase, English translation, and files
    my_note = genanki.Note(
        model=my_model,
        fields=[german_phrase, english_translation, audio_file, image_file]
    )

    # Add the note to the deck
    my_deck.add_note(my_note)

    # Save the deck to a file
    my_deck.write_to_file(deck_filename)

    print(f"Anki deck generated successfully! Saved as '{deck_filename}'.")

def download_video(url, save_path='video.mp4'):
    """Download video from YouTube using yt-dlp."""
    ydl_opts = {
        'format': 'best[ext=mp4]',  # Choose the best quality MP4 video
        'outtmpl': save_path  # Save the video as video.mp4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading video from: {url}")
        ydl.download([url])
    print(f"Video downloaded to {save_path}")

def capture_screenshot(video_path, timestamp, screenshot_path='screenshot.png'):
    """Capture a screenshot at a given timestamp from the video."""
    # Open the video
    cap = cv2.VideoCapture(video_path)
    
    # Set the video position to the desired timestamp
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    
    # Read the frame
    ret, frame = cap.read()
    if ret:
        # Save the screenshot
        cv2.imwrite(screenshot_path, frame)
        print(f"Screenshot saved to {screenshot_path}")
    else:
        print("Failed to capture the screenshot.")
    
    # Release the video capture object
    cap.release()

def get_subtitles_text(video_url, start_time, end_time, language='en'):
    """
    Retrieves subtitles text from a YouTube video within a specified time range,
    without timestamps.

    Args:
        video_url: The URL of the YouTube video.
        start_time: The start time in seconds or a timedelta object.
        end_time: The end time in seconds or a timedelta object.
        language: The desired language of the subtitles (default: 'en').

    Returns:
        A string containing the concatenated subtitle text within the time range,
        or an empty string if subtitles are not available or an error occurs.
    """
    try:
        yt = YouTube(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(yt.video_id, languages=[language])

        if isinstance(start_time, timedelta):
          start_time_sec = start_time.total_seconds()
        else:
          start_time_sec = start_time

        if isinstance(end_time, timedelta):
          end_time_sec = end_time.total_seconds()
        else:
          end_time_sec = end_time

        subtitles_text = ""
        for entry in transcript:
            start = entry['start']
            duration = entry['duration']
            end = start + duration
            text = entry['text']

            if start_time_sec <= start <= end_time_sec or start <= start_time_sec <= end or start <= end_time_sec <= end:
                subtitles_text += text + " "  # Add text and a space

        return subtitles_text.strip()  # Remove trailing space

    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
async def translate_text(txt, target, src):
    translator = Translator()

    # Use await to call the translate function
    translated_text = await translator.translate(text=txt, src=src, dest=target)

    # Print the translated text
    return translated_text.text

    # Run the asynchronous function
asyncio.run(translate_text('überalles', 'en', 'de'))


YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=1KmY8CRuIHg"
TIMESTAMP_START = 10
TIMESTAMP_END = 30

def main():
    download_audio_segment(YOUTUBE_VIDEO_URL, TIMESTAMP_START, TIMESTAMP_END, "ankioutput.mp3")
    SUBTITLE_TEXT = get_subtitles_text(YOUTUBE_VIDEO_URL, TIMESTAMP_START, TIMESTAMP_END, 'de')
    download_video(YOUTUBE_VIDEO_URL)
    capture_screenshot('video.mp4', (TIMESTAMP_START+TIMESTAMP_END)/2, "screenshot.png")
    TRANSLATED_TEXT = asyncio.run(translate_text(SUBTITLE_TEXT, 'en', 'de'))
    create_anki_card(SUBTITLE_TEXT, TRANSLATED_TEXT, "ankioutput.mp3", "screenshot.png")

main()