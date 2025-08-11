import {createAsyncThunk} from "@reduxjs/toolkit";
import {Product} from "../../types";
import axios from "axios";

export const fetchProducts = createAsyncThunk(
    'products/fetch',
    async (query: string, thunkAPI) => {
        try {
            const response = await axios.get<Product[]>("http://127.0.0.1:1337/get_products?query=" + query)
            if (!response.data.length) {
                return thunkAPI.rejectWithValue("По вашему запросу ничего не нашлось :(");
            }
            return response.data;
        } catch (e) {
            return thunkAPI.rejectWithValue("По вашему запросу ничего не нашлось :(");
        }
    }
)