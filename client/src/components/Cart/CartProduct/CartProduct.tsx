import {FC} from "react";
import Button from "../../Button/Button";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";

import {CartItem, Product} from "../../../types";

import "./CartProduct.css";

interface CartProductProps {
    cartItem: CartItem;
    removeProductFromCart: (product: Product) => void;
    addProductToCart: (product: Product) => void;
}

const CartProduct: FC<CartProductProps> = ({cartItem, removeProductFromCart, addProductToCart}) => {
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
                <Button className="product_count_remove_button" onClick={() => removeProductFromCart(cartItem.product)}>
                    <FontAwesomeIcon icon={faMinus}/>
                </Button>
                <span className="product_count">{cartItem.count}</span>
                <Button className="product_count_add_button" onClick={() => addProductToCart(cartItem.product)}>
                    <FontAwesomeIcon icon={faPlus}/>
                </Button>
            </div>
        </div>
    );
};

export default CartProduct;