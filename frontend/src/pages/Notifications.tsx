import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getNotifications,
  markNotificationAsRead,
  deleteNotification,
  markAllNotificationsAsRead,
  type Notification,
} from "../services/notificationService";

import "../styles/notification.css";

function Notifications() {

  const navigate = useNavigate();

  const [notifications, setNotifications] =
    useState<Notification[]>([]);

  const [page, setPage] = useState(1);

  const [totalPages, setTotalPages] = useState(1);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [readFilter, setReadFilter] =
    useState<boolean | undefined>(undefined);
  
  const [typeFilter, setTypeFilter] =
    useState<string | undefined>(undefined);
  
  const [priorityFilter, setPriorityFilter] =
    useState<string | undefined>(undefined);

  // ---------------------------------------------------------
  // Load Notifications
  // ---------------------------------------------------------

  const loadNotifications = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getNotifications(
        page,
        5,
        readFilter,
        typeFilter,
        priorityFilter
      );
      
      setNotifications(data.items);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.log(error);
      setError("Unable to load notifications.");
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------------------------
// Notification Resource Navigation
// ---------------------------------------------------------

  const handleNotificationClick = (
    notification: Notification
  ) => {
  
    switch (notification.resource_type) {
  
      case "Inventory":
        navigate("/inventory");
        break;
  
      case "ImportHistory":
        navigate("/data-import");
        break;
  
      case "Sales":
  
        if (notification.resource_id !== null) {
          navigate(
            `/sales/${notification.resource_id}`
          );
        } else {
          navigate("/sales");
        }
  
        break;
  
      case "Product":
        navigate("/products");
        break;
  
      case "Analytics":
        navigate("/analytics");
        break;
  
      default:
        break;
    }
  };

  // ---------------------------------------------------------
  // Initial Load
  // ---------------------------------------------------------

  useEffect(() => {
    loadNotifications();
  }, [
    page,
    readFilter,
    typeFilter,
    priorityFilter,
  ]);

  useEffect(() => {
    setPage(1);
  }, [
    readFilter,
    typeFilter,
    priorityFilter,
  ]);

  // ---------------------------------------------------------
  // Mark One Notification As Read
  // ---------------------------------------------------------

  const handleRead = async (id: number) => {
    try {
      const updatedNotification =
        await markNotificationAsRead(id);

      setNotifications((currentNotifications) =>
        currentNotifications.map((notification) =>
          notification.id === id
            ? updatedNotification
            : notification
        )
      );
    } catch (error) {
      console.log(error);
      setError("Unable to mark notification as read.");
    }
  };

  // ---------------------------------------------------------
  // Mark All Notifications As Read
  // ---------------------------------------------------------

  const handleMarkAllAsRead = async () => {
    try {
      await markAllNotificationsAsRead();

      setNotifications((currentNotifications) =>
        currentNotifications.map((notification) => ({
          ...notification,
          is_read: true,
          read_at: new Date().toISOString(),
        }))
      );
    } catch (error) {
      console.log(error);
      setError("Unable to mark all notifications as read.");
    }
  };

  // ---------------------------------------------------------
  // Delete Notification
  // ---------------------------------------------------------

  const handleDelete = async (id: number) => {
    const confirmDelete = window.confirm(
      "Delete this notification?"
    );

    if (!confirmDelete) return;

    try {
      await deleteNotification(id);

      setNotifications((currentNotifications) =>
        currentNotifications.filter(
          (notification) =>
            notification.id !== id
        )
      );
    } catch (error) {
      console.log(error);
      setError("Unable to delete notification.");
    }
  };

  // ---------------------------------------------------------
  // Render
  // ---------------------------------------------------------

  return (
    <>
      <Sidebar />

      <Navbar />

      <div className="notifications">

        <div className="notification-header">

          <h2>
            Notifications
          </h2>

          {notifications.some(
            (notification) =>
              !notification.is_read
          ) && (
            <button
              className="read-btn"
              onClick={handleMarkAllAsRead}
            >
              Mark All as Read
            </button>
          )}

        </div>

        {/* -------------------------------------------------
            Notification Filters
        ------------------------------------------------- */}
        
        <div className="notification-filters">
        
          <div className="filter-group">
        
            <label>
              Status
            </label>
        
            <select
              value={
                readFilter === undefined
                  ? "all"
                  : readFilter
                  ? "read"
                  : "unread"
              }
              onChange={(event) => {
        
                const value = event.target.value;
        
                if (value === "all") {
                  setReadFilter(undefined);
                } else if (value === "read") {
                  setReadFilter(true);
                } else {
                  setReadFilter(false);
                }
        
              }}
            >
              <option value="all">
                All
              </option>
        
              <option value="unread">
                Unread
              </option>
        
              <option value="read">
                Read
              </option>
        
            </select>
        
          </div>
        
        
          <div className="filter-group">
        
            <label>
              Type
            </label>
        
            <select
              value={typeFilter ?? ""}
              onChange={(event) => {
        
                setTypeFilter(
                  event.target.value || undefined
                );
        
              }}
            >
        
              <option value="">
                All Types
              </option>
        
              <option value="Stockout Risk">
                Stockout Risk
              </option>
        
              <option value="Low Stock">
                Low Stock
              </option>
        
              <option value="Overstock">
                Overstock
              </option>
        
              <option value="Import Completed">
                Import Completed
              </option>
        
              <option value="Import Failed">
                Import Failed
              </option>
        
              <option value="Sales Alert">
                Sales Alert
              </option>
        
              <option value="System Alert">
                System Alert
              </option>
        
            </select>
        
          </div>
        
        
          <div className="filter-group">
        
            <label>
              Priority
            </label>
        
            <select
              value={priorityFilter ?? ""}
              onChange={(event) => {
        
                setPriorityFilter(
                  event.target.value || undefined
                );
        
              }}
            >
        
              <option value="">
                All Priorities
              </option>
        
              <option value="Low">
                Low
              </option>
        
              <option value="Medium">
                Medium
              </option>
        
              <option value="High">
                High
              </option>
        
              <option value="Critical">
                Critical
              </option>
        
            </select>
        
          </div>
        
        </div>

        {/* -------------------------------------------------
            Loading State
        ------------------------------------------------- */}

        {loading && (
          <div className="empty">
            Loading notifications...
          </div>
        )}

        {/* -------------------------------------------------
            Error State
        ------------------------------------------------- */}

        {!loading && error && (
          <div className="empty">
            {error}
          </div>
        )}

        {/* -------------------------------------------------
            Empty State
        ------------------------------------------------- */}

        {!loading &&
          !error &&
          notifications.length === 0 && (
            <div className="empty">
              No Notifications Available
            </div>
          )}

        {/* -------------------------------------------------
            Notification List
        ------------------------------------------------- */}

        {!loading &&
          !error &&
          notifications.length > 0 && (
            <>
              {notifications.map((notification) => (
  
                <div
                  key={notification.id}
                  className={`notification-card ${
                    notification.is_read
                      ? "read"
                      : "unread"
                  }`}
                  onClick={() =>
                    handleNotificationClick(notification)
                  }
                >
  
                  <div className="notification-content">
  
                    <h3>
                      {notification.title}
                    </h3>
  
                    <p>
                      {notification.message}
                    </p>
  
                    {notification.type && (
                      <p>
                        <strong>
                          Type:
                        </strong>{" "}
                        {notification.type}
                      </p>
                    )}
  
                    {notification.priority && (
                      <p>
                        <strong>
                          Priority:
                        </strong>{" "}
                        {notification.priority}
                      </p>
                    )}
  
                    {notification.resource_type && (
                      <p>
                        <strong>
                          Resource:
                        </strong>{" "}
                        {notification.resource_type}
  
                        {notification.resource_id !== null &&
                          ` #${notification.resource_id}`}
                      </p>
                    )}
  
                    <small>
                      {new Date(
                        notification.created_at
                      ).toLocaleString()}
                    </small>
  
                  </div>
  
                  <div className="notification-actions">
  
                    {!notification.is_read && (
                      <button
                        className="read-btn"
                        onClick={(event) => {
                          event.stopPropagation();
                        
                          handleRead(notification.id);
                        }}
                      >
                        Mark Read
                      </button>
                    )}
  
                    <button
                      className="delete-btn"
                      onClick={(event) => {
                        event.stopPropagation();
                      
                        handleDelete(notification.id);
                      }}
                    >
                      Delete
                    </button>
  
                  </div>
  
                </div>
  
              ))}
  
              <div className="notification-pagination">
  
                <button
                  className="pagination-btn"
                  disabled={page === 1}
                  onClick={() => setPage((currentPage) => currentPage - 1)}
                >
                  Previous
                </button>
              
                <span>
                  Page {page} of {totalPages}
                </span>
              
                <button
                  className="pagination-btn"
                  disabled={page === totalPages}
                  onClick={() => setPage((currentPage) => currentPage + 1)}
                >
                  Next
                </button>
              
              </div>
            </>
          )}

      </div>
    </>
  );
}

export default Notifications;