import type { AuditLog } from "../services/auditService";

interface AuditLogDetailsModalProps {
    log: AuditLog | null;
    open: boolean;
    onClose: () => void;
}

function AuditLogDetailsModal({
    log,
    open,
    onClose
}: AuditLogDetailsModalProps) {

    if (!open || !log) {
        return null;
    }

    return (
        <div className="audit-modal-overlay">

            <div className="audit-modal">

                <div className="audit-modal-header">

                    <h3>Audit Log Details</h3>

                    <button
                        className="audit-modal-close"
                        onClick={onClose}
                    >
                        ×
                    </button>

                </div>

                <div className="audit-modal-body">

                    <div className="audit-detail-row">
                        <strong>ID:</strong>
                        <span>{log.id}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>User:</strong>
                        <span>{log.user_name}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>Action:</strong>
                        <span>{log.action}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>Resource:</strong>
                        <span>
                            {log.resource_type
                                ? `${log.resource_type}${
                                    log.resource_id
                                        ? ` #${log.resource_id}`
                                        : ""
                                }`
                                : "-"}
                        </span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>Status:</strong>
                        <span>{log.status}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>IP Address:</strong>
                        <span>{log.ip_address || "-"}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>Browser:</strong>
                        <span>{log.user_agent || "-"}</span>
                    </div>

                    <div className="audit-detail-row">
                        <strong>Timestamp:</strong>
                        <span>
                            {new Date(log.created_at).toLocaleString()}
                        </span>
                    </div>

                    <div className="audit-detail-section">

                        <strong>Description:</strong>

                        <p>
                            {log.description || "-"}
                        </p>

                    </div>

                    <div className="audit-detail-section">

                        <strong>Before Values:</strong>

                        <pre>
                            {log.before_values
                                ? log.before_values
                                : "-"}
                        </pre>

                    </div>

                    <div className="audit-detail-section">

                        <strong>After Values:</strong>

                        <pre>
                            {log.after_values
                                ? log.after_values
                                : "-"}
                        </pre>

                    </div>

                </div>

            </div>

        </div>
    );
}

export default AuditLogDetailsModal;