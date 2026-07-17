import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

import { getAuditLogs } from "../services/auditService";

import "../styles/auditlogs.css";

function AuditLogs() {

    const [logs, setLogs] = useState([]);

    const loadLogs = async () => {

        try {

            const response = await getAuditLogs();

            setLogs(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

        loadLogs();

    }, []);

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="audit-page">

                <h2>Audit Logs</h2>

                <table className="audit-table">

                    <thead>

                        <tr>

                            <th>Timestamp</th>
                            <th>User</th>
                            <th>Action</th>
                            <th>Entity</th>
                            <th>IP Address</th>
                            <th>Browser</th>

                        </tr>

                    </thead>

                    <tbody>

                        {logs.map((log: any) => (

                            <tr key={log.id}>

                                <td>{new Date(log.created_at).toLocaleString()}</td>

                                <td>{log.user_name}</td>

                                <td>{log.action}</td>

                                <td>{log.entity_name || "-"}</td>

                                <td>{log.ip_address || "-"}</td>

                                <td>{log.browser || "-"}</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </>

    );

}

export default AuditLogs;