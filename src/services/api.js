import axios from 'axios';

export const apiPython = axios.create({
    baseURL: import.meta.env.VITE_APP_API_PYTHON_URL, 
});

export const apiNode = axios.create({
    baseURL : import.meta.env.VITE_APP_API_NODE_URL,
})