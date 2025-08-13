import {FC} from "react";
import Button from "../../Button/Button";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";

import {addProductToCart, removeProductFromCart} from "../../../store/reducers/CartSlice";

import {CartItem} from "../../../types";

import "./CartProduct.css";
import {useAppDispatch} from "../../../hooks/redux";

interface CartProductProps {
    cartItem: CartItem;
}

const CartProduct: FC<CartProductProps> = ({cartItem}) => {
    const dispatch = useAppDispatch();

    return (
        <div className="cart_product_container">
            <img className="cart_product_img" src={cartItem.product.img_src} alt=""/>
            <div className="card_product_info">
                <div className="cart_product_info_name">{cartItem.product.name}</div>
                <div>
                    <span className="cart_product_info_price">{cartItem.product.price}₽ - </span>
                    <span className="cart_product_info_weight">{cartItem.product.weight} г</span>
                </div>
            </div>
            <div className="product_count_change_container">
                <Button className="product_count_remove_button" onClick={() => dispatch(removeProductFromCart(cartItem.product))}>
                    <FontAwesomeIcon icon={faMinus}/>
                </Button>
                <span className="product_count">{cartItem.count}</span>
                <Button className="product_count_add_button" onClick={() => dispatch(addProductToCart(cartItem.product))}>
                    <FontAwesomeIcon icon={faPlus}/>
                </Button>
            </div>
        </div>
    );
};

export default CartProduct;