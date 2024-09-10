import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Avatar, Button, Flex, Layout, Result, Typography } from "antd";
import * as React from "react";
import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import "../../styles/layout.css";
import SidebarMenu from "./SidebarMenu";
import ScrollToBottom from "react-scroll-to-bottom";
import { plotGraphFromQuery } from "../../api/plotFromQuery";
import { PlotDataType } from "../../types/apiResponseType";
import InputArea from "./InputArea";

const { Header, Sider, Content } = Layout;
export const ApiContext = React.createContext<{
  chartDataFromApi: PlotDataType[] | undefined;
  loading: boolean;
}>({ chartDataFromApi: undefined, loading: false });
const AppLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [queries, setQueries] = useState<string[]>([]);
  const [chartDataFromApi, setChartDataFromApi] = useState<any>();
  const [errorResponse, seterrorResponse] = useState<any | null>(null);
  const navigate = useNavigate();

  const onSearch = async (
    setQuery: React.Dispatch<React.SetStateAction<string>>,
    query: string
  ) => {
    setQuery(() => query.trim());
    if (query === "") return;
    setLoading(true);
    try {
      setChartDataFromApi(await plotGraphFromQuery(query));
      setLoading(false);
      setQueries((prevQueries) => [...prevQueries, query]);
      setQuery("");
      navigate("/dashboard");
    } catch (error) {
      console.error("An error occurred while fetching data:", error);
      seterrorResponse(error);
      setLoading(false);
    }
  };

  return (
    <ApiContext.Provider value={{ chartDataFromApi, loading }}>
      <Layout style={{ height: "100vh" }}>
        <Sider
          className={`sider ${collapsed ? "collapsed" : ""}`}
          breakpoint="lg"
          collapsible
          collapsedWidth={70}
          collapsed={collapsed}
          trigger={null}
        >
          <Button
            className="sider__toggle"
            type="text"
            size="large"
            onClick={() => setCollapsed(!collapsed)}
            icon={
              collapsed ? (
                <MenuUnfoldOutlined style={{ color: "#fff", fontSize: 24 }} />
              ) : (
                <MenuFoldOutlined style={{ color: "#fff", fontSize: 24 }} />
              )
            }
          />
          <SidebarMenu />
          {!collapsed && (
            <footer className="sider__footer">
              Powered by&nbsp;
              <a
                href="https://www.griddynamics.com/"
                target="_blank"
                rel="noreferrer"
              >
                Grid Dynamics
              </a>
            </footer>
          )}
        </Sider>
        <Layout>
          <Header className="header">
            <h2 className="header__title">LLM-BI</h2>
            <div className="header__profile">
              <h3 className="header__username">Grid Dynamics</h3>
              <Avatar style={{ backgroundColor: "#000" }}>GD</Avatar>
            </div>
          </Header>
          <Content style={{ overflow: "scroll", padding: "1rem 2rem 0" }}>
            <ScrollToBottom>
              <Content style={{ maxHeight: "100px", margin: "8px 0" }}>
                {queries.map((query, index) => (
                  <Flex
                    key={index}
                    align="center"
                    gap="small"
                    style={{ margin: "1rem 0" }}
                  >
                    <UserOutlined />
                    <Typography.Text
                      style={{
                        background: "rgb(32 160 144 / 66%)",
                        padding: "8px",
                        borderRadius: "12px",
                      }}
                    >
                      {query}
                    </Typography.Text>
                  </Flex>
                ))}
              </Content>
            </ScrollToBottom>
            {errorResponse ? (
              <Result
                status={errorResponse?.response?.status || 404}
                title={errorResponse?.response?.status || "Network error"}
                subTitle={errorResponse?.message || "Network error"}
                extra={<Button onClick={() => navigate("/")}>Back Home</Button>}
              />
            ) : (
              <>
                <Flex gap="small" style={{ margin: "8px" }}>
                  <InputArea loading={loading} onSearch={onSearch} />
                </Flex>
                <Outlet context={[collapsed]} />
              </>
            )}
          </Content>
        </Layout>
      </Layout>
    </ApiContext.Provider>
  );
};

export default AppLayout;
