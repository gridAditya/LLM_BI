import { BarChartOutlined } from "@ant-design/icons";
import { Card, Spin, Typography } from "antd";
import { useContext } from "react";
import { ApiContext } from "../components/app/Layout";

const HomePage = () => {
  const {loading} = useContext(ApiContext)
  return (
    <>
      <Spin spinning={loading}>
        <div
          style={{
            marginTop: "2rem",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Card
            title={"LMM-BI Data Analytics"}
            bordered={false}
            style={{ width: 650, marginBottom: "6rem" }}
            cover={
              <BarChartOutlined
                size={1000}
                style={{ margin: "2rem auto 1rem auto", fontSize: "80px" }}
              />
            }
          >
            <Typography.Paragraph style={{ fontSize: "16px" }}>
              <strong>
                Ask a query and get data visualizations in real time!
                <br />
                Here are some examples to get started with -
              </strong>
              <ul>
                <br />
                <li>
                  Join the advanced_monthly_sales_for_retail_and_food_services
                  table with the
                  advanced_monthly_sales_for_retail_and_food_services_categories
                  table to display the total sales for each category for the
                  year 1992.
                </li>
                <li>
                  Retrieve the total sales for each category from the
                  'advanced_monthly_sales_for_retail_and_food_services' table,
                  combined with the category descriptions from the
                  'advanced_monthly_sales_for_retail_and_food_services_categories'
                  table. Filter the data to include only records from the year
                  1992. Group the results by category description and calculate
                  the total sales for each category.
                </li>
                <li>
                  Locate datasets containing information on wildlife migration
                  patterns in Africa over the past 50 years, specifically
                  focusing on the impact of climate change on migration routes
                  of endangered species such as elephants and rhinoceroses.
                </li>
              </ul>
            </Typography.Paragraph>
          </Card>
        </div>
      </Spin>
    </>
  );
};

export default HomePage;
