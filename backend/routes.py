# routes.py
from typing import List
from fastapi import APIRouter, UploadFile, File
from models import Texte
from fastapi import APIRouter, HTTPException, status
import os
from dotenv import load_dotenv
from database import connect_to_mongodb
from services import ( traduire_vers_yoruba, 
                    generer_audio_yoruba, 
                    transcrire_srt_to_yoruba, 
                    generate_subtitled_video,
                    transcribe_yoruba_video,
                    transcribe_srt,
                    json_to_srt,
                    transcribe
        )
from schemas import TexteYoruba, AudioYorubaResponse, SectionVideoSchema
import assemblyai as aai
from fastapi import  HTTPException

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

aai.settings.api_key = os.getenv("API_KEY")


router = APIRouter()

# Route pour tester la connexion à MongoDB
@router.get("/test-mongodb")
async def test_mongodb_connection():
    try:
        collection_name = "ma_collection"  # Nom de votre collection
        mongodb = await connect_to_mongodb()  # Attendre la connexion à MongoDB
        collection = mongodb[collection_name]  # Accéder à la collection MongoDB
        count = await collection.count_documents({})
        return {"message": f"Connexion à MongoDB réussie, nombre de documents dans la collection : {count}"}
    
    except Exception as e:
        return {"message": f"Erreur lors de la connexion à MongoDB : {str(e)}"}


@router.post("/to-yoruba", response_model=TexteYoruba)
async def traduire_texte_vers_yoruba(texte: Texte):
    texte_yoruba = await traduire_vers_yoruba(texte.texte)
    
    if texte_yoruba is not None:
        return TexteYoruba(texte=texte_yoruba)
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Une erreur s'est produite lors de la traduction"
    )



@router.post("/to-audio-yoruba", response_model=AudioYorubaResponse)
async def generer_audio_yoruba_from_texte(texte_yoruba: Texte):
    audio =  await generer_audio_yoruba(texte_yoruba.texte)
    
    if audio is not None:
        return audio
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Une erreur s'est produite lors de la lecture du texte"
    )



@router.post("/extraire-sections-video", response_model=List[SectionVideoSchema])
async def extraire_sections_video(langue_source: str, video_url: str):
    # Votre logique d'extraction de sections vidéo ici
    sections_video = []  # Liste de SectionVideoSchema
    return sections_video













#--------------------------  #################################################
# Route pour uploader une vidéo
@router.post("/transcribe-yoruba", response_model=dict)
async def transcribe_video_to_yoruba(video_file: UploadFile = File(...)):
    if video_file.filename.endswith(".mp4") or video_file.filename.endswith(".mov"):
        
        # Lire le contenu du fichier vidéo
        file = await video_file.read()
        try:
        
            mongodb = await connect_to_mongodb()  # Connexion à MongoDB
            url = f"static/{video_file.filename}"
            
            # Sauvegarde des métadonnées de la vidéo dans la base de données
            data = {
                "fichier_url": url
            }
            
            inserted_video = await mongodb.videos.insert_one(data)
            
            print(inserted_video)
        
            with open(url, "wb") as video_file:
                video_file.write(file)

            # Transcrire la vidéo avec AssemblyAI
            # config = aai.TranscriptionConfig(language_detection=True)
            # transcriber = aai.Transcriber()
            
            # transcript = transcriber.transcribe(file, config=config)

            # if transcript.status == aai.TranscriptStatus.error:
            #     return {"error": transcript.error}
            # else:
            #     # Exporter la transcription au format SRT
            #     subtitles_srt = await transcrire_srt_to_yoruba(transcript.export_subtitles_srt())
            segments_fr = transcribe(url)
            segments = await transcrire_srt_to_yoruba(segments_fr)
                
            return {
                "message": "Vidéo enregistrée avec succès",
                "video": segments ,
                "url" : url,
                
            }

        except Exception as e:
            return {
                "message": f"Erreur lors de l'enregistrement de la vidéo : {str(e)}"
            }

    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="erreur"
    )

    
    
    
