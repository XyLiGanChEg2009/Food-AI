import {FC} from "react";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";

import "./KeyItem.css";
import Button from "../../Button/Button";

interface KeyItemProps {
    name: string;
    removeKey: (name: string) => void;
    addKey: (name: string) => void;
    isRemove: boolean;
}

const KeyItem: FC<KeyItemProps> = ({name, removeKey, addKey, isRemove}) => {
    return (
        <li className="chosen_key">
            <span className="chosen_key_name">{name}</span>
            {isRemove ?
                <Button className="chosen_key_remove_button" onClick={() => removeKey(name)}>
                    <FontAwesomeIcon className="chosen_key_icon" icon={faMinus}/>
                </Button>
                :
                <Button className="chosen_key_remove_button" onClick={() => addKey(name)}>
                    <FontAwesomeIcon className="chosen_key_icon" icon={faPlus}/>
                </Button>
            }

        </li>
    );
};

export default KeyItem;