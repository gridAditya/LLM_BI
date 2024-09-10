import { Card, Typography } from "antd";
import "../styles/analysis.css";
import { UpOutlined } from "@ant-design/icons";
import CustomTabs from "../components/dashboard/CustomTabs";
import { useContext } from "react";
import { ApiContext } from "../components/app/Layout";

const DashboardPage = () => {
  const {chartDataFromApi} = useContext(ApiContext)
  return (
    <>
      <div className="search-query">
        <CustomTabs />
      </div>
      {!!!chartDataFromApi ? (
        <></>
      ) : (
        <>
          <div className="dashboard">
            <div className="dashboard__analysis-button">
              <UpOutlined />
              <p>Text Analysis For Query</p>
            </div>
            <div className="dashboard__analysis">
              {/* backgroundColor: "#dedede" */}
              <Card style={{ backgroundColor: "#000" }}>
                {
                  chartDataFromApi.map((current, index)=>{
                    return (
                      <div key={index}>
                <Typography.Title level={3} style={{ color: "white" }}>
                  {current.plot_title}
                </Typography.Title>
                <Typography.Paragraph
                  type="secondary"
                  style={{ color: "white" }}
                >
                  {current.description}
                </Typography.Paragraph>
                      </div>
                    )
                  })
                }
              </Card>
            </div>
          </div>
        </>
      )}
      {/* <div className="dashboard">
        <div className="dashboard__analysis-button">
          <UpOutlined />
          <p>Text Analysis For Query</p>
        </div>
        <div className="dashboard__analysis">
          <Card style={{ backgroundColor: "#dedede" }}>
            <Typography.Text>
              OPENING PRICES OF AAPL AND AMZN OVER TIME
            </Typography.Text>
            <Typography.Paragraph type="secondary">
              {chartDataFromApi[0].description}
            </Typography.Paragraph>
          </Card>
        </div>
      </div> */}
    </>
  );
};

export default DashboardPage;
