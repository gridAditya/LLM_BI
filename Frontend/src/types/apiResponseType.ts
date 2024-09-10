export interface PlotDataType {
  sql_query: string;
  plot_type_name: string;
  plot_title: string;
  x: string; 
  y: string;
  data: { x_value: string , y_value:number}[];
  legend: string[];
  description: string;
}
