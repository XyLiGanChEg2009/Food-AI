export type Response = {
    status: "ok" | "error";
    message?: string;
}

export type Product = {
    id?: number;
    name: string;
    img_src: string;
    price: number;
    weight: number;
    keys: string[];
}

export type CartItem = {
    product: Product;
    count: number;
}