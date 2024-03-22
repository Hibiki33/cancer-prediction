import axios from "./axio";

export const doPostPicture = (data: any) => {
    const formData = new FormData()
    formData.append('file', data)
    return axios.post('medicalCase/upload_picture/', formData);
}


