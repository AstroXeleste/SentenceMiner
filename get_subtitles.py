from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta

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
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


# if __name__ == "__main__":
#     video_url = input("Enter the YouTube video URL: ")
#     start_time_seconds = float(input("Enter the start time in seconds: "))
#     end_time_seconds = float(input("Enter the end time in seconds: "))

#     subtitles_text = get_subtitles_text(video_url, start_time_seconds, end_time_seconds)

#     if subtitles_text:
#         print(subtitles_text)
#     else:
#         print("No subtitles found or an error occurred.")
