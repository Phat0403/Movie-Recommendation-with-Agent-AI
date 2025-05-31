// Header.js
import React, { useState, useEffect, useRef } from "react"; // Thêm useRef
import logo from "../assets/logo.png";
import { Link, NavLink, useNavigate, useLocation } from "react-router-dom";
import userIcon from "../assets/user.png";
import { IoSearchOutline } from "react-icons/io5";
import { FiUser, FiLogOut } from "react-icons/fi"; // Icons cho Profile và Logout
import { navigation } from "../contants/navigation";
import { useAuth } from '../hooks/useAuth'; // *** MODIFIED: Import useAuth ***

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const dropdownRef = useRef(null); // Ref cho dropdown để xử lý click bên ngoài

  // *** MODIFIED: Use useAuth hook ***
  const { currentUser, loadingAuth, logout } = useAuth();

  const removeSpace = location?.search?.slice(3)?.split("%20")?.join(" ");
  const [searchInput, setSearchInput] = useState(removeSpace || "");
  // const [isLoggedIn, setIsLoggedIn] = useState(false); // *** REMOVED: No longer needed ***
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // State cho dropdown

  // *** REMOVED: useEffect for manual token check is no longer needed ***
  // useEffect(() => {
  //   const token = localStorage.getItem("token");
  //   setIsLoggedIn(!!token);
  // }, [location]);

  // Xử lý click bên ngoài để đóng dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    if (isDropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isDropdownOpen]);

  // *** ADDED: Update searchInput when location.search changes (from previous good suggestion) ***
  useEffect(() => {
    const newSearchQuery = location?.search?.slice(3)?.split("%20")?.join(" ") || "";
    setSearchInput(newSearchQuery);
  }, [location.search]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchInput.trim())}`);
    }
  };

  const handleLogout = () => {

    logout(); // *** MODIFIED: Use logout from useAuth ***
    setIsDropdownOpen(false); // Đóng dropdown sau khi logout
    navigate("/login");
  };

  const handleSignIn = () => {
    navigate("/login");
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleProfileClick = () => {
    navigate("/profile"); // Hoặc đường dẫn profile của bạn
    setIsDropdownOpen(false); // Đóng dropdown khi điều hướng
  }

  // *** ADDED: Helper to get full user details if needed, assuming currentUser is just username ***
  // This is a workaround. Ideally, useAuth().currentUser would be the full object.
  const getStoredUserDetails = () => {
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      try {
        return JSON.parse(storedUser);
      } catch (e) {
        console.error("Failed to parse stored user details:", e);
        return null;
      }
    }
    return null;
  }

  const userDetailsFromStorage = currentUser ? getStoredUserDetails() : null;
  // If your userIcon should be dynamic based on stored data (e.g., userDetailsFromStorage.avatarUrl)
  // const avatarToDisplay = userDetailsFromStorage?.avatarUrl || userIcon;
  // For now, sticking to the original static userIcon:
  const avatarToDisplay = userIcon;


  return (
    <header className="fixed top-0 w-full h-16 bg-black opacity-75 z-40">
      <div className="container mx-auto px-3 flex items-center h-full">
        <Link to={"/"}>
          <img src={logo} alt="logo" width={120} />
        </Link>
        <nav className="hidden lg:flex items-center gap-1 ml-5">
          {navigation.map((nav, index) => (
            <NavLink
              key={nav.label + index}
              to={nav.href}
              className={({ isActive }) =>
                `px-2 hover:text-neutral-100 text-sm ${
                  isActive ? "text-white font-semibold" : "text-neutral-300"
                }`
              }
            >
              {nav.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-5">
          <form className="flex items-center gap-2" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Search here..."
              className="bg-transparent px-4 py-1 border-none outline-none hidden lg:block text-white placeholder-neutral-400 text-sm"
              onChange={(e) => setSearchInput(e.target.value)}
              value={searchInput}
            />
            <button type="submit" className="text-2xl text-white hover:text-sky-400">
              <IoSearchOutline />
            </button>
          </form>

          {/* *** MODIFIED: Conditional rendering based on auth.currentUser and auth.loadingAuth *** */}
          {loadingAuth ? (
            // Optional: Placeholder while auth state loads, can be simple or match button size
            <div className="w-8 h-8 rounded-full bg-neutral-700 animate-pulse"></div>
          ) : currentUser ? ( // currentUser is the username string
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={toggleDropdown}
                className="focus:outline-none"
              >
                <img
                  className="w-8 h-8 rounded-full overflow-hidden cursor-pointer active:scale-90 transition-transform"
                  src={avatarToDisplay} // Using the original static userIcon or a potentially dynamic one
                  alt={currentUser?.username || "user"} // Alt text is username
                  onError={(e) => { e.target.onerror = null; e.target.src = userIcon;}} // Fallback for avatarToDisplay
                />
              </button>
              {isDropdownOpen && (
                <div
                  className="absolute right-0 mt-2 w-48 bg-slate-800 rounded-md shadow-xl z-50 py-1 animate-fadeIn"
                >
                  {/* Optional: Display Username if you want */}
                  <div className="px-4 py-2 text-sm text-neutral-400 border-b border-slate-700">
                    Signed in as: <strong className="text-neutral-200 block">{currentUser?.username}</strong>
                  </div>
                  <button
                    onClick={handleProfileClick}
                    className="w-full text-left flex items-center px-4 py-2.5 text-sm text-gray-300 hover:bg-slate-700 hover:text-sky-400 transition-colors duration-150"
                  >
                    <FiUser className="mr-3 h-5 w-5" />
                    Profile
                  </button>
                  <div className="border-t border-slate-700 my-1"></div>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left flex items-center px-4 py-2.5 text-sm text-gray-300 hover:bg-slate-700 hover:text-rose-400 transition-colors duration-150"
                  >
                    <FiLogOut className="mr-3 h-5 w-5" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button
              onClick={handleSignIn}
              className="bg-sky-500 hover:bg-sky-600 text-white px-4 py-1.5 rounded-md font-semibold text-sm transition-colors"
            >
              Sign In
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;