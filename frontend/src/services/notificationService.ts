import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8001",
});

// Automatically attach JWT
API.interceptors.request.use((config) => {

  const token = localStorage.getItem("access_token");

  if (token) {

    config.headers.Authorization = `Bearer ${token}`;

  }

  return config;

});

// -----------------------------
// Get Notifications
// -----------------------------
export const getNotifications = async () => {

  const response = await API.get("/notifications/");

  return response.data;

};

// -----------------------------
// Mark As Read
// -----------------------------
export const markNotificationAsRead = async (
  id: number
) => {

  const response = await API.put(
    `/notifications/${id}`
  );

  return response.data;

};

// -----------------------------
// Delete Notification
// -----------------------------
export const deleteNotification = async (
  id: number
) => {

  const response = await API.delete(
    `/notifications/${id}`
  );

  return response.data;

};

// -------------------------
// Get Unread Count
// -------------------------
export const getUnreadCount = async () => {

  const notifications = await getNotifications();

  return notifications.filter(
    (notification: any) => !notification.is_read
  ).length;

};