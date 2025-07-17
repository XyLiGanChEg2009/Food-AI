import { FC } from "react";
import { Product } from "../../types";

import "./ProductCard.css"


const ProductCard: FC<Product> = ({img_src, price, weight, name, keys}: Product) => {
    return ( 
        <div className="card_container">
            <img className="card_image" src={img_src} alt="" />
            <span className="card_price">{price}$</span>
            <span className="card_name">{name}</span>
            <span className="card_weight">{weight}g.</span>
            {keys && <span className="card_keys">{keys.join(", ")}</span>}
        </div>
    );
}

export default ProductCard;