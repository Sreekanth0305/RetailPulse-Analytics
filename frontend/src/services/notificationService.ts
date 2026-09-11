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

// =========================================================
// Notification Interface
// =========================================================

export interface Notification {
  id: number;
  company_id: number;
  user_id: number | null;

  type: string | null;

  title: string;
  message: string;

  priority: string | null;

  resource_type: string | null;
  resource_id: number | null;

  is_read: boolean;

  created_at: string;
  read_at: string | null;
  expires_at: string | null;

  deduplication_key: string | null;
}

// =========================================================
// Notification List Response
// =========================================================

export interface NotificationListResponse {
  items: Notification[];

  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

// =========================================================
// Get Notifications
// =========================================================

export const getNotifications = async (
  page: number = 1,
  limit: number = 20,
  isRead?: boolean,
  type?: string,
  priority?: string
): Promise<NotificationListResponse> => {
  const response = await API.get("/notifications/", {
    params: {
      page,
      limit,
      is_read: isRead,
      notification_type: type,
      priority,
    },
  });

  return response.data;
};

// =========================================================
// Get Unread Count
// =========================================================

export const getUnreadCount = async (): Promise<number> => {
  const response = await API.get(
    "/notifications/unread-count"
  );

  return response.data.unread_count;
};

// =========================================================
// Mark One Notification As Read
// =========================================================

export const markNotificationAsRead = async (
  id: number
): Promise<Notification> => {
  const response = await API.patch(
    `/notifications/${id}/read`
  );

  return response.data;
};

// =========================================================
// Mark All Notifications As Read
// =========================================================

export const markAllNotificationsAsRead = async () => {
  const response = await API.patch(
    "/notifications/read-all"
  );

  return response.data;
};

// =========================================================
// Delete Notification
// =========================================================

export const deleteNotification = async (
  id: number
) => {
  const response = await API.delete(
    `/notifications/${id}`
  );

  return response.data;
};