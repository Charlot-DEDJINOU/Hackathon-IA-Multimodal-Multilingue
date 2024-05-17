export function generateSRT(subtitles) {
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