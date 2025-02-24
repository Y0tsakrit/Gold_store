import Link from "next/link";

export default function LogInPage() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg w-80">
                <h1 className="text-2xl font-bold text-center mb-4">Welcome to Gold Store</h1>
                <form className="flex flex-col space-y-4">
                    <label className="flex flex-col text-gray-700">
                        Email
                        <input type="email" className="border rounded p-2 mt-1" placeholder="CEI@kmitl.ac.th" />
                    </label>
                    <label className="flex flex-col text-gray-700">
                        Password
                        <input type="password" className="border rounded p-2 mt-1" placeholder="********" />
                    </label>
                    <button type="submit" className="bg-yellow-400 text-black py-2 rounded hover:bg-blue-600">
                        Login
                    </button>
                    <div className="flex items-center space-x-2">
                        <h2 className="text-xs  mb-0 pl-14">Not a member?</h2>
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
