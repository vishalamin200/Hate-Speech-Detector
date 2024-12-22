import React from "react";
import Select from "react-dropdown-select";
import styles from "./Mic.module.css";

import mic_green from "../../assets/microphone-green.svg";

const Mic = ({ listening, startListening, setLang }) => {
  const options = [
    {
      value: "hi-IN",
      label: "Hindi",
    },
    {
      value: "en-US",
      label: "English",
    },
  ];
  return (
    <div className={styles.mic}>
      <img
        className={`${styles.mic_img} ${
          listening ? styles.clicked : styles.bnw
        }`}
        src={mic_green}
        alt="Microphone On"
        onClick={() => startListening()}
      />
      <p className={styles.mic_text}>Click to record audio.</p>
      <Select
        options={options}
        onChange={(val) => setLang(val)}
        placeholder="Select Language"
        searchable={true}
      />
    </div>
  );
};

export default Mic;
