import { Skeleton, Spin, Typography } from "antd";
import { staticQueries } from "../../assets/utils/chartExampleData";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { ApiContext } from "../app/Layout";
import { useContext } from "react";
import { vs } from "react-syntax-highlighter/dist/esm/styles/prism";

const SqlCard = ({ keyIndex }: { keyIndex: string }) => {
  // const index = +keyIndex.split("newTab")[1];
  const index = 0;
  const { chartDataFromApi, loading } = useContext(ApiContext);
  // const sql_query = !!chartDataFromApi?  chartDataFromApi[index].sql_query: '';

  if (loading) {
    return <Skeleton />;
  }
  if (!!chartDataFromApi) { 
    return (
      <>
        <div
          style={{
            border: "1px solid #f2233",
            padding: "1rem",
            height: "20vh",
            overflow: "auto",
          }}
        >
          <Typography.Title level={4}>Generated SQL Queries</Typography.Title>
          {
            chartDataFromApi?.map((current, key)=>{
              return (
          <div key={key}>
            <div>
              <Typography.Text strong>
                {current?.plot_title}
              </Typography.Text>
            </div>
            <div>
              <SyntaxHighlighter language="sql" style={vs}>
                {current?.sql_query}
              </SyntaxHighlighter>
            </div>
          </div>
              )
            })
          }
        </div>
      </>
    );
  } else {
    return (
      <Typography.Title level={4}>Write the query to generate Graph</Typography.Title>
    )
  }
};

export default SqlCard;
