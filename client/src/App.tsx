import { useState, createContext, useEffect, ChangeEvent } from 'react';
import { Server } from "./modules/Server/Server";

import ProductCard from './components/ProductCard/ProductCard';
import Search from './components/Search/Search';
import ProductAdd from "./components/ProductAdd/ProductAdd";

import {Product} from "./types";

import './App.css';

export const ServerContext = createContext<Server>(null!);

function App() {
    const [query, setQuery] = useState<string>("");
    const [products, setProducts] = useState<Product[]>([]);

    const server = new Server();

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

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
                <ProductAdd/>
                <h1>Поиск еды</h1>
                <Search handleInputChange={handleInputChange} fetchProducts={fetchProducts}></Search>

                <div className='product_list'>
                    {products.map((product, id) =>
                        <ProductCard
                            img_src={product.img_src}
                            price={product.price}
                            weight={product.weight}
                            name={product.name}
                            keys={product.keys}
                            key={id}
                        />
                    )}
                </div>
            </div>
        </ServerContext>
    );
}

export default App;
