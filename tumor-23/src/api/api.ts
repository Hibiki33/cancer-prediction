import axios from "./axio";

export const doPostPicture = (data: any) => {
    const formData = new URLSearchParams()
    formData.append('data', data)
    return axios.post('test/getParamData', formData);
}




