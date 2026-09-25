import axios from "../api/axios";

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
};

// --------------------------------------------------
// Dashboard
// --------------------------------------------------

export const getDataQualityDashboard = async () => {
  const response = await axios.get(
    "/data-quality/dashboard",
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};

// --------------------------------------------------
// Run reconciliation
// --------------------------------------------------

export const runReconciliation = async () => {
  const response = await axios.post(
    "/data-quality/reconcile",
    {},
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};

// --------------------------------------------------
// Get issues
// --------------------------------------------------

export const getDataQualityIssues = async (
  params: {
    search?: string;
    issue_type?: string;
    severity?: string;
    module?: string;
    status?: string;
    page?: number;
    limit?: number;
  } = {}
) => {
  const response = await axios.get(
    "/data-quality/issues",
    {
      headers: getAuthHeaders(),
      params,
    }
  );

  return response.data;
};

// --------------------------------------------------
// Get issue details
// --------------------------------------------------

export const getDataQualityIssue = async (
  issueId: number
) => {
  const response = await axios.get(
    `/data-quality/issues/${issueId}`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};

// --------------------------------------------------
// Update issue status
// --------------------------------------------------

export const updateDataQualityIssueStatus = async (
  issueId: number,
  status: string,
  resolutionNote: string = ""
) => {
  const response = await axios.patch(
    `/data-quality/issues/${issueId}/status`,
    {
      status,
      resolution_note: resolutionNote,
    },
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};

// --------------------------------------------------
// Reconciliation history
// --------------------------------------------------

export const getReconciliationHistory = async (
  page: number = 1,
  limit: number = 10
) => {
  const response = await axios.get(
    "/data-quality/history",
    {
      headers: getAuthHeaders(),
      params: {
        page,
        limit,
      },
    }
  );

  return response.data;
};