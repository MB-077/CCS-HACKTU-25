import axios from 'axios';
import { Idata } from './../Interface/Interfaces';

const apiKey = `http://127.0.0.1:8000`;
// const token = localStorage.getItem('token');

export const post = async (data: Idata, endpoint: string) => {
  try {
    const api = `${apiKey}/${endpoint}`;
    const response = await axios.post(api, data, {
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json, text/plain, */*',
      },
    });
    return response;
  } catch (error) {
    console.log(error);
    return error;
  }
};
