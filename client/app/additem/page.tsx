"use client";
import React from "react";
import Link from "next/link";

export default function AddItem() {
    const [product, setProduct] = React.useState({
        name: '',
        price: '',
        purity: '',
        category: '',
        quantity: ''
    });

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8000/api/create-product/", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": `Bearer ${localStorage.getItem('jwt')}`
                },
                body: JSON.stringify(product)
            });
            if (response.ok) {
               
                console.log("Product added successfully");
            } else {
                
                console.error("Failed to add product");
            }
        } catch (err) {
            console.log(err);
        }
    };

    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setProduct({
            ...product,
            [name]: value
        });
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg mt-4 mb-4 w-[500px]">
                <h1 className="text-2xl font-bold text-center mb-4">Add Item</h1>
                <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
                    <label className="text-gray-700">Product Name</label>
                    <input
                        type="text"
                        name="name"
                        className="border rounded p-2 mt-1"
                        placeholder="Necklace"
                        onChange={handleChange}
                    />
                    <label className="text-gray-700">Price</label>
                    <input
                        type="text"
                        name="price"
                        className="border rounded p-2 mt-1"
                        placeholder="99999"
                        onChange={handleChange}
                    />
                    <label className="text-gray-700">Purity</label>
                    <input
                        type="text"
                        name="purity"
                        className="border rounded p-2 mt-1"
                        placeholder="99.99%"
                        onChange={handleChange}
                    />
                    <label className="text-gray-700">Category</label>
                    <input
                        type="text"
                        name="category"
                        className="border rounded p-2 mt-1"
                        placeholder="Jewelry"
                        onChange={handleChange}
                    />
                    <label className="text-gray-700">Quantity</label>
                    <input
                        type="text"
                        name="quantity"
                        className="border rounded p-2 mt-1"
                        placeholder="1"
                        onChange={handleChange}
                    />
                    <button type="submit" className="bg-yellow-400 text-black py-2 rounded hover:bg-blue-600">
                        Add Item
                    </button>
                </form>
            </div>
        </div>
    );
}