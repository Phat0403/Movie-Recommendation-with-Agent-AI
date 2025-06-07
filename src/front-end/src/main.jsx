import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

import './index.css';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import ExplorePage from './pages/ExplorePage.jsx';
import DetailsPage from './pages/DetailsPage.jsx';
import SearchPage from './pages/SearchPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import ResetPasswordPage from './pages/ResetPasswordPage.jsx';
import TheaterMovies from './pages/TheaterMovies.jsx';
import DetailsTheater from './pages/DetailsTheater.jsx';
import MyListPage from './pages/MyListPage.jsx';

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
        path: '/theater-movies', 
        element: <TheaterMovies />
      },
      {
      path: '/theater-movie/:id',
      element: <DetailsTheater />,
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
      },
      {
        path: '/my-list',
        element: <MyListPage/>
      },
    ],

  },
  {path:'/login', element: <LoginPage />},
  {path:'/register', element: <RegisterPage />},
  {path:'/reset-password', element: <ResetPasswordPage />}, // Assuming you have a ResetPasswordPage component

]);

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}> {/* 👈 Bọc Router trong Provider */}
      <RouterProvider router={router} />
      <Toaster 
        position="top-center" 
        reverseOrder={false}
      /> 
    </QueryClientProvider>
);
