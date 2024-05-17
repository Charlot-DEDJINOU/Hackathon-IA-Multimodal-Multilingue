import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "c3bf086135054edd8241e3910bbaf307"

# URL of the file to transcribe
FILE_URL = "video.mp4"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    transcipt = transcript.export_subtitles_srt()
    print(transcript.export_subtitles_srt())
