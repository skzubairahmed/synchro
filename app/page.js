'use client';
import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';

export default function Home() {
  let [data, setData] = useState("Loading flask...");
  let [activeTab, setActiveTab] = useState("home");

  return (
    <div>
      <Navbar />
    </div>
  );
}
