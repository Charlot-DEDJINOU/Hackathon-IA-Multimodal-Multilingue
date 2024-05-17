const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');
const multer = require('multer');

require('dotenv').config();

const app = express();
const port = process.env.PORT;

const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
ffmpeg.setFfmpegPath(ffmpegPath);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage }).single('video_file');

function generateSRT(subtitles) {
    let srtContent = '';
    let sequenceNumber = 1;

    subtitles.video.forEach((subtitle) => {
        const startTime = subtitle.debut.replace(',', '.');
        const endTime = subtitle.fin.replace(',', '.');

        srtContent += `${sequenceNumber}\n`;
        srtContent += `${startTime} --> ${endTime}\n`;
        srtContent += `${subtitle.text}\n\n`;

        sequenceNumber++;
    });

    return srtContent;
}

function createSRTFile(subtitles) {
    const srtContent = generateSRT(subtitles);
    const filePath = `./srt/subtitles_${Date.now()}.srt`;

    fs.writeFileSync(filePath, srtContent);
    return filePath;
}

function addSubtitles(videoPath, subtitlesPath, outputDir) {
    return new Promise((resolve, reject) => {
        const outputFileName = 'moviewithsubtitle.mp4';
        const outputPath = path.join(outputDir, outputFileName);

        ffmpeg(videoPath)
            .videoCodec('libx264')
            .audioCodec('libmp3lame')
            .outputOptions(`-vf subtitles=${subtitlesPath}:force_style='Bold=3,FontSize=25,OutlineColour=&H00000000,BackColour=&H00000000'`)
            .on('error', (err) => reject(err))
            .on('end', () => resolve(outputPath))
            .save(outputPath);
    });
}

app.post('/addSubtitles', upload, async (req, res) => {
    const { data } = req.body;
    
    if (!req.file || !data) {
        return res.status(400).json({ error: 'Veuillez fournir la vidéo et les sous-titres.' });
    }

    const subtitles = createSRTFile(JSON.parse(data));
    const outputDir = path.join(__dirname, 'public/videos'); // Définir le répertoire de sortie pour la vidéo sous-titrée

    try {
        const videoWithSubtitles = await addSubtitles(req.file.path, subtitles, outputDir);

        // Envoyer l'URL de la vidéo avec sous-titres au frontend
        const videoUrl = `${process.env.BASE_URL_NODE_SERVER}:${port}/videos/${path.basename(videoWithSubtitles)}`;
        res.json({ videoUrl });
    } catch (error) {
        console.error('Erreur lors de l\'ajout des sous-titres:', error);
        res.status(500).json({ error: 'Erreur lors de l\'ajout des sous-titres.' });
    }
});

app.use('/videos', express.static(path.join(__dirname, 'public/videos')));

app.listen(port, () => {
    console.log(`Serveur démarré sur le port ${port}`);
});