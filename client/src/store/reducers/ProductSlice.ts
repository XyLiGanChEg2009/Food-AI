import { Product } from "../../types";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {fetchProducts} from "./ActionCreators";

interface ProductState {
    products: Product[];
    isLoading: boolean;
    error: string;
}

const initialState: ProductState = {
    products: [],
    isLoading: false,
    error: "",
}

export const productSlice = createSlice({
    name: "product",
    initialState,
    reducers: {

    },
    extraReducers: (builder) => {
        builder.addCase(fetchProducts.fulfilled.type, (state, action: PayloadAction<Product[]>) => {
            state.products = action.payload;
            state.isLoading = false;
            state.error = "";
        })
        .addCase(fetchProducts.pending.type, (state, action) => {
            state.isLoading = true;
            state.error = "";
        })
        .addCase(fetchProducts.rejected.type, (state, action: PayloadAction<string>) => {
            state.isLoading = false;
            state.error = action.payload;
        })
    }
})

export default productSlice.reducer;