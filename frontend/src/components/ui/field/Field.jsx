import React from "react";
import cn from "classnames";

import "./styles.css";

const Field = ({ children, label = "", error = "", id }) => {
  return (
    <div
      className={cn("form-field", "form__field", {
        "form-field--error": error !== "",
      })}
    >
      {label !== "" && (
        <label className="form-filed__label" htmlFor={id}>
          {label}
        </label>
      )}
      {children}
      {error !== "" && <p className="form-label__error">{error}</p>}
    </div>
  );
};

export default Field;
// _сдсдсдсдсдInput<input type={type} className="input" style={{ width }} {...props} />``,
