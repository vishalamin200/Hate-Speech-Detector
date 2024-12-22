import { useState } from "react";
import axios from "axios";
import styles from "./App.module.css";

import Modal from "./components/Modal/Modal";
import Mic from "./components/Mic/Mic";
import TextArea from "./components/TextArea/TextArea";
import TranscriptText from "./components/TranscriptText/TranscriptText";

function App() {
  const [audioText, setAudioText] = useState("");
  const [lang, setLang] = useState([]);
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [listening, setListening] = useState(false);

  let recognition = null;

  const startListening = () => {
    // If already listening, stop listening
    if (listening && recognition) {
      recognition.stop();
      setListening(false);
    } else {
      // Start listening
      setListening(true);
      recognition = new window.webkitSpeechRecognition();

      // default value
      recognition.lang = "en-US";

      if (lang.length > 0) {
        recognition.lang = lang[0].value;
      }

      recognition.onresult = (event) => {
        const result = event.results[event.results.length - 1];
        const text = result[0].transcript;

        setAudioText(text);
      };

      recognition.onerror = (error) => {
        console.error("Speech recognition error:", error);
        setListening(false);
      };

      recognition.onend = () => {
        setListening(false);
      };

      // Start the recognition
      recognition.start();
    }
  };

  const getResult = async () => {
    let data;
    if (audioText.length > 0) {
      data = audioText;
    } else if (text.length > 0) {
      data = text;
    } else {
      data = "";
    }
    let language;
    if (lang.length > 0) {
      language = lang[0].value;
    } else {
      language = "en-US";
    }

    try {
      const response = await axios.post("/hate", {
        initial_state: data,
        lang: language,
      });
      console.log(response);
      setResult(response.data.vibe);
    } catch (error) {
      console.log(error.message);
    }
  };

  const cleanSlate = () => {
    setAudioText("");
    setLang([]);
    setText("");
    setResult("");
    setListening(false);
  };

  return (
    <div className={styles.App}>
      {result.length !== 0 && (
        <div className={styles.modal_container} onClick={() => cleanSlate()}>
          <Modal answer={result} />
        </div>
      )}

      <div className={styles.main}>
        <p className={styles.heading}>Hate Speech Recognition</p>
        <div className={styles.input_div}>
          <Mic
            listening={listening}
            startListening={startListening}
            setLang={setLang}
          />
          <p className={styles.choose}>OR</p>
          <TextArea setText={setText} text={text} />
        </div>
        {audioText.length !== 0 && <TranscriptText audioText={audioText} />}
        <div className={styles.submit} onClick={() => getResult()}>
          <p className={styles.submit_text}>Find out!</p>
        </div>
      </div>
    </div>
  );
}

export default App;

// 8E7AB5
// B784B7
// E493B3
// EEA5A6
