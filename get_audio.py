import subprocess
import yt_dlp
import os  # Use yt-dlp instead of pytube

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