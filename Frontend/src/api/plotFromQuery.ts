import { axiosInstance } from "../utils/axios";

export const plotGraphFromQuery = async (query: string) => {
  const response = await axiosInstance.post("/questions", {
    message:query });
  console.log("returned results ",response.data);
  // setChartDataFromApi(response.data)
  return response.data;
};