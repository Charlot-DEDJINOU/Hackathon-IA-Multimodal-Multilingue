# app.py
from database import connect_to_mongodb
from fastapi import FastAPI
from routes import router
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    mongogb= await connect_to_mongodb(os.getenv("DATABASE_NAME"))
    print("Connexion à MongoDB établie")
    

# Inclusion des routes définies dans routes.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.185.64", port=8000)
