import {CartItem, Product} from "../../types";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";

interface CartState {
    cart: CartItem[];
}

const initialState: CartState = {
    cart: [],
}

export const cartSlice = createSlice({
    name: "cart",
    initialState,
    reducers: {
        addProductToCart: (state, action: PayloadAction<Product>) => {
            const newProduct = action.payload;
            const existingItem = state.cart.find(item => item.product.name === newProduct.name);
            if (existingItem) {
                existingItem.count++;
            } else {
                state.cart.push({ product: newProduct, count: 1 });
            }
        },
        removeProductFromCart: (state, action: PayloadAction<Product>) => {
            const productToRemove = action.payload;
            const itemIndex = state.cart.findIndex(
                item => item.product.name === productToRemove.name
            );
            if (itemIndex !== -1) {
                if (state.cart[itemIndex].count > 1) {
                    state.cart[itemIndex].count--;
                } else {
                    state.cart.splice(itemIndex, 1);
                }
            }
        },
        clearCart: (state) => {
            state.cart = [];
        }
    },
})

export const {addProductToCart, removeProductFromCart, clearCart} = cartSlice.actions;
export default cartSlice.reducer;