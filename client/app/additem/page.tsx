import Link from "next/link";

export default function AddItem() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg mt-4 mb-4 w-[500px]">
                <h1 className="text-2xl font-bold text-center mb-4">Add Item</h1>
                <form className="flex flex-col space-y-4">
                    <label className="text-gray-700">Product Name</label>
                    <input type="text" className="border rounded p-2 mt-1" placeholder="Necklace" />
                    <label className="text-gray-700">Price</label>
                    <input type="text" className="border rounded p-2 mt-1" placeholder="99999" />
                    <label className="text-gray-700">Purity</label>
                    <input type="text" className="border rounded p-2 mt-1" placeholder="99.99%" />
                    <label className="text-gray-700">Category</label>
                    <input type="text" className="border rounded p-2 mt-1" placeholder="Jewelry" />
                    <label className="text-gray-700">Quantity</label>
                    <input type="text" className="border rounded p-2 mt-1" placeholder="1" />
                    <button type="submit" className="bg-yellow-400 text-black py-2 rounded hover:bg-blue-600">
                        Add Item
                    </button>
                    <label className="text-gray-700">List of items</label>
                    <div className="border rounded p-2 h-32 overflow-y-scroll ">
                        {/* ของที่เพิ่มจะต้องเอามาใส่ตรงนี้ */}
                    </div>


                </form>
            </div>
        </div>
    );
}
