import React from "react";

interface ProductCardProps<T> {
    items: T[];
    renderItem: (item: T) => React.ReactNode;
    className?: string;
}

export default function List<T>(props: ProductCardProps<T>) {
    return (  
        <div className={props.className}>
            {props.items.map(props.renderItem)}
        </div>
    );
};
