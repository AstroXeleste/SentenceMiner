import cv2
import yt_dlp
import os

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

def main():
    video_url = input("Enter YouTube video URL: ")
    timestamp = float(input("Enter timestamp in seconds: "))  # Accept timestamp as a float representing seconds

    # Download the video
    download_video(video_url)

    # Capture screenshot at the specified timestamp
    capture_screenshot('video.mp4', timestamp)

    # Optionally clean up by removing the downloaded video file
    os.remove('video.mp4')
    

if __name__ == '__main__':
    main()
