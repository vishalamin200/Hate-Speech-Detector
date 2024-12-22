import React from "react";
import styles from "./TranscriptText.module.css";

const TranscriptText = ({ audioText }) => {
  return (
    <div className={styles.trans_text}>
      <p className={styles.a_text}>{audioText}</p>
    </div>
  );
};

export default TranscriptText;
