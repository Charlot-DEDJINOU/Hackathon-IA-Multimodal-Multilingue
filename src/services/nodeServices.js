import { apiNode } from "./api";

export const getSubtitles = async (data) => {
    const response = await apiNode.post('/addSubtitles', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });
    console.log(response)
    return response.data;
};