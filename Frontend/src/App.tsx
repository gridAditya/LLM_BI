import { ConfigProvider } from "antd";
import { AuthProvider } from "react-auth-kit";
import "./App.css";
import AppRoutes from "./Routes";

const App = () => {
  return (
    <>
      <ConfigProvider
        theme={{
          token: {
            // colorPrimary: "#F93333",
            colorPrimary: "#20A090",
          },
          components: {
            Layout: {
              siderBg: "#000",
            },
            Menu: {
              collapsedIconSize: 16,
              iconSize: 18,
              iconMarginInlineEnd: 14,
              darkItemColor: "#fff",
              darkItemSelectedColor: "#000",
              darkItemHoverBg: "#1f1f1f",
              groupTitleFontSize: 16,
              itemMarginBlock: 10,
            },
          },
        }}
      >
        <AuthProvider
          authType="cookie"
          authName="_auth"
          cookieDomain={window.location.hostname}
          cookieSecure={window.location.protocol === "https:"}
        >
          <AppRoutes />
        </AuthProvider>
      </ConfigProvider>
    </>
  );
};

export default App;
