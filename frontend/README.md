# SMART VT - Video Translator and Dubber

SMART VT is a React application designed to subtitle and dub any video regardless of its original language into a language of your choice. It utilizes Python and Node.js APIs for video processing.

## Installation

```bash
npm install
```

Of course, here's an additional section to include information about the `.env` file in your README:

---

## Environment Configuration

The `.env` file is used to store sensitive environment variables necessary for the proper functioning of the application. Make sure to create a `.env` file at the root of the project and include the following variables:

```plaintext
VITE_APP_API_PYTHON_URL = "http://192.168.18.64:8000"
VITE_APP_API_NODE_URL = "http://localhost:3000"
```

- `VITE_APP_API_PYTHON_URL`: The URL of the Python API used for video processing.
- `VITE_APP_API_NODE_URL`: The URL of the Node.js API used for the server-side services of the React application.

Make sure these URLs correspond to the actual addresses of your Python and Node.js APIs.

## Usage

1. Start the development server:

```bash
npm run dev
```

2. Open your browser and visit [http://localhost:3000](http://localhost:3000) to view the application.

3. Upload a video, choose your translation/dubbing options and destination language, then click on "Charger la vidéo" to process the video.