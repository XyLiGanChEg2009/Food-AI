import {FC, useState, memo} from "react";

import Button from "../Button/Button";
import List from "../List/List";
import CartProduct from "./CartProduct/CartProduct";

import {clearCart} from "../../store/reducers/CartSlice";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";

import "./Cart.css";
import {useAppDispatch, useAppSelector} from "../../hooks/redux";


export const Cart: FC = memo(() => {
    const dispatch = useAppDispatch();
    const {cart} = useAppSelector(state => state.cartReducer)

    const [modalOpen, setModalOpen] = useState<boolean>(false);

    const modalOpenChangeHandler = () => {
        if (cart.length) {
            setModalOpen(!modalOpen);
        }
    }

    const handleClearCart = () => {
        dispatch(clearCart());
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
                    <Button onClick={() => handleClearCart()} className="cart_modal_clear">Очистить</Button>
                </div>
                <div className="cart_product_list">
                    <List
                        items={cart}
                        renderItem={(cartItem) => <CartProduct
                            cartItem={cartItem}
                            key={cartItem.product.id}
                        />}
                    />
                </div>
            </div>}
        </>
    );
});