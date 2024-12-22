import React from "react";
import styles from "./Modal.module.css";

const Modal = ({ answer }) => {
  let content;
  let color;
  switch (answer) {
    case "Hate Speech":
      content = "Damn You're A Hater!!";
      color = "red";
      break;
    case "Offensive Language":
      content = "That's Really Offensive!!";
      color = "purple";
      break;
    case "No Hate and Offensive":
      content = "You're Cool!!";
      color = "green";
      break;
    default:
      content = "No Idea";
      color = "grey";
  }
  return (
    <div className={`${styles.modal} ${styles[color]}`}>
      <p className={styles.modal_text}>{content}</p>
    </div>
  );
};

export default Modal;
