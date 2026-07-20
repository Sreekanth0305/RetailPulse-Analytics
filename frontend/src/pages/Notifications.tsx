import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getNotifications,
  markNotificationAsRead,
  deleteNotification,
} from "../services/notificationService";

import "../styles/notification.css";

interface Notification {

  id: number;

  title: string;

  message: string;

  is_read: boolean;

  created_at: string;

}

function Notifications() {

  const [notifications, setNotifications] =
    useState<Notification[]>([]);

  const loadNotifications = async () => {

    try {

      const data =
        await getNotifications();

      setNotifications(data);

    }

    catch (error) {

      console.log(error);

    }

  };

  useEffect(() => {

    loadNotifications();

  }, []);

  const handleRead = async (
    id: number
  ) => {

    try {

      await markNotificationAsRead(id);

      await loadNotifications();

    }

    catch (error) {

      console.log(error);

    }

  };

  const handleDelete = async (
    id: number
  ) => {

    const confirmDelete =
      window.confirm(
        "Delete this notification?"
      );

    if (!confirmDelete) return;

    try {

      await deleteNotification(id);

      await loadNotifications();

    }

    catch (error) {

      console.log(error);

    }

  };

  return (

    <>

      <Sidebar />

      <Navbar />

      <div className="notifications">

        <div className="notification-header">

          <h2>

            Notifications

          </h2>

        </div>

        {

          notifications.length === 0 ? (

            <div className="empty">

              No Notifications Available

            </div>

          ) : (

            notifications.map((notification) => (

              <div

                key={notification.id}

                className={`notification-card ${
                  notification.is_read
                    ? "read"
                    : "unread"
                }`}

              >

                <div className="notification-content">

                  <h3>

                    {notification.title}

                  </h3>

                  <p>

                    {notification.message}

                  </p>

                  <small>

                    {new Date(
                      notification.created_at
                    ).toLocaleString()}

                  </small>

                </div>

                <div className="notification-actions">

                  {

                    !notification.is_read && (

                      <button

                        className="read-btn"

                        onClick={() =>
                          handleRead(
                            notification.id
                          )
                        }

                      >

                        Mark Read

                      </button>

                    )

                  }

                  <button

                    className="delete-btn"

                    onClick={() =>
                      handleDelete(
                        notification.id
                      )
                    }

                  >

                    Delete

                  </button>

                </div>

              </div>

            ))

          )

        }

      </div>

    </>

  );

}

export default Notifications;