import { apiPython } from "./api";

export const transcribeYoruba = async (data) => {
        const response = await apiPython.post('/transcribe-yoruba', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        });

        return response.data;
};

export const doublageYoruba = async (data) => {
    const response = await apiPython.post('/subtitute', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });

    return response.data;
};