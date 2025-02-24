import Link from "next/link";

export default function SignUpPage() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg mt-4 mb-4 w-full max-w-md">
                <h1 className="text-2xl font-bold text-center mb-6">Sign Up</h1>
                <form className="flex flex-col space-y-4">
                    <label className="flex flex-col text-gray-700">
                        Full Name
                        <input type="text" className="border rounded p-2 mt-1" placeholder="Gold Store" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Email
                        <input type="email" className="border rounded p-2 mt-1" placeholder="CEI@kmitl.ac.th" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Password
                        <input type="password" className="border rounded p-2 mt-1" placeholder="********" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Phone
                        <input type="tel" className="border rounded p-2 mt-1" placeholder="+66 XX XXX XXXX" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Address
                        <input type="text" className="border rounded p-2 mt-1" placeholder="123 Main St, City, Country" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        ID Number
                        <input type="text" className="border rounded p-2 mt-1" placeholder="1234567890" />
                    </label>
                    <button type="submit" className="bg-yellow-400 text-white py-2 rounded hover:bg-blue-600">
                        Sign Up
                    </button>

                    <div className="flex justify-center items-center space-x-2">
                        <h2 className="text-xs">Already have an account?</h2>
                        <Link href="/login">
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