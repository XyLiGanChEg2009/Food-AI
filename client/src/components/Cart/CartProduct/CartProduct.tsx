import {FC} from "react";
import Button from "../../Button/Button";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMinus } from "@fortawesome/free-solid-svg-icons";

import {Product} from "../../../types";

import "./CartProduct.css";

interface CartProductProps {
    product: Product;
    removeProduct: (name: string) => void;
}

export const CartProduct: FC<CartProductProps> = ({product, removeProduct}) => {
    return (
        <div className="cart_product_container">
            <img className="cart_product_img" src={product.img_src} alt=""/>
            <div className="card_product_info">
                <div className="cart_product_info_name">{product.name}</div>
                <div>
                    <span className="cart_product_info_price">{product.price}₽ - </span>
                    <span className="cart_product_info_weight">{product.weight} г</span>
                </div>
            </div>
            <div className="product_count_change_container">
                <Button className="product_count_remove_button" onClick={() => removeProduct(product.name)}>
                    <FontAwesomeIcon icon={faMinus}/>
                </Button>
            </div>
        </div>
    );
};