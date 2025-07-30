import React, { useState, createContext, useEffect, ChangeEvent } from 'react';
import { Server } from "./modules/Server/Server";

import ProductCard from './components/ProductCard/ProductCard';
import Search from './components/Search/Search';
import ProductAdd from "./components/ProductAdd/ProductAdd";
import List from "./components/List/List";
import {Cart} from "./components/Cart/Cart";

import {CartItem, Product} from "./types";

import './App.css';

export const ServerContext = createContext<Server>(null!);

function App() {
    const [query, setQuery] = useState<string>("");
    const [products, setProducts] = useState<Product[]>([]);
    const [cart, setCart] = useState<CartItem[]>([]);

    const server = new Server();

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    // [backend] Надо будет заменить название на id продукта из БД
    const addProductToCart = (product: Product) => {
        setCart(prevState => {
            if (prevState.some(item => item.product.name === product.name)) {
                return prevState.map(item => {
                    if (item.product.name === product.name) {
                        return { ...item, count: item.count + 1 };
                    }
                    return item;
                });
            } else {
                return [...prevState, {product: product, count: 1}]
            }
        });
    }
    // [backend] Надо будет заменить название на id продукта из БД
    const removeProductFromCart = (product: Product) => {
        setCart(prevState => {
            return prevState.reduce((acc, item) => {
                if (item.product.name !== product.name) {
                    acc.push(item);
                } else if (item.count > 1) {
                    acc.push({ ...item, count: item.count - 1 });
                }
                return acc;
            }, [] as CartItem[]);
        });
    };

    const fetchProducts = async () => {
        const response = await server.getProducts(query);
        setProducts(response);
    }

    useEffect(() => {
        fetchProducts();
    }, [])

    return (
        <ServerContext value={server}>
            <div className="App">
                <header>
                    <ProductAdd/>
                    <h1 className="service_name">Поиск еды</h1>
                    <Search handleInputChange={handleInputChange} fetchProducts={fetchProducts}></Search>
                    <Cart cart={cart} setCart={setCart} addProductToCart={addProductToCart} removeProductFromCart={removeProductFromCart}/>
                </header>

                <div className="main">
                    {
                    products.length ?
                        <div className="product_list">
                            <List
                                items={products}
                                renderItem={(product: Product) =>
                                    <ProductCard
                                        product={product}
                                        addProductToCart={addProductToCart}
                                        key={product.name}
                                    />
                                }
                            />
                        </div>
                    :
                        <div className="product_not_found_container">
                            <span className="product_not_found_message">По вашему запросу ничего не нашлось :(</span>
                        </div>
                    }
                </div>
            </div>
        </ServerContext>
    );
}

export default App;
