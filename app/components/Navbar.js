import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar(){
    let [currentTab, setCurrentTab] = useState("home");
    function setActiveTab(tab){
        sessionStorage.setItem('active-tab', tab)
    }
    useEffect(() => {
        setCurrentTab(sessionStorage.getItem('active-tab') || 'home');
    }, [])
    return(
        <div className="p-2 container text-black flex flex-row gap-3 bg-white w-screen">
            <div className="flex flex-row gap-3 justify-center flex-wrap">
                <Link onNavigate={() => {setActiveTab('home')}} href="/" className="relative group cursor-pointer w-fit">
                    <h1 className="text text-2xl">
                        Synchro
                    </h1>
                    <span className="absolute bg-blue-500 h-0.5 left-0 bottom-[-2] w-0 transition-all duration-300 group-hover:w-full"></span>
                </Link>

                <div className="flex flex-row justify-center gap-3">
                    <Link href="/" className="cursor-pointer flex flex-col h-full w-fit justify-center ">
                        <button
                        className={`btn button p-1 rounded cursor-pointer ${currentTab == 'home' ? 'bg-blue-400 border-blue-600' : 'bg-transparent hover:bg-blue-400 transition-all duration-250 border-blue-500'} border-2`}
                        onClick={() => {setActiveTab('home')}}
                        >
                            Home
                        </button>
                    </Link>
                    <Link href="/create-pool" className="cursor-pointer flex flex-col h-full w-fit justify-center ">
                        <button 
                        className={`btn button p-1 rounded cursor-pointer ${currentTab == 'create-pool' ? 'bg-blue-400 border-blue-600' : 'bg-transparent hover:bg-blue-400 transition-all duration-250 border-blue-500'} border-2`}
                        onClick={() => {setActiveTab('create-pool')}}
                        >
                            Create Pool
                        </button>
                    </Link>
                    <Link href="/join-pool" className="cursor-pointer flex flex-col h-full w-fit justify-center">
                        <button 
                        className={`btn button p-1 rounded cursor-pointer ${currentTab == 'join-pool' ? 'bg-blue-400 border-blue-600' : 'bg-transparent hover:bg-blue-400 transition-all duration-250 border-blue-500'} border-2`}
                        onClick={() => {setActiveTab('join-pool')}}
                        >
                            Join Pool
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    )
}