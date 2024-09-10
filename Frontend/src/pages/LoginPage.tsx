import { ConfigProvider, theme } from "antd";
import LoginForm from "../components/auth/LoginForm";
import "../styles/login.css";
import logo from "../assets/GDYN-logo.svg";

const Login: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorBgContainer: "#1F1F1F",
          colorBorder: "#6e6e6e",
        },
      }}
    >
      <div className="page-container">
        <div className="hero-container">
          <img className="hero-image" width={200} src={logo} alt="grid-logo" />
          <h2 style={{ color: "white", textAlign: "center" }}>Grid Dynamics</h2>
          <h2 style={{ color: "white", margin: "1rem 0 4rem 0" }}>
            LLM-BI
          </h2>
        </div>
        <div className="login-container">
          <LoginForm />
        </div>
      </div>
    </ConfigProvider>
  );
};

export default Login;
