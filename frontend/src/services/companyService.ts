import axios from "../api/axios";

export const registerCompany = (data: any) => {

  return axios.post(
    "/companies/register",
    data
  );

};