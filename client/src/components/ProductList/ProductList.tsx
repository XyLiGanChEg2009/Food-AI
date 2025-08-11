import React, {FC, useEffect} from "react";
import {useAppDispatch, useAppSelector} from "../../hooks/redux";
import List from "../List/List";
import ProductCard from "../ProductCard/ProductCard";
import { fetchProducts } from "../../store/reducers/ActionCreators";

import {Product} from "../../types";


const ProductList: FC = () => {
    const dispatch = useAppDispatch();
    const {products, isLoading, error} = useAppSelector(state => state.productReducer);

    useEffect(() => {
        dispatch(fetchProducts(""));
    }, [])
    return (
        <>
            {
                products.length > 0 &&
                    <div className="product_list">
                        <List
                            items={products}
                            renderItem={(product: Product) =>
                                <ProductCard
                                    product={product}
                                    key={product.name}
                                />
                            }
                        />
                    </div>
            }
            {
                error &&
                    <div className="product_not_found_container">
                        <span className="product_not_found_message">{error}</span>
                    </div>
            }
            {
                isLoading &&
                <div className="product_not_found_container">
                    <span className="product_not_found_message">Загрузка...</span>
                </div>
            }
        </>
    );
};

export default ProductList;