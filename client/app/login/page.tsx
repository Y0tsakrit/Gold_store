"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LogInPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        email: "",
        password: ""
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
            const response = await fetch("http://127.0.0.1:8000/api/signin/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to sign in");
            }
            console.log(data)
            localStorage.setItem("jwt", data.token);
            document.cookie = `jwt=${data.token}; path=/;`;

            alert("Signin successful!");
            router.push("/");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg w-80">
                <h1 className="text-2xl font-bold text-center mb-4">Welcome to Gold Store</h1>
                
                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}
                
                <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
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
                    <button 
                        type="submit" 
                        className={`${isLoading ? 'bg-gray-400' : 'bg-yellow-400'} text-black py-2 rounded hover:bg-yellow-500 transition`}
                        disabled={isLoading}
                    >
                        {isLoading ? "Logging in..." : "Login"}
                    </button>
                    <div className="flex items-center space-x-2">
                        <h2 className="text-xs mb-0 pl-14">Not a member?</h2>
                        <Link href='/signup'>
                            <span className="text-xs text-blue-500 relative top-[-1px] hover:underline">
                                Signup now
                            </span>
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
}