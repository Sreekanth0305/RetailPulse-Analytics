import axios from "../api/axios";

// =========================================================
// AUTH HEADERS
// =========================================================

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
};


// =========================================================
// TYPES
// =========================================================

export interface WorkflowRequest {
  id: number;
  request_type: string;
  requested_by: number;
  company_id: number;
  related_record?: string;
  requested_changes?: Record<string, any>;
  reason?: string;
  status: string;
  priority?: string;
  created_at: string;
  updated_at?: string;
}


// =========================================================
// CREATE REQUEST
// =========================================================

export const createWorkflowRequest = async (
  data: {
    request_type: string;
    related_record?: string;
    requested_changes?: Record<string, any>;
    reason?: string;
    priority?: string;
  }
) => {
  const response = await axios.post(
    "/workflows",
    data,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// SUBMIT REQUEST
// =========================================================

export const submitWorkflowRequest = async (
  workflowId: number
) => {
  const response = await axios.post(
    `/workflows/${workflowId}/submit`,
    {},
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// LIST REQUESTS
// =========================================================

export const getWorkflowRequests = async (
  requestType?: string,
  status?: string,
  search?: string,
  page: number = 1,
  limit: number = 10
) => {
  const response = await axios.get(
    "/workflows",
    {
      headers: getAuthHeaders(),

      params: {
        request_type:
          requestType || undefined,

        status:
          status || undefined,

        search:
          search || undefined,

        page,
        limit,
      },
    }
  );

  return response.data;
};


// =========================================================
// GET DETAILS
// =========================================================

export const getWorkflowRequest = async (
  workflowId: number
) => {
  const response = await axios.get(
    `/workflows/${workflowId}`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// APPROVE
// =========================================================

export const approveWorkflowRequest = async (
  workflowId: number,
  comment: string
) => {
  const response = await axios.post(
    `/workflows/${workflowId}/approve`,
    {
      comment,
    },
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// REJECT
// =========================================================

export const rejectWorkflowRequest = async (
  workflowId: number,
  comment: string
) => {
  const response = await axios.post(
    `/workflows/${workflowId}/reject`,
    {
      comment,
    },
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// CANCEL
// =========================================================

export const cancelWorkflowRequest = async (
  workflowId: number,
  comment: string
) => {
  const response = await axios.post(
    `/workflows/${workflowId}/cancel`,
    {
      comment,
    },
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// HISTORY
// =========================================================

export const getWorkflowHistory = async (
  workflowId: number
) => {
  const response = await axios.get(
    `/workflows/${workflowId}/history`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// CREATE WORKFLOW CONFIGURATION
// =========================================================

export const createWorkflowConfig = async (
  data: {
    request_type: string;
    approver_role: string;
    approval_required: boolean;
    allow_self_approval: boolean;
    is_active: boolean;
  }
) => {
  const response = await axios.post(
    "/workflows/config",
    data,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// GET WORKFLOW CONFIGURATIONS
// =========================================================

export const getWorkflowConfigs = async () => {
  const response = await axios.get(
    "/workflows/config/list",
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};