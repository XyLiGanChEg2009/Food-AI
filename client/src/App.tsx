import React, { createContext } from 'react';
import { Server } from "./modules/Server/Server";

import Search from './components/Search/Search';
import ProductAdd from "./components/ProductAdd/ProductAdd";
import {Cart} from "./components/Cart/Cart";


import './App.css';
import ProductList from "./components/ProductList/ProductList";

export const ServerContext = createContext<Server>(null!);

function App() {
    const server = new Server();

    return (
        <ServerContext value={server}>
            <div className="App">
                <header>
                    <ProductAdd/>
                    <h1 className="service_name">Поиск еды</h1>
                    <Search></Search>
                    <Cart/>
                </header>

                <div className="main">
                    <ProductList/>
                </div>
            </div>
        </ServerContext>
    );
}

export default App;
