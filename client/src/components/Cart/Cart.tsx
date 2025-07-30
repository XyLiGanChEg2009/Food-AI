import {FC, useState, memo} from "react";

import Button from "../Button/Button";
import List from "../List/List";
import CartProduct from "./CartProduct/CartProduct";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";

import {CartItem, Product} from "../../types";

import "./Cart.css";

interface CartProps {
    cart: CartItem[];
    setCart: (cart: CartItem[]) => void;
    addProductToCart: (product: Product) => void;
    removeProductFromCart: (product: Product) => void;
}

export const Cart: FC<CartProps> = memo(({cart, setCart, addProductToCart, removeProductFromCart}) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);

    const modalOpenChangeHandler = () => {
        if (cart.length) {
            setModalOpen(!modalOpen);
        }
    }

    const clearCart = () => {
        setCart([]);
        setModalOpen(false);
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
                <div className="cart_modal_header">
                    <div className="cart_modal_name">Корзинка</div>
                    <Button onClick={() => clearCart()} className="cart_modal_clear">Очистить</Button>
                </div>
                <div className="cart_product_list">
                    <List
                        items={cart}
                        renderItem={(cartItem) => <CartProduct
                            cartItem={cartItem}
                            removeProductFromCart={removeProductFromCart}
                            addProductToCart={addProductToCart}
                            key={cartItem.product.name} // надо будет поменять на id
                        />}
                    />
                </div>
            </div>}
        </>
    );
});