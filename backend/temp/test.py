from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, pipeline
import torchaudio

# Initialize the speech recognition model and tokenizer
processor = Wav2Vec2Processor.from_pretrained("DereAbdulhameed/whisper-small-Yoruba_newly_trained")
model = Wav2Vec2ForCTC.from_pretrained("DereAbdulhameed/whisper-small-Yoruba_newly_trained")

# Initialize the speech recognition pipeline
speech_recognizer = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor,
    device=0  # Set the appropriate device (GPU) if available
)

def transcribe_audio(audio_path):
    # Load audio file for recognition
    audio_input, _ = torchaudio.load(audio_path)
    
    # Ensure single-channel audio
    if audio_input.shape[0] > 1:
        # Convert stereo to mono by selecting the first channel
        audio_input = audio_input[:1, :]
    
    # Perform speech recognition using the pipeline
    transcription = speech_recognizer(audio_input.squeeze().numpy())
    return transcription

# Example usage: transcribe an audio file
audio_path = "au_audio.wav"
transcription = transcribe_audio(audio_path)
print(transcription)
