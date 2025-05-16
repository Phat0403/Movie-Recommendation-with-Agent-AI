import React, { use } from "react";
import logo from "../assets/logo.png";
import { Link, NavLink } from "react-router-dom";
import userIcon from "../assets/user.png";
import { IoSearchOutline } from "react-icons/io5";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { navigation } from "../contants/navigation";

const Header = () => {
  const [searchInput, setSearchInput] = useState("");
  
  const navigate = useNavigate();
  // useEffect(() => {
  //   navigate(`/search?q=${searchInput}`);
  // }, [searchInput]);
  return (
    <header className="fixed top-0 w-full h-16 bg-neutral-600 opacity-75 z-40">
      <div className="container mx-auto px-3 flex items-center h-full">
        <Link to={"/"}>
          <img src={logo} alt="logo" width={120} />
        </Link>
        <nav className="hidden lg:flex items-center gap-1 ml-5">
          {navigation.map((nav, index) => {
            return (
              <div key={index}>
                <NavLink
                  key={nav.label}
                  to={nav.href}
                  className={({ isActive }) =>
                    `px-2 hover:text-neutral-100 ${
                      isActive && "text-neutral-100"
                    }`
                  }
                >
                  {nav.label}
                </NavLink>
              </div>
            );
          })}
        </nav>
        <div className="ml-auto flex items-center gap-5">
          <form className="flex items-center gap-2" action="">
            <input
              type="text"
              placeholder="Search here..."
              className="bg-transparent px-4 py-1 border-none outline-none hidden lg:block"
              onChange={(e) => setSearchInput(e.target.value)}
              value={searchInput}
            />
            <button className="text-2xl text-white">
              <IoSearchOutline />
            </button>
          </form>

          <div>
            <img
              className="w-8 h-8 rounded-full overflow-hidden cursor-pointer active:scale-50 transition-all"
              src={userIcon}
              width="w-full h-full"
            />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
