import {ChangeEvent, useContext, useState} from "react";
import Button from "../Button/Button";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faPlus} from "@fortawesome/free-solid-svg-icons";

import {ServerContext} from "../../App";

import "./ProductAdd.css";
import {Product, Response} from "../../types";
import List from "../List/List";
import KeyItem from "./KeyItem/KeyItem";


const ProductAdd = () => {
    const server = useContext(ServerContext);

    const [keys, setKeys] = useState<string[]>(['авторская_кухня', 'азиатская_кухня', 'алкогольные', 'без_лактозы', 'без_сахара', 'безалкогольные', 'безглютеновое', 'бизнес_ланч', 'бургеры', 'быстрое_питание', 'веганское', 'вегетарианское', 'вино', 'восточная_кухня', 'выпечка', 'гарниры', 'горячее', 'горячие_блюда', 'гриль', 'деликатесы', 'десерты', 'детское_меню', 'диабетическое', 'диетическое', 'для_вечеринки', 'для_компании', 'для_одного', 'для_пикника', 'европейская_кухня', 'еда_на_вынос', 'жареное', 'завтрак', 'закуски', 'запеченое', 'здоровая_еда', 'зерновые', 'испанская_кухня', 'итальянская_кухня', 'к_фильму', 'калорийное', 'китайская_кухня', 'комфортная_еда', 'кофе', 'курица', 'лапша', 'легкое', 'лимонады', 'мексиканская_кухня', 'морепродукты', 'мороженое', 'мясное', 'на_работу', 'напитки', 'обед', 'овощи', 'освежающее', 'основные_блюда', 'острое', 'паста', 'перекус', 'пирогидесерты', 'пицца', 'попкорн', 'праздничное', 'рис', 'роллы', 'романтическое', 'русская_кухня', 'рыба', 'салаты', 'свежевыжатые_соки', 'сладкое', 'смузи', 'снеки', 'соки', 'соленое', 'соусы', 'стейк', 'супы', 'суши', 'сыр', 'сытное', 'сэндвичи', 'терраса', 'торты', 'тушеное', 'ужин', 'фастфуд', 'фрукты', 'холодное', 'чай', 'шоколад', 'японская_кухня']);

    const [modalIsOpen, setModalIsOpen] = useState<boolean>(false);
    const [product, setProduct] = useState<Product>(
        {name: "", img_src: "", weight: 0, price: 0, keys: []}
    );
    const [responseMessage, setResponseMessage] = useState<string>("");

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        const id = event.target.id;
        setProduct(prevState => {
            if (id === "keys") {
                return {...prevState, [id]: event.target.value.split(" ")};
            }
            if (id === "weight" || id === "price") {
                return {...prevState, [id]: Number(event.target.value)};
            }
            return {...prevState, [id]: event.target.value};
        });
    };

    const fetchAddProduct = async () => {
        if (!product.name || !product.img_src || !product.weight || !product.price) {
            setResponseMessage("Error. Please fill in all fields.");
        } else {
            setResponseMessage("");
            const response: Response = await server.addProduct(product);
            setProduct({name: "", img_src: "", weight: 0, price: 0, keys: []});
            setResponseMessage(response.status === "ok" ? "Product added" : "Product add error");
        }
    }

    const addKey = (name: string) => {
        setProduct(prevState => {
            return {...prevState, keys: [...prevState.keys, name]};
        });
        setKeys(prevState => {
            return prevState.filter(key => key !== name)
        });
    }

    const removeKey = (name: string) => {
        setProduct(prevState => {
            return {...prevState, keys: prevState.keys.filter((key) => key !== name)};
        });
        setKeys(prevState => {
            return [...prevState, name];
        });
    }

    return (
        <>
            <div className="product_add_container">
                <Button className="product_add_open_button" onClick={() => setModalIsOpen(!modalIsOpen)}>
                    <FontAwesomeIcon className={modalIsOpen ? "product_add_open_button_icon" : ""} icon={faPlus}></FontAwesomeIcon>
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
                <div className="product_add_form_keys_container">
                    {product.keys.length ?
                        <ul className="multi_chose_items">
                            <List items={product.keys}
                                  renderItem={(key) => <KeyItem isRemove={true} addKey={addKey} removeKey={removeKey}
                                                                name={key} key={key}/>}
                            />
                        </ul>
                        :
                        <div className="keys_placeholder">keys</div>
                    }

                    <div className="product_add_form_keys_dropdown_container">
                        <ul className="multi_chose_items">
                            <List items={keys}
                                  renderItem={(key) => <KeyItem isRemove={false} addKey={addKey} removeKey={removeKey} name={key} key={key}/>}
                            />
                        </ul>
                    </div>
                </div>
                <Button className="product_add_form_push_button" onClick={() => fetchAddProduct()}>
                    <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon>
                </Button>
                {modalIsOpen && <span
                    className={responseMessage.toLowerCase().includes("error") ? "responseError" : "responseSuccess"}>{responseMessage}</span>}
            </div>

        </>
    );
};

export default ProductAdd;