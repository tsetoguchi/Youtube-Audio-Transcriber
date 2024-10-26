import os
import subprocess

import whisper
import yt_dlp

from fetchurls import fetch_youtube_urls

# Dictionary to hold transcriptions
transcriptions = {}


def download_audio(youtube_url, output_path="audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # yt-dlp renames the file to 'audio.mp3.mp3', so update the path
        mp3_file = f"{output_path}.mp3"
        if os.path.exists(mp3_file):
            print(f"Audio downloaded successfully to {mp3_file}")
            return mp3_file
        else:
            print(f"Error: Output file {mp3_file} does not exist.")
            return None
    except Exception as e:
        print(f"Error downloading audio with yt-dlp: {e}")
        return None


def convert_to_wav(input_file, output_file="audio.wav"):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return None

    # Convert the downloaded file to WAV format with overwrite option
    command = f"ffmpeg -y -i {input_file} -vn -acodec pcm_s16le -ar 44100 -ac 2 {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Audio converted to {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


def transcribe_audio(audio_file, quality):
    quality_dict = {"1": "base", "2": "small",
                    "3": "medium", "4": "large"}

    # Load the Whisper model
    model = whisper.load_model(quality_dict[quality])
    # Transcribe the audio file
    result = model.transcribe(audio_file)
    print("Transcription completed.")
    return result["text"]


def fetch_video_title(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info.get('title', 'Unknown Title')


def process_youtube_urls(youtube_urls, quality):
    for youtube_url in youtube_urls:
        audio_file = download_audio(youtube_url)

        if audio_file is None:
            print(f"Failed to download audio for {youtube_url}.")
            continue

        wav_file = convert_to_wav(audio_file)

        if wav_file is None:
            print(f"Failed to convert audio to WAV for {youtube_url}.")
            continue

        transcription = transcribe_audio(wav_file, quality)

        # Fetch the video title
        video_title = fetch_video_title(youtube_url)

        # Store the transcription in the dictionary
        transcriptions[video_title] = transcription

        # Delete audio files after processing
        try:
            os.remove(audio_file)  # Remove the .mp3 file
            os.remove(wav_file)  # Remove the .wav file
            print(f"Deleted audio files: {audio_file} and {wav_file}")
        except Exception as e:
            print(f"Error deleting audio files: {e}")

    # Save all transcriptions to a single text file
    with open("transcriptions.txt", 'w', encoding='utf-8') as f:
        for title, text in transcriptions.items():
            f.write(f"Title: {title}\n\nTranscription:\n{text}\n\n{'-' * 40}\n")
    print("All transcriptions saved to transcriptions.txt")


def channel_urls(channel_name):
    return fetch_youtube_urls(f"https://www.youtube.com/@{channel_name}")


def __check_quality(quality):
    int_quality = int(quality)
    try:
        if int_quality < 1 or int_quality > 4:
            raise Exception("Error: Quality must be between 1 - 4.")
    except:
        raise Exception("Error: An exception occurred, Quality must be a number between 1 - 4.")


def main():
    quality = input("Choose transcription quality 1 - 4. Lowest to highest.\n")
    __check_quality(quality)
    channel_name = input("Channel Name: \n")

    urls = channel_urls(channel_name)
    process_youtube_urls(urls, quality)


if __name__ == "__main__":
    # Example list of YouTube URLs
    # urls = [
    #     "https://www.youtube.com/watch?v=lCuP3_dMtpA&ab_channel=CookingwithDog"  # Add more URLs as needed
    # ]
    main()
