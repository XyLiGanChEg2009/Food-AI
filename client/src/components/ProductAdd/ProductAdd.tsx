import {ChangeEvent, useContext, useState} from "react";
import Button from "../Button/Button";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faPlus} from "@fortawesome/free-solid-svg-icons";

import {ServerContext} from "../../App";

import "./ProductAdd.css";
import {Product, Response} from "../../types";

const ProductAdd = () => {
    const server = useContext(ServerContext);

    const [modalIsOpen, setModalIsOpen] = useState<boolean>(false);
    const [product, setProduct] = useState<Product>(
        {name: "", img_src: "", weight: 250, price: 500}
    );
    const [responseMessage, setResponseMessage] = useState<string>("");

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        const id = event.target.id;
        setProduct(prevState => {
            if (id === "weight" || id === "price") {
                return {...prevState, [id]: Number(event.target.value)};
            }
            return {...prevState, [id]: event.target.value};
        });
    };

    const fetchAddProduct = async () => {
        setResponseMessage("");
        const response: Response = await server.addProduct(product);
        setResponseMessage(response.status === "ok" ? "Product added" : "Product add error");
    }

    return (
        <div>
            <div className="product_add_container">
                <Button className="product_add_open_button" onClick={() => setModalIsOpen(!modalIsOpen)}>
                    <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon>
                </Button>
            </div>

            <div className={"product_add_form " + (modalIsOpen ? "product_add_form_open" : "")}>
                <input onChange={(event) => handleInputChange(event)} id="name" placeholder="name"
                       className="product_add_form_input" type="text"/>
                <input onChange={(event) => handleInputChange(event)} id="img_src" placeholder="img_src"
                       className="product_add_form_input" type="text"/>
                <input onChange={(event) => handleInputChange(event)} id="weight" placeholder="weight"
                       className="product_add_form_input" type="text"/>
                <input onChange={(event) => handleInputChange(event)} id="price" placeholder="price"
                       className="product_add_form_input" type="text"/>
                {/*<input onChange={(event) => handleInputChange(event)} id="keys" placeholder="keys"*/}
                {/*       className="product_add_form_input" type="text"/>*/}
                <Button className="product_add_form_push_button" onClick={() => fetchAddProduct()}>
                    <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon>
                </Button>
                {modalIsOpen && <span className={responseMessage === "Product add error" ? "responseError" : "responseSuccess"}>{responseMessage}</span>}
            </div>

        </div>
    );
};

export default ProductAdd;