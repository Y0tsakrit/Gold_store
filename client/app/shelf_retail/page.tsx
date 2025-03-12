"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';


interface Product {
  _id: string;
  name: string;
  price: number;
  purity: string;
  quantity: number;
}

interface ApiResponse {
  message?: string;
  error?: string;
}

const ProductPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/products/', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product[] = await response.json();
      setProducts(data);
      

      const initialQuantities: Record<string, number> = {};
      data.forEach(product => {
        initialQuantities[product._id] = 1; 
      });
      setQuantities(initialQuantities);
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load products. Please try again later.');
      setLoading(false);
      console.error('Error fetching products:', err);
    }
  };

  const handleQuantityChange = (productId: string, value: string) => {

    const quantity = Math.max(1, parseInt(value) || 1);
    setQuantities({
      ...quantities,
      [productId]: quantity
    });
  };

  const handlePurchase = async (productId: string) => {
    try {
      setMessage(null); 
      
      const response = await fetch('http://127.0.0.1:8000/purchase-retail/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: productId,
          quantity: quantities[productId]
        })
      });

      const data: ApiResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
      }
      
      setMessage({ type: 'success', text: data.message || 'Purchase successful' });
      

      fetchProducts();
    } catch (err: any) {
      const errorMessage = err.message || 'Purchase failed. Please try again.';
      setMessage({ type: 'error', text: errorMessage });
      console.error('Error making purchase:', err);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Head>
        <title>Products - Buy Gold</title>
        <meta name="description" content="Purchase gold products" />
      </Head>

      <h1 className="text-3xl font-bold mb-8">Manufactory Shelf</h1>
      
      {message && (
        <div className={`p-4 mb-6 rounded-md ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {message.text}
        </div>
      )}
      
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : error ? (
        <div className="bg-red-100 text-red-800 p-4 rounded-md">{error}</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.length > 0 ? (
            products.map(product => (
              <div key={product._id} className="border border-gray-200 rounded-lg shadow-sm overflow-hidden bg-white">
                <div className="p-5">
                  <h2 className="text-xl font-semibold text-gray-800 mb-2">{product.name}</h2>
                  <div className="space-y-2 mb-4">
                    <p className="text-gray-600">
                      <span className="font-medium">Purity:</span> {product.purity}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-medium">Price:</span> ${product.price.toFixed(2)}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-medium">Available:</span> {product.quantity} units
                    </p>
                  </div>
                  
                  <div className="mt-4">
                    <label htmlFor={`quantity-${product._id}`} className="block text-sm font-medium text-gray-700 mb-1">
                      Quantity:
                    </label>
                    <div className="flex items-center">
                      <input
                        id={`quantity-${product._id}`}
                        type="number"
                        min="1"
                        max={product.quantity}
                        value={quantities[product._id]}
                        onChange={(e) => handleQuantityChange(product._id, e.target.value)}
                        className="border border-gray-300 rounded-md px-3 py-2 w-24 text-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-500">
                        Total: ${(product.price * (quantities[product._id] || 0)).toFixed(2)}
                      </span>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handlePurchase(product._id)}
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={product.quantity < 1}
                  >
                    Buy Now
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center py-16 text-gray-500">
              No products available at the moment.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProductPage;