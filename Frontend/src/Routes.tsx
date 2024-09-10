import { RequireAuth } from "react-auth-kit";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import AppLayout from "./components/app/Layout";
import DashboardRoute from "./pages/DashboardPage";
import HomeRoute from "./pages/HomePage";
import Login from "./pages/LoginPage";
import PageNotFound from "./pages/PageNotFound";

const PrivateRoute: React.FC<{ Component: React.ElementType }> = ({
  Component,
}) => {
  return (
    <RequireAuth loginPath="/login">
      <Component />
    </RequireAuth>
  );
};
const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/login" />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    element: <PrivateRoute Component={AppLayout} />,
    children: [
      {
        path: "/home",
        element: <PrivateRoute Component={HomeRoute} />,
      },
      {
        path: "/dashboard",
        element: <PrivateRoute Component={DashboardRoute} />,
      },
    ],
  },
  {
    element: <PageNotFound />,
    path: "*",
  },
]);

const AppRoutes = () => {
  return <RouterProvider router={router} />;
}

export default AppRoutes;