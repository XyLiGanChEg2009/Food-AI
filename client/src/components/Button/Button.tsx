import {FC, ReactNode} from "react";

import "./Button.css";

type ButtonProps = {
    className: string;
    onClick: () => void;
    children: ReactNode
}

const Button: FC<ButtonProps> = ({className, onClick, children}) => {
    return (  
        <button className={"default_button " + className} onClick={() => onClick()}>{children}</button>
    );
}

export default Button;