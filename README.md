
# SMART VT - Video Translator and Dubber

SMART VT is an application designed to subtitle and dub any video, regardless of its original language, into a language of your choice. The project leverages a React frontend, Python APIs for video processing, and Node.js for handling video subtitles.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Node.js API Setup](#nodejs-api-setup)
6. [Usage](#usage)
7. [Conclusion](#conclusion)

## Prerequisites

- Python 3.x
- Node.js
- Git
- npm (Node Package Manager)
- Stable internet connection

## Project Structure

The project is structured into three main parts:

- **Backend**: Handles video processing with Python.
- **Frontend**: React application for user interaction.
- **Node.js API**: Manages video subtitle addition using ffmpeg.

## Backend Setup

### 1. Clone the Project

```bash
git clone https://github.com/Charlot-DEDJINOU/Hackathon-IA-Multimodal-Multilingue
```

### 2. Configure the Virtual Environment

Navigate to the `backend` directory and set up the Python environment:

```bash
cd backend
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
MONGO_URI=mongodb+srv://username:password@dbname.id.mongodb.net/
DATABASE_NAME=your_dbname
API_KEY="api key for assembly ai" ## Optional
BASE_URL=your_base_url ## For example: http://127.0.0.1:8000/
```

### 4. Start the FastAPI Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Frontend Setup

### 1. Navigate to the Frontend Directory

```bash
cd ../frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Environment Variables

Create a `.env` file in the `frontend` directory with the following content:

```env
VITE_APP_API_PYTHON_URL="http://192.168.18.64:8000"
VITE_APP_API_NODE_URL="http://localhost:3000"
```

### 4. Start the Development Server

```bash
npm run dev
```

Open your browser and visit `http://localhost:3000` to view the application.

## Node.js API Setup

### 1. Navigate to the Node Directory

```bash
cd ../node
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Environment Variables

Create a `.env` file in the `node` directory with the following content:

```env
BASE_URL_NODE_SERVER=http://localhost
PORT=3000
```

### 4. Start the Node.js Server

```bash
node serve.js
```

The API will be accessible at the URL specified in the `.env` file, for example: `http://localhost:3000`.

## Usage

1. **Upload a Video**: Open the frontend application and upload a video.
2. **Choose Translation/Dubbing Options**: Select your desired translation and dubbing options, and choose the destination language.
3. **Process the Video**: Click on "Charger la vidéo" to process the video. The backend and Node.js API will handle the video processing and subtitle addition.

## Conclusion

Your SMART VT application should now be fully operational. If you encounter any issues or have questions, feel free to consult the documentation or open an issue on the GitHub repository.
