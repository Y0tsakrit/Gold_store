"use client";  // Add this to enable client-side functionality

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignUpPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        phone: "",
        address: "",
        id: ""
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");

        try {
            const response = await fetch("http://127.0.0.1:8000/api/signup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
                credentials: "include"
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to sign up");
            }

            alert("Signup successful! Please log in.");
            router.push("/signin");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg mt-4 mb-4 w-full max-w-md">
                <h1 className="text-2xl font-bold text-center mb-6">Sign Up</h1>
                
                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}
                
                <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
                    <label className="flex flex-col text-gray-700">
                        Full Name
                        <input 
                            type="text" 
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="Gold Store" 
                            required
                        />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Email
                        <input 
                            type="email" 
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="CEI@kmitl.ac.th" 
                            required
                        />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Password
                        <input 
                            type="password" 
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="********" 
                            required
                        />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Phone
                        <input 
                            type="tel" 
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="+66 XX XXX XXXX" 
                            required
                        />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Address
                        <input 
                            type="text" 
                            name="address"
                            value={formData.address}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="123 Main St, City, Country" 
                            required
                        />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        ID Number
                        <input 
                            type="text" 
                            name="id"
                            value={formData.id}
                            onChange={handleChange}
                            className="border rounded p-2 mt-1" 
                            placeholder="1234567890" 
                            required
                        />
                    </label>
                    <button 
                        type="submit" 
                        className={`${isLoading ? 'bg-gray-400' : 'bg-yellow-400'} text-white py-2 rounded hover:bg-blue-600`}
                        disabled={isLoading}
                    >
                        {isLoading ? "Signing Up..." : "Sign Up"}
                    </button>

                    <div className="flex justify-center items-center space-x-2">
                        <h2 className="text-xs">Already have an account?</h2>
                        <Link href="/l">
                            <span className="text-xs text-blue-500 relative top-[-1px] hover:underline">
                                Login
                            </span>
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
}