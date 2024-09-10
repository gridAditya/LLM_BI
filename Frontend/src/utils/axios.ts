import axios, { AxiosRequestConfig } from "axios";

const requestConfig: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_APP_API_URL,
};

export const axiosInstance = axios.create(requestConfig);
