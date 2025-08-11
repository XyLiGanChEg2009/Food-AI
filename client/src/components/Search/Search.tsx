import React, {ChangeEvent, FC, useState} from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSearch} from "@fortawesome/free-solid-svg-icons";

import {useAppDispatch} from "../../hooks/redux";
import {fetchProducts} from "../../store/reducers/ActionCreators";

import Button from "../Button/Button";

import "./Search.css";


const Search: FC = () => {
    const dispatch = useAppDispatch();

    const [query, setQuery] = useState<string>("");
    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    const keyDownHandler = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.code === "Enter") {
            dispatch(fetchProducts(query));
        }
    }
    
    return (
        <div className="search_container">
            <input onKeyDown={(e) => keyDownHandler(e)} className="search_input" type="text" placeholder="Поиск..." onChange={(event) => handleInputChange(event)}/>
            <Button className={"search_button"} onClick={() => dispatch(fetchProducts(query))}>
                <FontAwesomeIcon icon={faSearch}/>
            </Button>
        </div>
    );
}

export default Search; 