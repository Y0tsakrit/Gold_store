import Link from "next/link";

export default function AddItem() {
    return (
        <div className="flex min-h-screen items-center bg-gray-100">
            <div className="bg-yellow-400  rounded-2xl shadow-lg w-[250px] h-[250px] flex justify-center items-center"
            style={{ marginTop: '350px', marginBottom: '550px', marginLeft: '400px' }}>
                <div className="text-2xl font-bold text-center mb-4">
                    Users
                </div>
            </div>
            <div className="bg-yellow-200  rounded-2xl shadow-lg w-[250px] h-[250px] flex justify-center items-center"
            style={{ marginTop: '350px', marginBottom: '550px', marginLeft: '100px' }}>
                <div className="text-2xl font-bold text-center mb-4">
                    Manufacturer
                </div>
            </div>
            <div className="bg-yellow-100  rounded-2xl shadow-lg w-[250px] h-[250px] flex justify-center items-center"
            style={{ marginTop: '350px', marginBottom: '550px', marginLeft: '100px' }}>
                <div className="text-2xl font-bold text-center mb-4">
                    Retail shop
                </div>
            </div>
        </div>
    );
}
