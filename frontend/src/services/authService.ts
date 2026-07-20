import axios from "../api/axios";

export const login = (email: string, password: string) => {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  return axios.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export const logout = () => {

    const token = localStorage.getItem("access_token");

    return axios.post(
        "/auth/logout",
        {},
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};

export const getCurrentUser = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/auth/me", {

        headers: {

            Authorization: `Bearer ${token}`

        }

    });

};