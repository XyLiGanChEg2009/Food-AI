import React, { ChangeEvent, FC } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSearch} from "@fortawesome/free-solid-svg-icons";

import Button from "../Button/Button";

import "./Search.css";

type SearchProps = {
    handleInputChange: (event: ChangeEvent<HTMLInputElement>) => void;
    fetchProducts: () => void
}

const Search: FC<SearchProps> = ({handleInputChange, fetchProducts}) => {
    const keyDownHandler = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.code === "Enter") {
            fetchProducts();
        }
    }
    
    return (
        <div className="search_container">
            <input onKeyDown={(e) => keyDownHandler(e)} className="search_input" type="text" placeholder="Поиск..." onChange={(event) => handleInputChange(event)}/>
            <Button className={"search_button"} onClick={fetchProducts}>
                <FontAwesomeIcon icon={faSearch}/>
            </Button>
        </div>
    );
}

export default Search; 