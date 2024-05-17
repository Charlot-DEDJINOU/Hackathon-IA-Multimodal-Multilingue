# schemas.py

from pydantic import BaseModel



class AudioYorubaResponse(BaseModel):
    """le format de retour d'un audio

    Args:
        BaseModel (_type_): _description_
    """
    audio: bytes 
    message: str

    class Config:
        schema_extra = {
            "example": {
                "audio": b"binary_audio_data_here",
                "message": "Audio en Yoruba généré avec succès"
            }
        }

class  AudioYoruba(BaseModel):
    texte: str

class TexteYoruba(BaseModel):
    texte: str


class SectionVideoSchema(BaseModel):
    debut: float
    fin: float
    texte: str
    langue_source: str



class VideoResponse(BaseModel):
    message: str
    # Type dict pour représenter les données de la vidéo
    video: dict  


class TranscriptResponse(BaseModel):
    transcript : str
    
class SubtitleItem(BaseModel):
    debut: str
    fin: str
    text: str
