'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  let [data, setData] = useState("Loading flask...");

  useEffect(() => {
    fetch("/api/test")
            .then(res => res.json())
            .then(dat => setData(dat.message))
            .catch(() => setData("Flask not found"));
  }, []);

  return (
    <div>
      <p>{data}</p>
    </div>
  );
}
