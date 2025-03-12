"use client";

import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Sidebar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isRetailer, setIsRetailer] = useState(false);
  const [isManufactory, setIsManufactory] = useState(false);

  const router = useRouter();

  useEffect(() => {
    const token:any = localStorage.getItem('jwt');
    if (token) {
      setIsAuthenticated(true);
      try{      
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      if (decodedToken.role === 'retailer') {
        setIsRetailer(true);
      }
      if (decodedToken.role === 'manufactory') {
        setIsManufactory(true);
      }
    }catch(err){
      console.log(err)
    }

    }
  }, []);


  const logout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/signout/", {
        method: "POST",
        credentials: "include" 
      });
      
      if (!response.ok) {
        throw new Error("Failed to logout");
      }
      

      localStorage.removeItem('jwt');
      document.cookie.split(";").forEach((c) => {
        document.cookie = c
          .replace(/^ +/, "")
          .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });
      setIsAuthenticated(false);
      

      router.push('/');
      router.refresh();
      
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="h-full w-64 fixed top-0 left-0 bg-gray-900 text-white">
      <ol className="list-none p-0">
        <li className="p-4 text-center hover:bg-gray-700">
          <Link href="/">Home</Link>
        </li>

        {!isAuthenticated && (
          <>
            <li className="p-4 text-center hover:bg-gray-700">
              <Link href="/signup">Sign Up</Link>
            </li>
            <li className="p-4 text-center hover:bg-gray-700">
              <Link href="/login">Sign In</Link>
            </li>
          </>
        )}
        
        {isAuthenticated && (
          <>
            <li className="p-4 text-center hover:bg-gray-700">
              <Link href="/profile">Profile</Link>
            </li>
            <li className="p-4 text-center hover:bg-gray-700">
              <Link href="/settings">Settings</Link>
            </li>
            {isRetailer && (
              <>
                <li className="p-4 text-center hover:bg-gray-700">
                  <Link href="/retailer">Stocking</Link>
                </li>
                <li className="p-4 text-center hover:bg-gray-700">
                  <Link href="/shelf_retail">Buy stock</Link>
                </li>
              </>
            )}
            {isManufactory && (
              <>
                <li className="p-4 text-center hover:bg-gray-700">
                  <Link href="/additem">Create Product</Link>
                </li>
              </>
            )}
            <li className="p-4 text-center hover:bg-gray-700">
              <button 
                onClick={logout}
                className="text-white bg-transparent cursor-pointer w-full text-center"
              >
                Logout
              </button>
            </li>
          </>
        )}
      </ol>
    </div>
  );
}