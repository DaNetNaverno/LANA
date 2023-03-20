import React from "react";
import { forwardRef } from "react";
import "./styles.css";

const Input = ({ type = "text", width = "100%", ...props }, ref) => {
  return (
    <input
      ref={ref}
      type={type}
      className="input"
      style={{ width }}
      {...props}
    />
  );
};

export default forwardRef(Input);
// _сдсдсдсдсд
