import React, { useState } from 'react';

const AudioRecorder = ({ sampleRate }) => {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState('');
  const [showDownloadButton, setShowDownloadButton] = useState(false);

  const startRecording = () => {
    setRecording(true);
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then((stream) => {
        const options = { mimeType: 'audio/webm', audioBitsPerSecond: sampleRate };
        const mediaRecorder = new MediaRecorder(stream, options);
        const chunks = [];
        mediaRecorder.ondataavailable = (e) => {
          chunks.push(e.data);
        };
        mediaRecorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'audio/webm' });
          const url = URL.createObjectURL(blob);
          setAudioBlob(blob);
          setAudioURL(url);
          setShowDownloadButton(true);
        };
        mediaRecorder.start();
        setTimeout(() => {
          mediaRecorder.stop();
          setRecording(false);
        }, 1000); // Recording for 5 seconds, adjust as needed
      })
      .catch((err) => {
        console.error('Error accessing microphone:', err);
      });
  };

  const handleDownloadClick = () => {
    const a = document.createElement('a');
    a.href = audioURL;
    a.download = 'recorded_audio.webm';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div style={{ position: 'relative', color :"black" }}>
        <div>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corrupti, dolorum obcaecati minus beatae repudiandae expedita, deserunt nesciunt sunt exercitationem repellendus voluptatibus dignissimos amet nisi iusto. Assumenda accusamus commodi quasi!</div>

      <button style={{color : "black"}} onClick={startRecording} disabled={recording}>

        {recording ? 'Recording...' : 'Start Recording'}
      </button>
      {audioBlob && (
        <div style={{ position: 'relative' }}>
          <audio controls>
            <source src={audioURL} type="audio/webm" />
            Your browser does not support the audio element.
          </audio>
          {showDownloadButton && (
            <button
              onClick={handleDownloadClick}
              style={{ color:"black",position: 'absolute', bottom: '10px', right: '10px' }}
            >
              Download
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
