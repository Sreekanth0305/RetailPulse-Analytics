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