import classnames from "classnames";

import "./style.css";

const Button = ({ children, className, ...props }) => {
  return (
    <button
      className={classnames("button", className)}
      type="button"
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
