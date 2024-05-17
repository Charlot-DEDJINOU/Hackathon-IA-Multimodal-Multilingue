# models.py
from pydantic import BaseModel


class Texte(BaseModel):
    texte: str

class SectionVideo(BaseModel):
    debut: float
    fin: float
    texte: str

class Video(BaseModel):
    titre: str
    description: str
    fichier_url: str
    
class VideoResponse(BaseModel):
    message: str
    video: Video
