import {Response, Product} from "../../types";

export class Server {
    HOST: string;
    constructor() {
        this.HOST = "http://127.0.0.1:1337/";

    }

    async getProducts(query: string): Promise<Product[]> {
        const res = await fetch(this.HOST + "get_products?query=" + query);
        return res.json();
    }

    async addProduct(product: Product): Promise<Response> {
        try {
            const res = await fetch(this.HOST + "add_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(product)
            });
            return res.json();
        } catch {
            return {"status": "error"}
        }
    }
}