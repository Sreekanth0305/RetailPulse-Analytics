import axios from "../api/axios";

export interface AuditLog {
    id: number;
    company_id: number;
    user_id: number;
    user_name: string;
    action: string;
    resource_type: string | null;
    resource_id: number | null;
    description: string | null;
    ip_address: string | null;
    user_agent: string | null;
    status: string;
    before_values: string | null;
    after_values: string | null;
    created_at: string;
}

export interface AuditLogResponse {
    items: AuditLog[];
    total: number;
    page: number;
    limit: number;
    total_pages: number;
}

export interface AuditLogFilters {
    user_id?: number;
    action?: string;
    resource_type?: string;
    status?: string;
    search?: string;
    date_from?: string;
    date_to?: string;
    sort_order?: "asc" | "desc";
    page?: number;
    limit?: number;
}


// =========================================================
// GET AUDIT LOGS
// =========================================================

export const getAuditLogs = (
    filters: AuditLogFilters = {}
) => {

    const token = localStorage.getItem("access_token");

    return axios.get<AuditLogResponse>(
        "/audit-logs/",
        {
            params: filters,

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};


// =========================================================
// GET SINGLE AUDIT LOG
// =========================================================

export const getAuditLogById = (
    auditLogId: number
) => {

    const token = localStorage.getItem("access_token");

    return axios.get<AuditLog>(
        `/audit-logs/${auditLogId}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};


// =========================================================
// CREATE AUDIT LOG
// =========================================================

export const createAuditLog = (
    data: any
) => {

    const token = localStorage.getItem("access_token");

    return axios.post(
        "/audit-logs/",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};

export const exportAuditLogsCSV = (
    filters: AuditLogFilters = {}
) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/audit-logs/export/csv", {

        params: filters,

        headers: {
            Authorization: `Bearer ${token}`
        },

        responseType: "blob"

    });

};


export const exportAuditLogsPDF = (
    filters: AuditLogFilters = {}
) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/audit-logs/export/pdf", {

        params: filters,

        headers: {
            Authorization: `Bearer ${token}`
        },

        responseType: "blob"

    });

};

export const clearAuditLogs = () => {

    const token = localStorage.getItem("access_token");

    return axios.delete(
        "/audit-logs/clear",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};