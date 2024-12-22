import React from "react";

import styles from "./TextArea.module.css";

const TextArea = ({ text, setText }) => {
  return (
    <div className={styles.text_box}>
      <textarea
        className={styles.text}
        // rows={10}
        // cols={30}
        placeholder="Enter text..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
    </div>
  );
};

export default TextArea;
