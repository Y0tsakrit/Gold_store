"use client";
import React from "react";
import Link from "next/link";
import Sidebar from "../component/sidebar";

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
                    'Accept': 'application/json',
                    "Authorization": `Bearer ${localStorage.getItem('jwt')}`
                },
                body: JSON.stringify(product)
            });
            
            if (response.ok) {
                alert("Product added successfully");
                // Reset form after successful submission
                setProduct({
                    name: '',
                    price: '',
                    purity: '',
                    category: '',
                    quantity: ''
                });
            } else {
                console.error("Failed to add product");
                alert("Failed to add product");
            }
        } catch (err) {
            console.log(err);
            alert("An error occurred while adding the product");
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
        <div className="flex">
            {/* Sidebar fixed on the left */}
            <div className="fixed h-full">
                <Sidebar />
            </div>
            
            {/* Main content with left margin to prevent overlap */}
            <div className="flex-1 ml-64 flex justify-center items-center min-h-screen bg-gray-100">
                <div className="bg-white p-8 rounded-lg shadow-lg m-4 w-[500px]">
                    <h1 className="text-2xl font-bold text-center mb-4">Add Item</h1>
                    <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
                        <label className="text-gray-700">Product Name</label>
                        <input
                            type="text"
                            name="name"
                            value={product.name}
                            className="border rounded p-2 mt-1"
                            placeholder="Necklace"
                            onChange={handleChange}
                            required
                        />
                        <label className="text-gray-700">Price</label>
                        <input
                            type="number"
                            name="price"
                            value={product.price}
                            className="border rounded p-2 mt-1"
                            placeholder="99999"
                            onChange={handleChange}
                            required
                        />
                        <label className="text-gray-700">Purity</label>
                        <input
                            type="text"
                            name="purity"
                            value={product.purity}
                            className="border rounded p-2 mt-1"
                            placeholder="99.99%"
                            onChange={handleChange}
                            required
                        />
                        <label className="text-gray-700">Category</label>
                        <input
                            type="text"
                            name="category"
                            value={product.category}
                            className="border rounded p-2 mt-1"
                            placeholder="Jewelry"
                            onChange={handleChange}
                            required
                        />
                        <label className="text-gray-700">Quantity</label>
                        <input
                            type="number"
                            name="quantity"
                            value={product.quantity}
                            className="border rounded p-2 mt-1"
                            placeholder="1"
                            onChange={handleChange}
                            required
                        />
                        <button type="submit" className="bg-yellow-400 text-black py-2 rounded hover:bg-blue-600 hover:text-white transition duration-300">
                            Add Item
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}