import { useEffect, useState } from "react";

import {
  createScheduledReport,
  getScheduledReports,
  updateScheduledReportStatus,
  deleteScheduledReport,
} from "../services/scheduledReportService";

import type {
  ScheduledReport,
} from "../services/scheduledReportService";

interface ScheduledReportsProps {
  reportTypes: string[];
  filters: Record<string, any>;
  getAppliedFilters: () => string[];
}

const ScheduledReports = ({
  reportTypes,
  filters,
  getAppliedFilters,
}: ScheduledReportsProps) => {
  const [scheduledReports, setScheduledReports] =
    useState<ScheduledReport[]>([]);

  const [showForm, setShowForm] = useState(false);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [scheduleForm, setScheduleForm] = useState({
    report_type: "",
    frequency: "Daily",
    execution_time: "09:00",
    recipients: "",
    export_format: "CSV",
  });

  // ---------------------------------------------------------
  // Load Scheduled Reports
  // ---------------------------------------------------------

  const loadScheduledReports = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getScheduledReports();

      setScheduledReports(response.data);
    } catch (err) {
      console.error(err);

      setError(
        "Failed to load scheduled reports."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadScheduledReports();
  }, []);

  // ---------------------------------------------------------
  // Create Scheduled Report
  // ---------------------------------------------------------

  const handleCreateSchedule = async () => {
    if (!scheduleForm.report_type) {
      setError("Please select a report type.");
      return;
    }

    if (!scheduleForm.recipients.trim()) {
      setError(
        "Please enter at least one recipient."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = {
        report_type: scheduleForm.report_type,

        filters: {
          ...filters,
        },

        frequency: scheduleForm.frequency,

        execution_time:
          scheduleForm.execution_time,

        recipients:
          [scheduleForm.recipients],

        export_format:
          scheduleForm.export_format,

        is_active: true,
      };

      await createScheduledReport(data);

      setScheduleForm({
        report_type: "",
        frequency: "Daily",
        execution_time: "09:00",
        recipients: "",
        export_format: "CSV",
      });

      setShowForm(false);

      await loadScheduledReports();
    } catch (err) {
      console.error(err);

      setError(
        "Failed to create scheduled report."
      );
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------------------------
  // Enable / Disable
  // ---------------------------------------------------------

  const handleToggleSchedule = async (
    id: number,
    currentStatus: boolean
  ) => {
    try {
      setError("");

      await updateScheduledReportStatus(
        id,
        !currentStatus
      );

      await loadScheduledReports();
    } catch (err) {
      console.error(err);

      setError(
        "Failed to update scheduled report status."
      );
    }
  };

  // ---------------------------------------------------------
  // Delete
  // ---------------------------------------------------------

  const handleDeleteSchedule = async (
    id: number
  ) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this scheduled report?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await deleteScheduledReport(id);

      await loadScheduledReports();
    } catch (err) {
      console.error(err);

      setError(
        "Failed to delete scheduled report."
      );
    }
  };

  return (
    <div className="scheduled-reports-section">

      {/* -------------------------------------------------- */}
      {/* Header */}
      {/* -------------------------------------------------- */}

      <div className="scheduled-reports-header">

        <div>
          <h2>Scheduled Reports</h2>

          <p>
            Create and manage recurring reports.
          </p>
        </div>

        <button
          className="schedule-report-btn"
          onClick={() =>
            setShowForm(!showForm)
          }
        >
          {showForm
            ? "Close Scheduler"
            : "Schedule Report"}
        </button>

      </div>

      {/* -------------------------------------------------- */}
      {/* Error */}
      {/* -------------------------------------------------- */}

      {error && (
        <div className="schedule-error">
          {error}
        </div>
      )}

      {/* -------------------------------------------------- */}
      {/* Schedule Form */}
      {/* -------------------------------------------------- */}

      {showForm && (
        <div className="schedule-form">

          <div className="schedule-form-header">
            <h3>Create Scheduled Report</h3>

            <p>
              The currently selected report filters
              will be saved with this schedule.
            </p>
          </div>

          <div className="schedule-fields">

            {/* Report Type */}

            <div className="report-field">

              <label>
                Report Type
              </label>

              <select
                value={scheduleForm.report_type}
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    report_type:
                      e.target.value,
                  })
                }
              >
                <option value="">
                  Select Report
                </option>

                {reportTypes.map(
                  (reportType) => (
                    <option
                      key={reportType}
                      value={reportType}
                    >
                      {reportType}
                    </option>
                  )
                )}
              </select>

            </div>

            {/* Frequency */}

            <div className="report-field">

              <label>
                Frequency
              </label>

              <select
                value={scheduleForm.frequency}
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    frequency:
                      e.target.value,
                  })
                }
              >
                <option value="Daily">
                  Daily
                </option>

                <option value="Weekly">
                  Weekly
                </option>

                <option value="Monthly">
                  Monthly
                </option>
              </select>

            </div>

            {/* Execution Time */}

            <div className="report-field">

              <label>
                Execution Time
              </label>

              <input
                type="time"
                value={
                  scheduleForm.execution_time
                }
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    execution_time:
                      e.target.value,
                  })
                }
              />

            </div>

            {/* Format */}

            <div className="report-field">

              <label>
                Format
              </label>

              <select
                value={scheduleForm.export_format}
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    export_format:
                      e.target.value,
                  })
                }
              >
                <option value="CSV">
                  CSV
                </option>

                <option value="PDF">
                  PDF
                </option>
              </select>

            </div>

            {/* Recipients */}

            <div className="report-field schedule-recipient-field">

              <label>
                Recipients
              </label>

              <input
                type="text"
                placeholder="email1@example.com, email2@example.com"
                value={
                  scheduleForm.recipients
                }
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    recipients:
                      e.target.value,
                  })
                }
              />

              <small>
                Separate multiple recipients
                with commas.
              </small>

            </div>

          </div>

          {/* Current Filters */}

          <div className="schedule-filter-info">

            <strong>
              Current Filters
            </strong>

            {getAppliedFilters().length > 0 ? (
              <div className="schedule-filter-list">

                {getAppliedFilters().map(
                  (filter, index) => (
                    <span key={index}>
                      {filter}
                    </span>
                  )
                )}

              </div>
            ) : (
              <p>
                No filters applied. The
                scheduled report will use
                all available data.
              </p>
            )}

          </div>

          <button
            className="create-schedule-btn"
            onClick={handleCreateSchedule}
            disabled={loading}
          >
            {loading
              ? "Creating..."
              : "Create Schedule"}
          </button>

        </div>
      )}

      {/* -------------------------------------------------- */}
      {/* Scheduled Reports Table */}
      {/* -------------------------------------------------- */}

      {loading && !showForm ? (
        <div className="report-loading">
          Loading scheduled reports...
        </div>
      ) : scheduledReports.length === 0 ? (
        <div className="report-empty">
          No scheduled reports found.
        </div>
      ) : (
        <div className="scheduled-table-container">

          <table className="scheduled-table">

            <thead>
              <tr>
                <th>Report</th>
                <th>Frequency</th>
                <th>Execution Time</th>
                <th>Format</th>
                <th>Recipients</th>
                <th>Status</th>
                <th>Last Run</th>
                <th>Next Run</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {scheduledReports.map(
                (schedule) => (
                  <tr key={schedule.id}>

                    <td>
                      {schedule.report_type}
                    </td>

                    <td>
                      {schedule.frequency}
                    </td>

                    <td>
                      {schedule.execution_time}
                    </td>

                    <td>
                      {schedule.format}
                    </td>

                    <td>
                      {schedule.recipients}
                    </td>

                    <td>

                      <span
                        className={
                          schedule.is_active
                            ? "schedule-active"
                            : "schedule-inactive"
                        }
                      >
                        {schedule.is_active
                          ? "Active"
                          : "Inactive"}
                      </span>

                    </td>

                    <td>
                      {schedule.last_run_at
                        ? new Date(
                            schedule.last_run_at
                          ).toLocaleString()
                        : "Not generated"}
                    </td>

                    <td>
                      {schedule.next_run_at
                        ? new Date(
                            schedule.next_run_at
                          ).toLocaleString()
                        : "Not scheduled"}
                    </td>

                    <td>

                      <div className="schedule-actions">

                        <button
                          className="toggle-schedule-btn"
                          onClick={() =>
                            handleToggleSchedule(
                              schedule.id,
                              schedule.is_active
                            )
                          }
                        >
                          {schedule.is_active
                            ? "Disable"
                            : "Enable"}
                        </button>

                        <button
                          className="delete-schedule-btn"
                          onClick={() =>
                            handleDeleteSchedule(
                              schedule.id
                            )
                          }
                        >
                          Delete
                        </button>

                      </div>

                    </td>

                  </tr>
                )
              )}

            </tbody>

          </table>

        </div>
      )}

    </div>
  );
};

export default ScheduledReports;