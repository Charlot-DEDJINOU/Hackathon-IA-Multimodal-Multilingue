# Video Subtitling API with Node.js and ffmpeg

This API allows you to add subtitles to a video using Node.js as the backend and ffmpeg for video processing.

## Installation

Install dependencies by running `npm install`.

## Configuration

1. Create a `.env` file at the root of the project.
2. Define the following environment variables:
   - `BASE_URL_NODE_SERVER`: The base URL of your Node.js server.
   - `PORT`: The port on which the server listens (default: 3000).

Example `.env` file:

```
BASE_URL_NODE_SERVER=http://localhost
PORT=3000
```

## Usage

1. Start the server using `node serve.js` or `nodemon serve` if you have nodemon installed.
2. The API will be accessible at the URL specified in the `.env` file, for example: `http://localhost:3000`.

## Endpoints

- **POST /addSubtitles**: Endpoint to add subtitles to a video. Requires a video file and subtitles in JSON format.

The response will contain the URL of the video with subtitles.

## Project Structure

- `serve.js`: Entry point of the Express server.
- `uploads/`: Directory where video files are temporarily stored during processing.
- `srt/`: Directory where SRT format subtitle files are stored.
- `public/videos/`: Directory where videos with subtitles are stored for serving to clients.