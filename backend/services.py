# services.py
from deep_translator import GoogleTranslator
from schemas import TexteYoruba, AudioYorubaResponse, SubtitleItem
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from huggingface_hub import hf_hub_download
import torch
from functools import lru_cache
import ffmpeg
# from IPython.display import Audio
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
import assemblyai as aai
from dotenv import load_dotenv
import os
import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from datetime import datetime
import soundfile as sf
from pydub import AudioSegment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# Initialize the model and processor and cache them



load_dotenv()

aai.settings.api_key = os.getenv("API_KEY")


BASE_URL = os.getenv("BASE_URL")





@lru_cache
def charger_modele():
    processor = SpeechT5Processor.from_pretrained("imhotepai/yoruba-tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("imhotepai/yoruba-tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    dir_ = hf_hub_download(repo_id="imhotepai/yoruba-tts", filename="speaker_embeddings.pt")
    speaker_embeddings = torch.load(dir_)
    return processor, model, vocoder, speaker_embeddings


@lru_cache
def load_speech_model():
    processor = Wav2Vec2Processor.from_pretrained("steja/whisper-small-yoruba")
    model = Wav2Vec2ForCTC.from_pretrained("steja/whisper-small-yoruba")
    return processor, model


async def traduire_vers_yoruba(texte: str) -> str:
    """traduire du texte de n'importe quelle source international vers yoruba

    Args:
        texte (Texte): le texte de la source

    Returns:
        str: Si tout se passe bien le texte yoruba est retourné
    """
    
    try:
        translator = GoogleTranslator(source='auto', target='yo')
        traduction = translator.translate(texte)
        print(texte, "###===>", traduction)
        return traduction
    except Exception as e:
        print("Une erreur s'est produite lors de la traduction :", e)
        return None
    

def json_to_srt(data, output_file_path):
    srt_content = []
    for index, item in enumerate(data, start=1):
        srt_content.append(f"{index}")
        srt_content.append(f"{item['debut']} --> {item['fin']}")
        srt_content.append(f"{item['text']}\n")

    with open(output_file_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write("\n".join(srt_content))

    return output_file_path


def transcribe_srt(file):
    config = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        print({"error": transcript.error})
    else:
        # Exporter la transcription au format SRT
        subtitles_srt = transcript.export_subtitles_srt()

        with open("static/subtitle-yo.srt", "w") as f:
            f.write(subtitles_srt)
    return "static/subtitle-yo.srt"


async def generer_audio_yoruba(texte: str) -> AudioYorubaResponse:
    try:
        texte_yoruba = await traduire_vers_yoruba(texte)
        
        print("le texte yoruba ====================================>", texte_yoruba)
        processor, model, vocoder, speaker_embeddings = charger_modele()

        inputs = processor(text=texte_yoruba, return_tensors="pt")
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

        # Convertir l'audio en bytes
        audio_yoruba = speech.numpy()

        # Convertir l'audio en base64
        audio_base64 = base64.b64encode(audio_yoruba).decode('utf-8')
        
        return AudioYorubaResponse(audio=audio_base64, message="Audio en Yoruba généré avec succès")
    
    
    except Exception as e:
        print(f"une erreur s'est produite lors de la génération d'audio {e}")
        return None




async def transcribe_video(file: UploadFile):
    try:
        # Enregistrer le fichier vidéo temporairement
        with open(file.filename, "wb") as video_file:
            video_file.write(await file.read())

        # Transcrire la vidéo avec AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file.filename)

        if transcript.status == aai.TranscriptStatus.error:
            return {"error": transcript.error}
        else:
            # Exporter la transcription au format SRT
            subtitles_srt = transcript.export_subtitles_srt()
            return subtitles_srt

    except Exception as e:
        return {"error": str(e)}
    
async def transcrire_srt_to_yoruba(segments):
    
    yoruba_segments = []
    for segment in segments:
        
        # Traduire le texte en yoruba
        texte_yoruba = await traduire_vers_yoruba(segment["text"])
        
        # Créer un objet de sous-titre avec les informations
        subtitle = {
            "debut": segment["debut"],
            "fin": segment["fin"],
            "text": texte_yoruba
        }
        
        yoruba_segments.append(subtitle)
        # Ajouter l'objet de sous-titre à la liste des sous-titres
        

    return yoruba_segments




def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def time_to_milliseconds(time_str):
    h, m, s = time_str.split(':')
    seconds, milliseconds = s.split(',')
    return int(h) * 3600000 + int(m) * 60000 + int(seconds) * 1000 + int(milliseconds)




def create_subtitle_clips(subtitles, videosize,fontsize=24, font='Arial', color='yellow', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize
        
        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height* 4 / 5 

        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips


def subtitle_video(filename, subtitles):
    
    video = VideoFileClip(filename)
    begin, end= filename.split(".mp4")
    output_video_file = begin+'_subtitled'+".mp4"

    print ("Output file name: ", output_video_file)

    # Create subtitle clips
    subtitle_clips = create_subtitle_clips(subtitles,video.size)

    # Add subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)

    # Write output video file
    final_video.write_videofile(output_video_file)
    
    return output_video_file
    
    
    

def generate_subtitled_video(video_file, output_video, subtitle_file, soft_subtitle = False, subtitle_language="yo"):
    try:
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
            
            return {
                "url_output": BASE_URL + output_video,
                "message": f"Subtitles added successfully to {output_video}"
            } 
        except ffmpeg.Error as e:
            return {
                "error" : f"An error occurred: {e}"
            }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la vidéo sous-titrée: {str(e)}")


def time_to_mili_seconds(time_str):
    hours, minutes, seconds = map(float, time_str.split(':'))
    seconds += hours * 3600 + minutes * 60
    return seconds * 1000



########## GENERATE video yoruba from international languages

async def generer_audio_yoruba(segments: dict, video_path):
    
    try:
        
        video_clip = VideoFileClip(video_path)
        original_audio_clip = video_clip.audio
        
        duration = original_audio_clip.duration
        # Charger le modèle et générer l'audio en Yoruba
        processor, model, vocoder, speaker_embeddings = charger_modele()
        start_ms = time_to_milliseconds(segments[0]["debut"])
        combined_audio = AudioSegment.silent(duration=(start_ms + 200))  # Créer un segment audio vide
        
        for segment in segments:
            text = segment["text"]
            inputs = processor(text=text, return_tensors="pt")
            audio_data = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

            # Convertir l'audio en numpy array
            audio_np = audio_data.numpy()

            # Calculer la durée nécessaire pour le segment
            start_ms = time_to_milliseconds(segment["debut"])
            end_ms = time_to_milliseconds(segment["fin"])
            duration_ms = end_ms - start_ms  # Durée nécessaire en millisecondes

            # Enregistrer l'audio dans un fichier WAV temporaire
            temp_filename = f"temp_audio.wav"
            sf.write(temp_filename, audio_np, samplerate=16050)  # Assurez-vous que samplerate correspond à votre modèle

            # Charger l'audio à partir du fichier WAV avec la durée spécifiée
            segment_audio = AudioSegment.from_file(temp_filename, format="wav")

            # Limiter la durée du segment audio à la durée spécifiée
            second_to_add = 100
            
            if len(segment_audio) < duration_ms:
                second_to_add += (duration_ms - len(segment_audio))
                
            
            segment_audio = segment_audio + AudioSegment.silent(duration=second_to_add)

            # Assembler le segment audio dans l'audio combiné
            
            combined_audio = combined_audio + segment_audio   # Ajouter un silence entre les segments

            # Supprimer le fichier WAV temporaire
            os.remove(temp_filename)
            
        end_ms = duration - time_to_milliseconds(segments[-1]["fin"])
        combined_audio = combined_audio + 6 + AudioSegment.silent(duration=(end_ms + 4000))
        combined_audio = combined_audio + 6
        combined_audio.export("output_combined_audio.wav", format="wav")
        # Convertir l'audio généré en bytes et ensuite en base64
        
        
        
        output_wav_file = "output_combined_audio.wav"
        
        
        # Charger l'audio généré en Yoruba à partir de base64
        audio_yoruba_clip = AudioFileClip(output_wav_file)
        # Ajuster la taille de l'audio généré pour correspondre à la durée de l'audio original
        audio_yoruba_clip = audio_yoruba_clip.set_duration(original_audio_clip.duration)
        
        # Substituer l'audio original par l'audio généré en Yoruba
        video_clip_with_substituted_audio = video_clip.set_audio(audio_yoruba_clip)
        
        # Enregistrer la vidéo finale avec l'audio substitué
        output_video_path =  "static/video_generated_yoruba.mp4"
        video_clip_with_substituted_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        
        return {'message':"Audio en Yoruba généré et substitué avec succès" , 'url_video' : output_video_path}
    
    except Exception as e:
        print(f"Une erreur s'est produite lors de la génération d'audio en Yoruba : {e}")
        return None
    
    
    
    
import moviepy.editor as mp
import speech_recognition as sr

def transcribe_yoruba_video(video_path):
    # Extraction de l'audio depuis la vidéo
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp/audio.wav"
    audio.write_audiofile(audio_path)
    
    return transcribe_yoruba_audio(audio_path=audio_path)
    
    # # Transcription de l'audio en texte (Yoruba)
    # recognizer = sr.Recognizer()
    # with sr.AudioFile(audio_path) as source:
    #     audio_data = recognizer.record(source)
    
    # try:
    #     transcription = recognizer.recognize_google(audio_data, language='yo-NG')
    # except sr.UnknownValueError:
    #     transcription = "Échec de la transcription"
    
    # # Formatage des sous-titres dans le format spécifié
    # subtitles = []
    # start_time = 0
    # lines = transcription.split('\n')
    
    # for line in lines:
    #     if line.strip():
    #         words_count = len(line.split())
    #         duration_seconds = words_count / 3.0
    #         end_time = start_time + duration_seconds
            
    #         subtitles.append({
    #             "debut": format_time(start_time),
    #             "fin": format_time(end_time),
    #             "text": line
    #         })
            
    #         start_time = end_time + 1
    
    # return subtitles

def transcribe_yoruba_audio(audio_path):
    import torchaudio
    
    processor, model = load_speech_model()

    # Load audio file for recognition
    audio_input, _ = torchaudio.load(audio_path)
    
    # Preprocess the audio input for the model
    inputs = processor(
        audio_input.numpy().squeeze(), 
        return_tensors="pt", 
        padding="longest", 
        # truncation=True
    )

    # Perform Yoruba speech recognition using the model
    with torch.no_grad():
        logits = model(inputs.input_values.to(model.device)).logits
    
    # Decode the output using the processor
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    
    # Format the transcription into SRT-style subtitles
    subtitles = []
    start_time = 0
    for text in transcription:
        if text.strip():
            words_count = len(text.split())
            duration_seconds = words_count / 3.0
            end_time = start_time + duration_seconds
            
            subtitles.append({
                "debut": format_time(start_time),
                "fin": format_time(end_time),
                "text": text
            })
            
            start_time = end_time + 1
    
    return subtitles


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"



from faster_whisper import WhisperModel

def extract_audio(video_path):
    extracted_audio = f"audio-temp.wav"
    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(video_path):
    audio_path = extract_audio(video_path)
    model = WhisperModel("small")
    segments, info = model.transcribe(audio_path)
    list_segments = []
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
            (segment.start, segment.end, segment.text))
        list_segments.append(
            {
                "debut": format_time(segment.start),
                "fin": format_time(segment.end),
                "text": segment.text
            }
        )
    return list_segments


def generate_subtitle_file(segments, subtitle_file):

    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file
