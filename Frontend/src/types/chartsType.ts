export interface ChartsProps {
  name: string;
  type: string;
  data: { x_value: string; y_value: number }[]
  insideModal: boolean;
  setChartModal: React.Dispatch<React.SetStateAction<boolean>>;
  tableCol: { x: string, y: string }
}
