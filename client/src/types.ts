export type Response = {
    status: "ok" | "error";
    message?: string;
}

export type Product = {
    name: string;
    img_src: string;
    price: number;
    weight: number;
    keys?: string[];
}