"use client"
import { useState } from 'react';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'; // Add more request methods if needed

const useApi = <T>() => {
   const [data, setData] = useState<T | null>(null);
   const [error, setError] = useState<string | null>(null);
   const [loading, setLoading] = useState(false);

   const basePath = process.env.BASE_PATH || 'http://localhost:8000/'; // Add base path from process.env
   
   const makeRequest = async (config: AxiosRequestConfig) => {
      setLoading(true);
      try {
         const response: AxiosResponse<T> = await axios({
            ...config,
            url: `${basePath}${config.url}`,
            method: config.method as RequestMethod,
         });
         setData(response.data);
      } catch (error) {
         setError('Failed to fetch data');
      } finally {
         setLoading(false);
      }
   };

   return { data, error, loading, makeRequest };
};

export default useApi;
