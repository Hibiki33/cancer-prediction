import axios from "./axio";

export const doPostPicture = (data: any) => {
    const formData = new URLSearchParams()
    formData.append('data', data)
    return axios.post('test/getParamData', formData);
}


export const doGetTest = () => {
    return axios.get('posts/1');
}

export const postMerge = (data: FormData) => {
    return axios.post('posts/1', data);
}

export const doUpload = (data: FormData) => {
    return axios.post('posts/1', data);
}
