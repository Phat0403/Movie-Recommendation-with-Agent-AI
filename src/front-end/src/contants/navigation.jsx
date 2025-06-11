import { MdHomeFilled } from "react-icons/md";
import { PiTelevisionFill } from "react-icons/pi";
import { BiSolidMoviePlay } from "react-icons/bi";
import { IoSearchOutline } from "react-icons/io5";
import { FaListAlt } from "react-icons/fa";

import { href } from "react-router-dom";

export const navigation = [
    { label: "Movie Shows", href: "/explore", icon: <PiTelevisionFill/> },
    { label: "Theater Movies", href: "/theater-movies", icon: <BiSolidMoviePlay /> },
 
  ];

export const mobileNavigation = [
    { label: "Home", href: "/" , icon: <MdHomeFilled />},
    ...navigation,
    {label: "Search" , href: "/search", icon: <IoSearchOutline/>}
  ];
