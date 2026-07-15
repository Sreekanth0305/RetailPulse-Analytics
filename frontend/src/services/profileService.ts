import axios from "../api/axios";

export const getProfile = () => {

  return axios.get(
    "/users/profile",
    {
      headers: {
        Authorization:
          "Bearer " +
          localStorage.getItem("access_token"),
      },
    }
  );

};