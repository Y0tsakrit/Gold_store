import Image from "next/image";
import React from "react";
import Sidebar from "./component/sidebar";

export default function Home() {
  return (
    <div>
      <Sidebar/>
      <h1>Home</h1>
      <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
    </div>
  )
}
