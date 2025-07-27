import {FC, useState} from "react";

import Button from "../Button/Button";
import List from "../List/List";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";

import {Product} from "../../types";

import "./Cart.css";
import {CartProduct} from "./CartProduct/CartProduct";

interface CartProps {
    cart: Product[];
    setCart: (cart: Product[]) => void;
}

export const Cart: FC<CartProps> = ({cart, setCart}) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);

    const modalOpenChangeHandler = () => {
        if (cart.length) {
            setModalOpen(!modalOpen);
        }
    }

    // [backend] Надо будет заменить название на id продукта из БД
    const removeProduct = (name: string) => {
        setCart(cart.filter((product) => product.name !== name));
    }

    return (
        <>
            <div className="cart_container">
                <Button onClick={() => {modalOpenChangeHandler()}} className="cart_view_button">
                    <FontAwesomeIcon icon={faCartShopping}/>
                    <span className={"cart_counter" + (cart.length ? "" : " zero")}>{cart.length ? cart.length : ""}</span>
                </Button>
            </div>
            {modalOpen && <div className="cart_modal_container">
                <List
                    items={cart}
                    renderItem={(product) => <CartProduct
                        product={product}
                        removeProduct={removeProduct}
                    />}
                    className="cart_product_list"
                />
            </div>}
        </>
    );
};