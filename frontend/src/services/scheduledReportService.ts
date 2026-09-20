import axios from "../api/axios";

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
};

export interface ScheduledReport {
  id: number;
  company_id: number;
  report_type: string;
  filters: Record<string, any>;
  frequency: string;
  execution_time: string;
  recipients: string;
  format: string;
  is_active: boolean;
  last_run_at?: string | null;
  last_run_status?: string | null;
  next_run_at?: string | null;
  created_at?: string;
  updated_at?: string;
}

export const createScheduledReport = (
  data: any
) => {
  return axios.post(
    "/scheduled-reports/",
    data,
    {
      headers: getAuthHeaders(),
    }
  );
};

export const getScheduledReports = () => {
  return axios.get(
    "/scheduled-reports/",
    {
      headers: getAuthHeaders(),
    }
  );
};

export const getScheduledReport = (
  id: number
) => {
  return axios.get(
    `/scheduled-reports/${id}`,
    {
      headers: getAuthHeaders(),
    }
  );
};

export const updateScheduledReport = (
  id: number,
  data: any
) => {
  return axios.put(
    `/scheduled-reports/${id}`,
    data,
    {
      headers: getAuthHeaders(),
    }
  );
};

export const updateScheduledReportStatus = (
  id: number,
  isActive: boolean
) => {
  return axios.patch(
    `/scheduled-reports/${id}/status`,
    {
      is_active: isActive,
    },
    {
      headers: getAuthHeaders(),
    }
  );
};

export const deleteScheduledReport = (
  id: number
) => {
  return axios.delete(
    `/scheduled-reports/${id}`,
    {
      headers: getAuthHeaders(),
    }
  );
};