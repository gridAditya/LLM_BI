import { Card, Flex, List, Modal, Skeleton, Spin } from "antd";
import { useContext, useState } from "react";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import { chartsdata } from "../../assets/utils/chartExampleData";
import { ApiContext } from "../app/Layout";
import Charts from "./Charts";

const ChartsLayout = ({ keyIndex }: { keyIndex: string }) => {
  const [chartModal, setChartModal] = useState(false);
  const [selectedChart, setSelectedChart] = useState<{
    sql_query: string;
    plot_type_name: string;
    plot_title: string;
    x: string;
    y: string;
    data: { x_value: string, y_value: number }[];
    legend: string[];
    description: string;

  } | null>();

  const index = +keyIndex.split("newTab")[1];
  const chartsDataLength = chartsdata.length;
  const { chartDataFromApi, loading } = useContext(ApiContext);


  console.log("Selected chart : ", selectedChart ? selectedChart.data : "Nothing...")


  return (
    <div style={{ width: "100%", height: "100%" }}>
      {loading ? (
        <Flex>
          <Card
            style={{ width: "50%", margin: 16, height: "50vh" }}
            loading={loading}
          >
            <Card.Meta
              title="Card title"
              description="This is the description"
            />
          </Card>
          <Card
            style={{ width: "50%", margin: 16, height: "50vh" }}
            loading={loading}
          >
            <Card.Meta
              title="Card title"
              description="This is the description"
            />
          </Card>
        </Flex>
      ) : (
        <List
          size="large"
          dataSource={chartDataFromApi}
          // dataSource={[...chartsdata.slice(0,5), ...chartsdata]}
          // dataSource={[
          //   ...chartsdata.slice(
          //     index % chartsDataLength,
          //     (index % chartsDataLength) + 4
          //   ),
          // ]}
          grid={{
            gutter: 6,
            xs: 1,
            sm: 2,
            md: chartDataFromApi?.length,
            lg: chartDataFromApi?.length,
            xl: chartDataFromApi?.length,
            // xl: 4,
            // xl: index + 4 - (index % chartsDataLength),
            // xxl: 3,
            xxl: chartDataFromApi?.length,
          }}
          renderItem={(item) => (
            <>
              {/* <h1>items {item}</h1> */}
              <List.Item
                // key={item.title}
                key={item.plot_title}
                style={{ padding: 0 }}
                onClick={() => {
                  console.log("Item clicked:", item);
                  setSelectedChart(item);
                  setChartModal(true);
                }}
              >
                <Card
                  title={item.plot_title}
                // title={item.title}
                // styles={{ body: { width: "100%" } }}
                >
                  <Charts
                    name={item.plot_title}
                    // name={item.title}
                    type={item.plot_type_name}
                    // type={item.type!}
                    data={
                      item.plot_type_name === "table"
                        ? item.data.slice(0, 3)
                        : item.data
                    }
                    insideModal={false}
                    setChartModal={setChartModal}
                    tableCol={{ x: item.x, y: item.y }}
                  />
                </Card>
              </List.Item>
            </>
          )}
        />
      )}

      <Modal
        open={chartModal}
        onCancel={() => setChartModal(false)}
        width={"80%"}
        // styles={{
        //   body: {
        //     minHeight: "500px",
        //   },
        // }}
        title={selectedChart?.plot_title}
        footer={null}
      >


        {selectedChart && (
          <Charts
            name={selectedChart.plot_title ?? 'Default Title'}
            type={selectedChart.plot_type_name ?? 'Default Type'}
            data={selectedChart.data ?? []}
            insideModal={true}
            setChartModal={setChartModal}
            tableCol={{ x: selectedChart.x ?? 'x', y: selectedChart.y ?? 'y' }}
          />
        )}

      </Modal>
    </div>
  );
};

export default ChartsLayout;

