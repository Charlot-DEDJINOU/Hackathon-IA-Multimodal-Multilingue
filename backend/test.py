import math
import ffmpeg
import assemblyai as aai
import os

def transcribe_srt(file="static/videoplayback.mp4"):
    config = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        print({"error": transcript.error})
    else:
        # Exporter la transcription au format SRT
        subtitles_srt = transcript.export_subtitles_srt()

        with open("subtitle-yo.srt", "w") as f:
            f.write(subtitles_srt)
    return "subtitle-yo.srt"

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time


def add_subtitle_to_video(soft_subtitle, subtitle_file="subtitle-yo.srt", subtitle_language="yo"):
    video_file = "static/videoplayback.mp4"
    output_video = "output-videoplayback.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    # Verify subtitle file exists
    if not os.path.exists(subtitle_file):
        print(f"Subtitle file not found: {subtitle_file}")
        return

    # Add soft or hard subtitles
    if soft_subtitle:
        # Soft subtitles (embedding subtitles as a separate track)
        stream = ffmpeg.output(
            ffmpeg.input(video_file),
            ffmpeg.input(subtitle_file),
            output_video,
            **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
               "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
    else:
        # Hard subtitles (burning subtitles into the video)
        stream = ffmpeg.output(
            ffmpeg.input(video_file),
            output_video,
            vf=f"subtitles={subtitle_file}"
        )

    try:
        ffmpeg.run(stream, overwrite_output=True)
        print(f"Subtitles added successfully to {output_video}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode('utf8')}")


# Example usage
# Ensure transcription and subtitle file creation is done first
# add_subtitle_to_video(False)
transcribe_srt()