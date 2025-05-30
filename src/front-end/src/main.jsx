import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import './index.css';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import ExplorePage from './pages/ExplorePage.jsx';
import DetailsPage from './pages/DetailsPage.jsx';
import SearchPage from './pages/SearchPage.jsx';
import LoginPage from './pages/LoginPage.jsx';

const queryClient = new QueryClient();

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
      path: '/movie/:id',
      element: <DetailsPage/>
    },
      {
        path: '/search',
        element: <SearchPage/>
      }
    ],

  },
  {path:'/login', element: <LoginPage />},
  {path:'/register', element: <RegisterPage />},

]);

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}> {/* 👈 Bọc Router trong Provider */}
      <RouterProvider router={router} />
    </QueryClientProvider>
);
