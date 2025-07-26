import { useState, createContext, useEffect, ChangeEvent } from 'react';
import { Server } from "./modules/Server/Server";

import ProductCard from './components/ProductCard/ProductCard';
import Search from './components/Search/Search';
import ProductAdd from "./components/ProductAdd/ProductAdd";
import List from "./components/List/List";

import {Product} from "./types";

import './App.css';

export const ServerContext = createContext<Server>(null!);

function App() {
    const [query, setQuery] = useState<string>("");
    const [products, setProducts] = useState<Product[]>([]);
    const [cart, setCart] = useState<Product[]>([]);

    const server = new Server();

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    const addProductToCart = (product: Product) => {
        setCart(prevState => {
            return [...prevState, product];
        });
    }

    const fetchProducts = async () => {
        const response = await server.getProducts(query);
        setProducts(response);
    }

    useEffect(() => {
        // fetchProducts();
    }, [])

    return (
        <ServerContext value={server}>
            <div className="App">
                <header>
                    <ProductAdd/>
                    <h1 className="service_name">Поиск еды</h1>
                    <Search handleInputChange={handleInputChange} fetchProducts={fetchProducts}></Search>
                </header>

                <div className="main">
                    <List
                        items={products}
                        className="product_list"
                        renderItem={(product: Product) =>
                            <ProductCard
                                product={product}
                                addProductToCart={addProductToCart}
                                key={product.name}
                            />
                        }
                    />
                </div>
            </div>
        </ServerContext>
    );
}

export default App;
