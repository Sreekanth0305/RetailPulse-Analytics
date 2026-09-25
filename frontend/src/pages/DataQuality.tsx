import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getDataQualityDashboard,
  getDataQualityIssues,
  getDataQualityIssue,
  updateDataQualityIssueStatus,
  runReconciliation,
  getReconciliationHistory,
} from "../services/dataQualityService";

import "../styles/dataQuality.css";

interface DashboardData {
  total_records_checked: number;
  valid_records: number;
  warnings: number;
  errors: number;
  unresolved_issues: number;
  last_reconciliation_time: string | null;
}

interface DataQualityIssue {
  id: number;
  issue_type: string;
  severity: string;
  module: string;
  affected_record: string | null;
  description: string;
  detected_at: string;
  status: string;
  resolved_at: string | null;
  resolved_by: number | null;
  resolution_note: string | null;
}

interface ReconciliationHistory {
  id: number;
  execution_id: string;
  started_at: string;
  completed_at: string | null;
  triggered_by: number | null;
  records_checked: number;
  issues_detected: number;
  issues_resolved: number;
  failed_checks: number;
  execution_status: string;
  error_message: string | null;
}

const DataQuality = () => {
  const [dashboard, setDashboard] = useState<DashboardData>({
    total_records_checked: 0,
    valid_records: 0,
    warnings: 0,
    errors: 0,
    unresolved_issues: 0,
    last_reconciliation_time: null,
  });

  const [issues, setIssues] = useState<DataQualityIssue[]>([]);
  const [history, setHistory] = useState<ReconciliationHistory[]>([]);

  const [selectedIssue, setSelectedIssue] =
    useState<DataQualityIssue | null>(null);

  const [search, setSearch] = useState("");
  const [issueType, setIssueType] = useState("");
  const [severity, setSeverity] = useState("");
  const [module, setModule] = useState("");
  const [status, setStatus] = useState("");

  const [issuePage, setIssuePage] = useState(1);
  const [historyPage, setHistoryPage] = useState(1);

  const [issueTotal, setIssueTotal] = useState(0);
  const [historyTotal, setHistoryTotal] = useState(0);

  const [loading, setLoading] = useState(false);
  const [reconciling, setReconciling] = useState(false);

  const [error, setError] = useState("");

  const [resolutionNote, setResolutionNote] = useState("");

  const issueLimit = 10;
  const historyLimit = 10;

  // -----------------------------------------
  // Load dashboard
  // -----------------------------------------

  const loadDashboard = async () => {
    try {
      const data = await getDataQualityDashboard();
      setDashboard(data);
    } catch (err) {
      console.error("Failed to load dashboard:", err);
      setError("Failed to load data quality dashboard.");
    }
  };

  // -----------------------------------------
  // Load issues
  // -----------------------------------------

  const loadIssues = async () => {
    try {
      setLoading(true);

      const data = await getDataQualityIssues({
        search: search || undefined,
        issue_type: issueType || undefined,
        severity: severity || undefined,
        module: module || undefined,
        status: status || undefined,
        page: issuePage,
        limit: issueLimit,
      });

      /*
        The backend may return either:

        {
          items: [],
          total: 0
        }

        or directly an array.

        This handles both cases.
      */

      if (Array.isArray(data)) {
        setIssues(data);
        setIssueTotal(data.length);
      } else {
        setIssues(data.items || data.results || []);
        setIssueTotal(data.total || 0);
      }
    } catch (err) {
      console.error("Failed to load issues:", err);
      setError("Failed to load data quality issues.");
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------
  // Load reconciliation history
  // -----------------------------------------

  const loadHistory = async () => {
    try {
      const data = await getReconciliationHistory(
        historyPage,
        historyLimit
      );

      if (Array.isArray(data)) {
        setHistory(data);
        setHistoryTotal(data.length);
      } else {
        setHistory(data.items || data.results || []);
        setHistoryTotal(data.total || 0);
      }
    } catch (err) {
      console.error("Failed to load reconciliation history:", err);
      setError("Failed to load reconciliation history.");
    }
  };

  // -----------------------------------------
  // Initial loading
  // -----------------------------------------

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    loadIssues();
  }, [search, issueType, severity, module, status, issuePage]);

  useEffect(() => {
    loadHistory();
  }, [historyPage]);

  // -----------------------------------------
  // Run reconciliation
  // -----------------------------------------

  const handleRunReconciliation = async () => {
    try {
      setReconciling(true);
      setError("");

      await runReconciliation();

      // Refresh dashboard, issues and history
      await Promise.all([
        loadDashboard(),
        loadIssues(),
        loadHistory(),
      ]);
    } catch (err) {
      console.error("Reconciliation failed:", err);
      setError("Reconciliation failed. Please try again.");
    } finally {
      setReconciling(false);
    }
  };

  // -----------------------------------------
  // View issue details
  // -----------------------------------------

  const handleViewIssue = async (issueId: number) => {
    try {
      const data = await getDataQualityIssue(issueId);
      setSelectedIssue(data);
      setResolutionNote(data.resolution_note || "");
    } catch (err) {
      console.error("Failed to load issue details:", err);
      setError("Failed to load issue details.");
    }
  };

  // -----------------------------------------
  // Update issue status
  // -----------------------------------------

  const handleStatusUpdate = async (newStatus: string) => {
    if (!selectedIssue) {
      return;
    }

    try {
      setError("");

      await updateDataQualityIssueStatus(
        selectedIssue.id,
        newStatus,
        resolutionNote
      );

      // Refresh issue details and dashboard
      const updatedIssue = await getDataQualityIssue(
        selectedIssue.id
      );

      setSelectedIssue(updatedIssue);

      await Promise.all([
        loadDashboard(),
        loadIssues(),
        loadHistory(),
      ]);
    } catch (err) {
      console.error("Failed to update issue:", err);
      setError("Failed to update issue status.");
    }
  };

  // -----------------------------------------
  // Clear filters
  // -----------------------------------------

  const clearFilters = () => {
    setSearch("");
    setIssueType("");
    setSeverity("");
    setModule("");
    setStatus("");
    setIssuePage(1);
  };

  // -----------------------------------------
  // Pagination
  // -----------------------------------------

  const totalIssuePages = Math.ceil(
    issueTotal / issueLimit
  );

  const totalHistoryPages = Math.ceil(
    historyTotal / historyLimit
  );

  return (
    <>
      <Sidebar />
      <Navbar />

      <div className="data-quality-page">

        {/* ---------------------------------- */}
        {/* Header */}
        {/* ---------------------------------- */}

        <div className="data-quality-header">
          <div>
            <h1>Data Quality & Reconciliation</h1>

            <p>
              Monitor data consistency across sales, inventory,
              products, customers and reports.
            </p>
          </div>

          <button
            type="button"
            onClick={handleRunReconciliation}
            disabled={reconciling}
          >
            {reconciling
              ? "Running Reconciliation..."
              : "Run Reconciliation"}
          </button>
        </div>

        {/* ---------------------------------- */}
        {/* Error */}
        {/* ---------------------------------- */}

        {error && (
          <div className="data-quality-error">
            {error}
          </div>
        )}

        {/* ---------------------------------- */}
        {/* KPI Cards */}
        {/* ---------------------------------- */}

        <div className="data-quality-kpi-grid">

          <div className="data-quality-card">
            <h3>Total Records Checked</h3>
            <strong>{dashboard.total_records_checked}</strong>
          </div>

          <div className="data-quality-card">
            <h3>Valid Records</h3>
            <strong>{dashboard.valid_records}</strong>
          </div>

          <div className="data-quality-card">
            <h3>Warnings</h3>
            <strong>{dashboard.warnings}</strong>
          </div>

          <div className="data-quality-card">
            <h3>Errors</h3>
            <strong>{dashboard.errors}</strong>
          </div>

          <div className="data-quality-card">
            <h3>Unresolved Issues</h3>
            <strong>{dashboard.unresolved_issues}</strong>
          </div>

          <div className="data-quality-card">
            <h3>Last Reconciliation</h3>

            <strong>
              {dashboard.last_reconciliation_time
                ? new Date(
                    dashboard.last_reconciliation_time
                  ).toLocaleString()
                : "Never"}
            </strong>
          </div>

        </div>

        {/* ---------------------------------- */}
        {/* Filters */}
        {/* ---------------------------------- */}

        <div className="data-quality-filters">

          <input
            type="text"
            placeholder="Search issues..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setIssuePage(1);
            }}
          />

          <select
            value={issueType}
            onChange={(e) => {
              setIssueType(e.target.value);
              setIssuePage(1);
            }}
          >
            <option value="">All Issue Types</option>
            <option value="Invalid Product">
              Invalid Product
            </option>
            <option value="Invalid Customer">
              Invalid Customer
            </option>
            <option value="Duplicate SKU">
              Duplicate SKU
            </option>
            <option value="Invalid SKU">
              Invalid SKU
            </option>
            <option value="Customer Information">
              Customer Information
            </option>
            <option value="Inventory Movement">
              Inventory Movement
            </option>
            <option value="Sales Inventory">
              Sales Inventory
            </option>
          </select>

          <select
            value={severity}
            onChange={(e) => {
              setSeverity(e.target.value);
              setIssuePage(1);
            }}
          >
            <option value="">All Severities</option>
            <option value="Error">Error</option>
            <option value="Warning">Warning</option>
          </select>

          <select
            value={module}
            onChange={(e) => {
              setModule(e.target.value);
              setIssuePage(1);
            }}
          >
            <option value="">All Modules</option>
            <option value="Products">Products</option>
            <option value="Customers">Customers</option>
            <option value="Inventory">Inventory</option>
            <option value="Sales">Sales</option>
          </select>

          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setIssuePage(1);
            }}
          >
            <option value="">All Statuses</option>
            <option value="Open">Open</option>
            <option value="Investigating">
              Investigating
            </option>
            <option value="Resolved">Resolved</option>
            <option value="Ignored">Ignored</option>
          </select>

          <button
            type="button"
            onClick={clearFilters}
          >
            Clear
          </button>

        </div>

        {/* ---------------------------------- */}
        {/* Issues Table */}
        {/* ---------------------------------- */}

        <div className="data-quality-section">

          <div className="section-header">
            <h2>Data Quality Issues</h2>
          </div>

          {loading ? (
            <p>Loading issues...</p>
          ) : issues.length === 0 ? (
            <p>No data quality issues found.</p>
          ) : (
            <div className="data-quality-table-wrapper">

              <table className="data-quality-table">

                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Issue Type</th>
                    <th>Severity</th>
                    <th>Module</th>
                    <th>Affected Record</th>
                    <th>Description</th>
                    <th>Detected At</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {issues.map((issue) => (
                    <tr key={issue.id}>

                      <td>{issue.id}</td>

                      <td>{issue.issue_type}</td>

                      <td>
                        <span
                          className={`severity-${issue.severity.toLowerCase()}`}
                        >
                          {issue.severity}
                        </span>
                      </td>

                      <td>{issue.module}</td>

                      <td>
                        {issue.affected_record || "-"}
                      </td>

                      <td>{issue.description}</td>

                      <td>
                        {new Date(
                          issue.detected_at
                        ).toLocaleString()}
                      </td>

                      <td>{issue.status}</td>

                      <td>
                        <button
                          type="button"
                          onClick={() =>
                            handleViewIssue(issue.id)
                          }
                        >
                          View
                        </button>
                      </td>

                    </tr>
                  ))}
                </tbody>

              </table>

            </div>
          )}

          {/* Issue Pagination */}

          {totalIssuePages > 1 && (
            <div className="pagination">

              <button
                type="button"
                disabled={issuePage === 1}
                onClick={() =>
                  setIssuePage((prev) => prev - 1)
                }
              >
                Previous
              </button>

              <span>
                Page {issuePage} of {totalIssuePages}
              </span>

              <button
                type="button"
                disabled={issuePage === totalIssuePages}
                onClick={() =>
                  setIssuePage((prev) => prev + 1)
                }
              >
                Next
              </button>

            </div>
          )}

        </div>

        {/* ---------------------------------- */}
        {/* Reconciliation History */}
        {/* ---------------------------------- */}

        <div className="data-quality-section">

          <div className="section-header">
            <h2>Reconciliation History</h2>
          </div>

          {history.length === 0 ? (
            <p>No reconciliation history found.</p>
          ) : (
            <div className="data-quality-table-wrapper">

              <table className="data-quality-table">

                <thead>
                  <tr>
                    <th>Execution ID</th>
                    <th>Started</th>
                    <th>Completed</th>
                    <th>Records Checked</th>
                    <th>Issues Detected</th>
                    <th>Issues Resolved</th>
                    <th>Failed Checks</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {history.map((item) => (
                    <tr key={item.id}>

                      <td>{item.execution_id}</td>

                      <td>
                        {new Date(
                          item.started_at
                        ).toLocaleString()}
                      </td>

                      <td>
                        {item.completed_at
                          ? new Date(
                              item.completed_at
                            ).toLocaleString()
                          : "-"}
                      </td>

                      <td>{item.records_checked}</td>

                      <td>{item.issues_detected}</td>

                      <td>{item.issues_resolved}</td>

                      <td>{item.failed_checks}</td>

                      <td>{item.execution_status}</td>

                    </tr>
                  ))}
                </tbody>

              </table>

            </div>
          )}

          {/* History Pagination */}

          {totalHistoryPages > 1 && (
            <div className="pagination">

              <button
                type="button"
                disabled={historyPage === 1}
                onClick={() =>
                  setHistoryPage((prev) => prev - 1)
                }
              >
                Previous
              </button>

              <span>
                Page {historyPage} of {totalHistoryPages}
              </span>

              <button
                type="button"
                disabled={historyPage === totalHistoryPages}
                onClick={() =>
                  setHistoryPage((prev) => prev + 1)
                }
              >
                Next
              </button>

            </div>
          )}

        </div>

        {/* ---------------------------------- */}
        {/* Issue Details Modal */}
        {/* ---------------------------------- */}

        {selectedIssue && (
          <div className="issue-modal-overlay">

            <div className="issue-modal">

              <div className="issue-modal-header">
                <h2>
                  Issue #{selectedIssue.id}
                </h2>

                <button
                  type="button"
                  onClick={() =>
                    setSelectedIssue(null)
                  }
                >
                  X
                </button>
              </div>

              <div className="issue-details">

                <p>
                  <strong>Issue Type:</strong>{" "}
                  {selectedIssue.issue_type}
                </p>

                <p>
                  <strong>Severity:</strong>{" "}
                  {selectedIssue.severity}
                </p>

                <p>
                  <strong>Module:</strong>{" "}
                  {selectedIssue.module}
                </p>

                <p>
                  <strong>Affected Record:</strong>{" "}
                  {selectedIssue.affected_record || "-"}
                </p>

                <p>
                  <strong>Description:</strong>{" "}
                  {selectedIssue.description}
                </p>

                <p>
                  <strong>Detected At:</strong>{" "}
                  {new Date(
                    selectedIssue.detected_at
                  ).toLocaleString()}
                </p>

                <p>
                  <strong>Current Status:</strong>{" "}
                  {selectedIssue.status}
                </p>

                {selectedIssue.resolution_note && (
                  <p>
                    <strong>Resolution Note:</strong>{" "}
                    {selectedIssue.resolution_note}
                  </p>
                )}

              </div>

              {/* Resolution Note */}

              <div className="resolution-form">

                <label>
                  Resolution Note
                </label>

                <textarea
                  value={resolutionNote}
                  onChange={(e) =>
                    setResolutionNote(e.target.value)
                  }
                  placeholder="Enter resolution note..."
                  rows={4}
                />

              </div>

              {/* Status buttons */}

              <div className="issue-status-actions">

                <button
                  type="button"
                  onClick={() =>
                    handleStatusUpdate("Investigating")
                  }
                >
                  Investigating
                </button>

                <button
                  type="button"
                  onClick={() =>
                    handleStatusUpdate("Resolved")
                  }
                >
                  Resolve
                </button>

                <button
                  type="button"
                  onClick={() =>
                    handleStatusUpdate("Ignored")
                  }
                >
                  Ignore
                </button>

              </div>

            </div>

          </div>
        )}

      </div>
    </>
  );
};

export default DataQuality;