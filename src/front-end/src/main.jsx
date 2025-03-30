import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import ExplorePage from './pages/ExplorePage.jsx';
import DetailsPage from './pages/DetailsPage.jsx';
import SearchPage from './pages/SearchPage.jsx';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <Home />,
      },
      {
        path: '/about', 
        element: <About />
      },
    {
      path: '/explore',
      element: <ExplorePage/>
    },
    {
      path: '/explore/:id',
      element: <DetailsPage/>
    },
      {
        path: '/search',
        element: <SearchPage/>
      }
    ],

  },
  {path:'/login', element: <Login />},
  {path:'/register', element: <Register />},

]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
