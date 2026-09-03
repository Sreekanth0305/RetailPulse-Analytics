import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import AuditLogDetailsModal from "../components/AuditLogDetailsModal";

import { 
    getAuditLogs, 
    getAuditLogById,
    exportAuditLogsCSV,
    exportAuditLogsPDF,
    clearAuditLogs
} from "../services/auditService";
import type { AuditLog } from "../services/auditService";

import "../styles/auditlogs.css";

function AuditLogs() {

    const [logs, setLogs] = useState<AuditLog[]>([]);

    const [search, setSearch] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [actionFilter, setActionFilter] = useState("");
    const [resourceFilter, setResourceFilter] = useState("");
    const [statusFilter, setStatusFilter] = useState("");

    const [dateFrom, setDateFrom] = useState("");
    const [dateTo, setDateTo] = useState("");

    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [limit] = useState(25);

    const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);
    const [showDetails, setShowDetails] = useState(false);

    const loadLogs = async (page: number = currentPage) => {

        setLoading(true);
        setError("");

        try {

            const response = await getAuditLogs({
                search: search || undefined,
                action: actionFilter || undefined,
                resource_type: resourceFilter || undefined,
                status: statusFilter || undefined,
                date_from: dateFrom || undefined,
                date_to: dateTo || undefined,
                sort_order: sortOrder,
                page: page,
                limit: limit
            });

            setLogs(response.data.items);
            setCurrentPage(response.data.page);
            setTotalPages(response.data.total_pages);

        } catch (error) {

            console.log(error);

            setError("Failed to load audit logs. Please try again.");

        } finally {

            setLoading(false);

        }

    };

    const loadLogDetails = async (auditLogId: number) => {

        try {
    
            const response = await getAuditLogById(auditLogId);
    
            setSelectedLog(response.data);
            setShowDetails(true);
    
        } catch (error) {
    
            console.log(error);
    
        }
    
    };

    const exportCSV = async () => {

        try {
    
            const response = await exportAuditLogsCSV({
    
                search: search || undefined,
                action: actionFilter || undefined,
                resource_type: resourceFilter || undefined,
                status: statusFilter || undefined,
                date_from: dateFrom || undefined,
                date_to: dateTo || undefined,
                sort_order: sortOrder
    
            });
    
            const blob = new Blob(
                [response.data],
                { type: "text/csv" }
            );
    
            const url = window.URL.createObjectURL(blob);
    
            const link = document.createElement("a");
    
            link.href = url;
            link.download = "audit_logs.csv";
    
            document.body.appendChild(link);
    
            link.click();
    
            link.remove();
    
            window.URL.revokeObjectURL(url);
    
        } catch (error) {
    
            console.log(error);
    
        }
    
    };

    const exportPDF = async () => {

        try {
    
            const response = await exportAuditLogsPDF({
    
                search: search || undefined,
                action: actionFilter || undefined,
                resource_type: resourceFilter || undefined,
                status: statusFilter || undefined,
                date_from: dateFrom || undefined,
                date_to: dateTo || undefined,
                sort_order: sortOrder
    
            });
    
            const blob = new Blob(
                [response.data],
                { type: "application/pdf" }
            );
    
            const url = window.URL.createObjectURL(blob);
    
            const link = document.createElement("a");
    
            link.href = url;
            link.download = "audit_logs.pdf";
    
            document.body.appendChild(link);
    
            link.click();
    
            link.remove();
    
            window.URL.revokeObjectURL(url);
    
        } catch (error) {
    
            console.log(error);
    
        }
    
    };

    const handleClearLogs = async () => {

        const confirmed = window.confirm(
            "Are you sure you want to clear all audit logs for your company? This action cannot be undone."
        );
    
        if (!confirmed) {
            return;
        }
    
        try {
    
            await clearAuditLogs();
    
            await loadLogs(1);
    
            alert("Audit logs cleared successfully.");
    
        } catch (error) {
    
            console.log(error);
    
            alert(
                "Failed to clear audit logs. Please try again."
            );
    
        }
    
    };

    useEffect(() => {

        loadLogs();

    }, []);

    useEffect(() => {

        const interval = setInterval(() => {
    
            loadLogs(currentPage);
    
        }, 30000);
    
        return () => {
    
            clearInterval(interval);
    
        };
    
    }, [
        currentPage,
        search,
        actionFilter,
        resourceFilter,
        statusFilter,
        dateFrom,
        dateTo,
        sortOrder
    ]);

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="audit-page">

                <div className="audit-title-row">

                    <h2>Audit Logs</h2>
                
                    {loading && logs.length > 0 && (
                        <span className="audit-refreshing">
                            Refreshing...
                        </span>
                    )}
                
                </div>

                <div className="audit-filters">

                    <div className="audit-search">
                
                        <input
                            type="text"
                            placeholder="Search audit logs..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                
                    </div>
                
                    <select
                        value={actionFilter}
                        onChange={(e) => setActionFilter(e.target.value)}
                    >
                        <option value="">All Actions</option>
                    
                        <option value="Company Registered">Company Registered</option>
                        <option value="Customer Active">Customer Active</option>
                        <option value="Customer Created">Customer Created</option>
                        <option value="Customer Deleted">Customer Deleted</option>
                        <option value="Customer Inactive">Customer Inactive</option>
                        <option value="Customer Updated">Customer Updated</option>
                        <option value="Dashboard Viewed">Dashboard Viewed</option>
                        <option value="Forecast Generated">Forecast Generated</option>
                        <option value="Inventory Recommendation Generated">
                            Inventory Recommendation Generated
                        </option>
                        <option value="Inventory Updated">Inventory Updated</option>
                        <option value="LOGIN">LOGIN</option>
                        <option value="LOGOUT">LOGOUT</option>
                        <option value="Password Changed">Password Changed</option>
                        <option value="Product Activated">Product Activated</option>
                        <option value="Product Created">Product Created</option>
                        <option value="Product Deactivated">Product Deactivated</option>
                        <option value="Product Updated">Product Updated</option>
                        <option value="Report Exported">Report Exported</option>
                        <option value="Sale Created">Sale Created</option>
                        <option value="Sale Deleted">Sale Deleted</option>
                        <option value="Sale Updated">Sale Updated</option>
                        <option value="Stock Added">Stock Added</option>
                        <option value="Stock Adjusted">Stock Adjusted</option>
                        <option value="Stock Removed">Stock Removed</option>
                        <option value="User Login">User Login</option>
                        <option value="User Logout">User Logout</option>
                    </select>
                
                    <select
                        value={resourceFilter}
                        onChange={(e) => setResourceFilter(e.target.value)}
                    >
                        <option value="">All Resources</option>
                        <option value="USER">USER</option>
                    </select>
                
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                    >
                        <option value="">All Statuses</option>
                        <option value="Success">Success</option>
                        <option value="Failed">Failed</option>
                    </select>

                    <select
                        value={sortOrder}
                        onChange={(e) =>
                            setSortOrder(e.target.value as "asc" | "desc")
                        }
                    >
                        <option value="desc">Newest First</option>
                        <option value="asc">Oldest First</option>
                    </select>

                    <div className="audit-date-filter">

                        <label>
                            From
                        </label>
                    
                        <input
                            type="date"
                            value={dateFrom}
                            onChange={(e) => setDateFrom(e.target.value)}
                        />
                    
                    </div>
                    
                    <div className="audit-date-filter">
                    
                        <label>
                            To
                        </label>
                    
                        <input
                            type="date"
                            value={dateTo}
                            onChange={(e) => setDateTo(e.target.value)}
                        />
                    
                    </div>
                
                    <button
                        onClick={() => {
                            setCurrentPage(1);
                            loadLogs(1);
                        }}
                    >
                        Search
                    </button>

                    <button
                        type="button"
                        onClick={exportCSV}
                    >
                        Export CSV
                    </button>
                    
                    <button
                        type="button"
                        onClick={exportPDF}
                    >
                        Export PDF
                    </button>
                
                </div>

                <button
                    type="button"
                    className="audit-clear-button"
                    onClick={handleClearLogs}
                >
                    Clear Logs
                </button>

                <div className="audit-table-container">

                    {error && (
                        <div className="audit-error">
                            <span>{error}</span>
                    
                            <button onClick={() => loadLogs(currentPage)}>
                                Retry
                            </button>
                        </div>
                    )}

                    <table className="audit-table">
    
                        <thead>
    
                            <tr>
    
                                <th>Timestamp</th>
                                <th>User</th>
                                <th>Action</th>
                                <th>Resource</th>
                                <th>Resource ID</th>
                                <th>Description</th>
                                <th>IP Address</th>
                                <th>Browser</th>
                                <th>Status</th>
    
                            </tr>
    
                        </thead>
    
                        <tbody>

                            {loading && logs.length === 0 ? (
                        
                                Array.from({ length: 5 }).map((_, index) => (
                        
                                    <tr key={index} className="audit-loading-row">
                        
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                                        <td>Loading...</td>
                        
                                    </tr>
                        
                                ))
                        
                            ) : logs.length === 0 ? (
                        
                                <tr>
                        
                                    <td
                                        colSpan={9}
                                        className="audit-empty"
                                    >
                                        No activity found for the selected filters.
                                    </td>
                        
                                </tr>
                        
                            ) : (
                        
                                logs.map((log: AuditLog) => (
                        
                                    <tr
                                        key={log.id}
                                        onClick={() => loadLogDetails(log.id)}
                                    >
                        
                                        <td>
                                            {new Date(log.created_at).toLocaleString()}
                                        </td>
                        
                                        <td>
                                            {log.user_name}
                                        </td>
                        
                                        <td>
                                            {log.action}
                                        </td>
                        
                                        <td>
                                            {log.resource_type || "-"}
                                        </td>
                        
                                        <td>
                                            {log.resource_id ?? "-"}
                                        </td>
                        
                                        <td>
                                            {log.description || "-"}
                                        </td>
                        
                                        <td>
                                            {log.ip_address || "-"}
                                        </td>
                        
                                        <td>
                                            {log.user_agent || "-"}
                                        </td>
                        
                                        <td>
                                            {log.status || "-"}
                                        </td>
                        
                                    </tr>
                        
                                ))
                        
                            )}
                        
                        </tbody>
    
                    </table>

                </div>

                <div className="audit-pagination">

                    <button
                        onClick={() => loadLogs(currentPage - 1)}
                        disabled={currentPage <= 1}
                    >
                        Previous
                    </button>
                
                    <span>
                        Page {currentPage} of {totalPages}
                    </span>
                
                    <button
                        onClick={() => loadLogs(currentPage + 1)}
                        disabled={currentPage >= totalPages || totalPages === 0}
                    >
                        Next
                    </button>
                
                </div>

                <AuditLogDetailsModal
                    log={selectedLog}
                    open={showDetails}
                    onClose={() => setShowDetails(false)}
                />

            </div>

        </>

    );

}

export default AuditLogs;