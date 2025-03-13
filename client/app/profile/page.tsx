"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Sidebar from '../component/sidebar';

interface InventoryItem {
  product_id: string;
  name: string;
  price: number;
  purity: string;
  still: number;
  quantity: number;
  manufactory_id: string;
  retail_id: string;
}

interface TransactionItem {
  product_id: string;
  type: string;
  name: string;
  price: number;
  purity: string;
  quantity: number;
  timestamp: string;
}

interface User {
  name: string;
  email: string;
  balance: number;
  Inventory: InventoryItem[];
  Transaction: TransactionItem[];
}

const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/user-profile/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: User = await response.json();
      setUser(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load user profile. Please try again later.');
      setLoading(false);
      console.error('Error fetching user profile:', err);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Head>
        <title>User Profile</title>
        <meta name="description" content="User profile including inventory and transactions" />
      </Head>
      <div className='flex flex-row'>
        <div className="fixed h-full">
        <Sidebar />
        </div>
        <div className="ml-64">
          <h1 className="text-3xl font-bold mb-8">User Profile</h1>
          
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : error ? (
            <div className="bg-red-100 text-red-800 p-4 rounded-md">{error}</div>
          ) : user ? (
            <div>
              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">User Details</h2>
                <p><strong>Name:</strong> {user.name}</p>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Balance:</strong> ${user.balance}</p>
              </div>

              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Inventory</h2>
                {user.Inventory?.length > 0 ? (
                  <table className="min-w-full bg-white">
                    <thead>
                      <tr>
                        <th className="py-2">Product ID</th>
                        <th className="py-2">Name</th>
                        <th className="py-2">Price</th>
                        <th className="py-2">Purity</th>
                        <th className="py-2">Still</th>
                        <th className="py-2">Quantity</th>
                        <th className="py-2">Manufactory ID</th>
                        <th className="py-2">Retail ID</th>
                      </tr>
                    </thead>
                    <tbody>
                      {user.Inventory.map((item) => (
                        <tr key={item.product_id}>
                          <td className="py-2">{item.product_id}</td>
                          <td className="py-2">{item.name}</td>
                          <td className="py-2">${item.price}</td>
                          <td className="py-2">{item.purity}</td>
                          <td className="py-2">{item.still}</td>
                          <td className="py-2">{item.quantity}</td>
                          <td className="py-2">{item.manufactory_id}</td>
                          <td className="py-2">{item.retail_id}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p>No inventory items found.</p>
                )}
              </div>

              <div>
                <h2 className="text-2xl font-semibold mb-4">Transactions</h2>
                {user.Transaction?.length > 0 ? (
                  <table className="min-w-full bg-white">
                    <thead>
                      <tr>
                        <th className="py-2">Product ID</th>
                        <th className="py-2">Type</th>
                        <th className="py-2">Name</th>
                        <th className="py-2">Price</th>
                        <th className="py-2">Purity</th>
                        <th className="py-2">Quantity</th>
                        <th className="py-2">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {user.Transaction.map((item) => (
                        <tr key={item.product_id}>
                          <td className="py-2">{item.product_id}</td>
                          <td className="py-2">{item.type}</td>
                          <td className="py-2">{item.name}</td>
                          <td className="py-2">${item.price}</td>
                          <td className="py-2">{item.purity}</td>
                          <td className="py-2">{item.quantity}</td>
                          <td className="py-2">{new Date(item.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p>No transactions found.</p>
                )}
              </div>
            </div>
          ) : (
            <div>No user data available.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;