############################################################################################""

# Route pour uploader une vidéo
@router.post("/subtitles")
async def generate_subtitled_video_international_language(video_file: UploadFile = File(...)):
    if video_file.filename.endswith(".mp4") or video_file.filename.endswith(".mov"):
        # Lire le contenu du fichier vidéo
        file = await video_file.read()
        try:
        
            mongodb = await connect_to_mongodb()  # Connexion à MongoDB
            url = f"static/{video_file.filename}"
            output_url = f"static/output-{video_file.filename}"
            
            # Sauvegarde des métadonnées de la vidéo dans la base de données
            data = {
                "fichier_url": url
            }
            
            inserted_video = await mongodb.videos.insert_one(data)
            
            print(inserted_video)
        
            with open(url, "wb") as video_file:
                video_file.write(file)
                
            srt_file = transcribe_srt(url)
            
            # with open(srt_file, "wb") as video_file:
            #     video_file.write(file)
                
                
            return generate_subtitled_video(url, output_url, subtitle_file=srt_file)

        except Exception as e:
            return {
                "message": f"Erreur lors de l'enregistrement de la vidéo : {str(e)}"
            }

    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="erreur"
    )


###########################################  SUBTITUTE  ################################
@router.post("/subtitute")
async def transcribe_video_to_yoruba(video_file: UploadFile = File(...)):
    if video_file.filename.endswith(".mp4") or video_file.filename.endswith(".mov"):
        
    
        # Lire le contenu du fichier vidéo
        subtitles_file = f"static/subtitle-{video_file.filename}.srt"
        output_url = f"static/output-yoruba{video_file.filename}"
        file = await video_file.read()
        url = f"static/{video_file.filename}"
        try:
        
            mongodb = await connect_to_mongodb()  # Connexion à MongoDB
        
            
            # Sauvegarde des métadonnées de la vidéo dans la base de données
            data = {
                "fichier_url": url
            }
            
            inserted_video = await mongodb.videos.insert_one(data)
            
            print(inserted_video)
            print("loading...")
        
            with open(url, "wb") as video_file:
                video_file.write(file)

            # Transcrire la vidéo avec AssemblyAI
            # config = aai.TranscriptionConfig(language_detection=True)
            # transcriber = aai.Transcriber()
            # transcript = transcriber.transcribe(file, config=config)

            # if transcript.status == aai.TranscriptStatus.error:
            #     return {"error": transcript.error}
            # else:
            #     transcibe_text = transcript.export_subtitles_srt()
                
            
            # Exporter la transcription au format SRT
            segments_fr = transcribe(url)
            segments = await transcrire_srt_to_yoruba(segments_fr)
            subtitles_srt = await transcrire_srt_to_yoruba(segments)
            print("texxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxt",subtitles_srt)
            output_file_path = json_to_srt(subtitles_srt, subtitles_file)
                
                
            audio = await generer_audio_yoruba(segments=subtitles_srt, video_path=url)
            
            if audio is not None:
                
                return generate_subtitled_video(audio["url_video"], output_url, subtitle_file=output_file_path)
            
        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="erreur !!!!!!!!!!"
            )
            

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Erreur lors de génération de l'audio : {str(e)}"
            )
            

    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="erreur"
    )


@router.post("/transcribe-from-yoruba/")
async def transcribe_video_from_yoruba(video_file: UploadFile = File(...)):
    # Fichier vidéo reçu en entrée depuis la requête POST
    # Enregistrer le fichier vidéo temporairement
    video_path = f"temp/{video_file.filename}"
    with open(video_path, "wb") as f:
        f.write(video_file.file.read())
    
    # Appeler la fonction pour transcrire la vidéo
    subtitles = transcribe_yoruba_video(video_path)
    
    return subtitles