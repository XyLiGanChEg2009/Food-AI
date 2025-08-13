import { FC } from "react";
import {Product} from "../../types";
import { addProductToCart } from "../../store/reducers/CartSlice";

import Button from "../Button/Button";

import "./ProductCard.css"
import {faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {useAppDispatch} from "../../hooks/redux";

interface ProductCardProps {
    product: Product;
}

const ProductCard: FC<ProductCardProps> = ({product}) => {
    const dispatch = useAppDispatch();

    return (
        <div className="card_container">
            <img className="card_image" src={product.img_src} alt="" />
            <span className="card_price">{product.price}₽</span>
            <span className="card_name">{product.name}</span>
            <span className="card_weight">{product.weight} г</span>
            <Button className="card_add_product_button" onClick={() => {dispatch(addProductToCart(product))}}>
                <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon> Добавить
            </Button>
            {product.keys && <span className="card_keys">{product?.keys.join(", ")}</span>}
        </div>
    );
}

export default ProductCard;