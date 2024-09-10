import { useContext, useState } from "react";
import ReactEcharts from "echarts-for-react";
import { TabsContext } from "./CustomTabs";
import { ChartsProps } from "../../types/chartsType";
import { Table } from "antd";

const Charts: React.FC<ChartsProps> = ({
  name,
  type,
  data,
  insideModal,
  setChartModal,
  tableCol
}: ChartsProps) => {
  const [selectedBarIndex, setSelectedBarIndex] = useState<number | null>(null);
  const { ...addNewTab } = useContext<{
    add: () => void;
  } | null>(TabsContext);
  const handleBarClick = (params: any) => {
    const clickedBarIndex = params.dataIndex;
    addNewTab.add();
    setChartModal(false);
    setSelectedBarIndex(clickedBarIndex);
  };
  const handleBarClickWithoutModal = (params: any) => {};

  console.log("Data from chart compoennets : ", data[0])

  const chartOptions: { [key: string]: any } = {
    pie: {
      tooltip: {},
      series: [
        {
          name: name,
          type: "pie",
          data: data.map((item: any) => ({
            value: item.y_value,
            name: item.x_value,
          })),
        },
      ],
    },
    line: {
      xAxis: {
        type: "category",
        data: data.map((item: any) => item.x_value),
      },
      tooltip: {},
      yAxis: {
        type: "value",
      },
      series: [
        {
          type: "line",
          name: name,
          data: data.map((item: any) => item.y_value),
        },
      ],
    },
    bar: {
      tooltip: {},
      xAxis: {
        type: "category",
        data: data.map((item: any) => item.x_value),
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          type: "bar",
          name: name,
          data: data.map((item: any) => item.y_value),
        },
      ],
    },
    area: {
      tooltip: {
        axisPointer: {
          label: {
            backgroundColor: "#283b56",
          },
        },
      },
      xAxis: {
        type: "category",
        data: data.map((item: any) => item.x_value),
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          type: "line",
          areaStyle: {},
          name: name,
          data: data.map((item: any) => item.y_value),
        },
      ],
    },
    funnel: {
      // tooltip: {},
      // legend: {
      //   data: data.map((current) => current.time).slice(0, 8),
      // },
      series: [
        {
          type: "funnel",
          left: "10%",
          top: 60,
          bottom: 60,
          width: "80%",
          sort: "descending",
          gap: 2,
          label: {
            show: true,
            position: "inside",
          },
          data: data.slice(0, 8).map((item) => ({
            name: item.x_value,
            value: item.y_value,
          })),
        },
      ],
    },
    scatter: {
      tooltip: {},
      xAxis: {
        type: "category",
        data: data.map((item: any) => item.x_value),
        name: "Time",
      },
      yAxis: {
        type: "value",
        name: "Value",
      },
      series: [
        {
          type: "scatter",
          name: name,
          data: data.map((item: any) => [item.x_value, item.y_value]),
        },
      ],
    },
  };

const columns = [
  {
    title: tableCol.x,
    dataIndex: 'x_value',
    key: 'x_value',
  },
  {
    title: tableCol.y,
    dataIndex: 'y_value',
    key: 'y_value',
  },
];

const dataSources = data.map((item, index)=>({...item, key: index, }))


  return (
    <>
      {type === "table" ? (
        <Table
          dataSource={dataSources}
          columns={columns}
          pagination={false}
          scroll={{ y: 240 }}
          onRow={(record, rowIndex) => {
            return {
              onClick:insideModal? (event) => {
                handleBarClick(rowIndex);
              }: ()=>{}, // click row
            };
          }}
        />
      ) : (
        <ReactEcharts
          option={chartOptions[type]}
          // style={{ height: "100%", width: "100%" }}
          onEvents={{
            click: insideModal ? handleBarClick : handleBarClickWithoutModal,
          }}
        />
      )}
    </>
  );
};

export default Charts;
