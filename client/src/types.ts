export type Response = {
    status: "ok" | "error";
}

export type Product = {
    name: string;
    img_src: string;
    price: number;
    weight: number;
    keys?: string[];
}