"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Sidebar from '../component/sidebar';

interface InventoryItem {
  product_id: string;
  name: string;
  price: number;
  purity: string;
  quantity: number;
  still: number; // Changed from optional to required since it exists in your DB
  manufactory_id?: string;
  retail_id?: string;
}

interface ApiResponse {
  message?: string;
  error?: string;
  product_id?: string;
}

const InventoryAndSellPage: React.FC = () => {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  
  // Form state for selling items
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const [sellPrice, setSellPrice] = useState<string>('');
  const [sellQuantity, setSellQuantity] = useState<string>('1');
  
  // Modal state
  const [showSellModal, setShowSellModal] = useState<boolean>(false);

  // Fetch inventory on component mount
  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/inventory/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: InventoryItem[] = await response.json();
      setInventory(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load inventory. Please try again later.');
      setLoading(false);
      console.error('Error fetching inventory:', err);
    }
  };

  const openSellModal = (item: InventoryItem) => {
    setSelectedItem(item.product_id);
    setSellPrice(item.price.toString());
    setSellQuantity('1');
    setShowSellModal(true);
  };

  const closeSellModal = () => {
    setShowSellModal(false);
    setSelectedItem(null);
    setSellPrice('');
    setSellQuantity('1');
    setMessage(null);
  };

  const handleSellItem = async () => {
    try {
      setMessage(null);
      
      if (!selectedItem) {
        setMessage({ type: 'error', text: 'No item selected' });
        return;
      }
      

      const price = parseFloat(sellPrice);
      const quantity = parseInt(sellQuantity);
      
      if (isNaN(price) || price <= 0) {
        setMessage({ type: 'error', text: 'Please enter a valid price' });
        return;
      }
      
      if (isNaN(quantity) || quantity <= 0) {
        setMessage({ type: 'error', text: 'Please enter a valid quantity' });
        return;
      }
      

      const item = inventory.find(i => i.product_id === selectedItem);
      if (!item) {
        setMessage({ type: 'error', text: 'Item not found in inventory' });
        return;
      }
      

      if (quantity > item.still) {
        setMessage({ type: 'error', text: `You only have ${item.still} units available` });
        return;
      }
      
      const response = await fetch('http://127.0.0.1:8000/api/sell/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: selectedItem,
          price: price,
          quantity: quantity
        })
      });

      const data: ApiResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
      }
      
      setMessage({ type: 'success', text: data.message || 'Item listed for sale successfully' });
      

      fetchInventory();
      

      setTimeout(() => {
        closeSellModal();
      }, 2000);
      
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to list item for sale. Please try again.';
      setMessage({ type: 'error', text: errorMessage });
      console.error('Error selling item:', err);
    }
  };

  return (
    <div className="flex">
      <div className='fixed h-full'>
        <Sidebar />
      </div>
      <div className='ml-64 p-8 w-full'>        
        <div className="flex-1 ml-4">
          {message && !showSellModal && (
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
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Purity</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Available</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Quantity</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {inventory.length > 0 ? (
                    inventory.map((item) => (
                      <tr key={item.product_id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{item.name}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.purity}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.price}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.still}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.quantity}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {item.manufactory_id}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => openSellModal(item)}
                            className="text-indigo-600 hover:text-indigo-900 transition duration-150 ease-in-out"
                            disabled={item.still <= 0}
                          >
                            Sell
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={7} className="px-6 py-4 text-center text-sm text-gray-500">
                        Your inventory is empty. Purchase products to see them here.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
      
      {showSellModal && selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Sell Item</h2>
            
            {message && (
              <div className={`p-3 mb-4 rounded-md ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {message.text}
              </div>
            )}
            
            <div className="mb-4">
              <p className="text-gray-700 mb-2">
                <span className="font-medium">Item: </span>
                {inventory.find(i => i.product_id === selectedItem)?.name}
              </p>
              <p className="text-gray-700 mb-2">
                <span className="font-medium">Available Quantity: </span>
                {inventory.find(i => i.product_id === selectedItem)?.still}
              </p>
              <p className="text-gray-700 mb-2">
                <span className="font-medium">Purity: </span>
                {inventory.find(i => i.product_id === selectedItem)?.purity}
              </p>
            </div>
            
            <div className="mb-4">
              <label htmlFor="sellPrice" className="block text-sm font-medium text-gray-700 mb-1">
                Selling Price ($):
              </label>
              <input
                id="sellPrice"
                type="number"
                min="0.01"
                step="0.01"
                value={sellPrice}
                onChange={(e) => setSellPrice(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="mb-6">
              <label htmlFor="sellQuantity" className="block text-sm font-medium text-gray-700 mb-1">
                Quantity to Sell:
              </label>
              <input
                id="sellQuantity"
                type="number"
                min="1"
                max={inventory.find(i => i.product_id === selectedItem)?.still}
                value={sellQuantity}
                onChange={(e) => setSellQuantity(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex justify-end space-x-3">
              <button
                onClick={closeSellModal}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition duration-150 ease-in-out"
              >
                Cancel
              </button>
              <button
                onClick={handleSellItem}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-150 ease-in-out"
              >
                List for Sale
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InventoryAndSellPage;