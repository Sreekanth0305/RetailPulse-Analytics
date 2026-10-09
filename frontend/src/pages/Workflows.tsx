import {
  useEffect,
  useState
} from "react";

import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Select,
  Switch,
  TextField,
  Typography
} from "@mui/material";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getWorkflowRequests,
  getWorkflowRequest,
  getWorkflowHistory,
  approveWorkflowRequest,
  rejectWorkflowRequest,
  cancelWorkflowRequest,
  createWorkflowRequest,
  submitWorkflowRequest,
  createWorkflowConfig,
  getWorkflowConfigs
} from "../services/workflowService";

import "../styles/workflows.css";


// =========================================================
// TYPES
// =========================================================

interface Workflow {
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

interface WorkflowHistory {
  id: number;
  workflow_id: number;
  action: string;
  comment?: string;
  performed_by?: number;
  created_at: string;
}


// =========================================================
// COMPONENT
// =========================================================

export default function Workflows() {

  const [requests, setRequests] =
    useState<Workflow[]>([]);

  const [selectedRequest, setSelectedRequest] =
    useState<Workflow | null>(null);

  const [history, setHistory] =
    useState<WorkflowHistory[]>([]);

  const [search, setSearch] =
    useState("");

  const [requestType, setRequestType] =
    useState("");

  const [status, setStatus] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [comment, setComment] =
    useState("");

  const [detailsOpen, setDetailsOpen] =
    useState(false);

  const [createOpen, setCreateOpen] =
    useState(false);

  const [configOpen, setConfigOpen] =
    useState(false);


  // =========================================================
  // CREATE FORM
  // =========================================================

  const [newRequest, setNewRequest] =
  useState<{
    request_type: string;
    related_record: string;
    requested_changes: Record<string, any>;
    reason: string;
    priority: string;
  }>({
    request_type: "Stock Adjustment",
    related_record: "",
    requested_changes: {},
    reason: "",
    priority: "Normal"
  });

  const [requestedChangesText, setRequestedChangesText] =
  useState("");

  // =========================================================
  // CONFIG FORM
  // =========================================================

  const [config, setConfig] =
    useState({
      request_type: "Stock Adjustment",
      approver_role: "Admin",
      approval_required: true,
      allow_self_approval: false,
      is_active: true
    });


  // =========================================================
// LOAD REQUESTS
// =========================================================

const loadRequests = async () => {

  try {

    setLoading(true);
    setError("");

    const response =
      await getWorkflowRequests(
        requestType || undefined,
        status || undefined,
        search || undefined,
        1,
        50
      );

    console.log(
      "Workflow API response:",
      response
    );

    if (
      response &&
      Array.isArray(response.requests)
    ) {

      setRequests(
        response.requests
      );

    } else {

      setRequests([]);

    }

  } catch (err) {

    console.error(
      "Failed to load workflows:",
      err
    );

    setError(
      "Failed to load workflow requests."
    );

  } finally {

    setLoading(false);

  }
};

  // =========================================================
  // LOAD WORKFLOW CONFIGURATIONS
  // =========================================================

  const loadWorkflowConfigs = async () => {

    try {

      const configs = await getWorkflowConfigs();

      console.log(
        "Workflow configurations:",
        configs
      );

    } catch (error) {

      console.error(
        "Failed to load workflow configurations",
        error
      );

    }
  };


  // =========================================================
  // INITIAL LOAD
  // =========================================================

  useEffect(() => {

    loadRequests();

    loadWorkflowConfigs();

  }, [
    requestType,
    status
  ]);


  // =========================================================
  // VIEW DETAILS
  // =========================================================

  const handleViewDetails =
    async (id: number) => {

      try {

        setError("");

        const response =
          await getWorkflowRequest(id);

        setSelectedRequest(
          response
        );

        const historyResponse =
          await getWorkflowHistory(id);

        setHistory(
          Array.isArray(
            historyResponse
          )
            ? historyResponse
            : []
        );

        setDetailsOpen(true);

      } catch (err) {

        console.error(err);

        setError(
          "Unable to load workflow details."
        );

      }
    };


  // =========================================================
  // APPROVE
  // =========================================================

  const handleApprove =
    async () => {

      if (!selectedRequest) {
        return;
      }

      try {

        await approveWorkflowRequest(
          selectedRequest.id,
          comment
        );

        setComment("");

        setDetailsOpen(false);

        await loadRequests();

      } catch (err) {

        console.error(err);

        setError(
          "Unable to approve request."
        );

      }
    };


  // =========================================================
  // REJECT
  // =========================================================

  const handleReject =
    async () => {

      if (!selectedRequest) {
        return;
      }

      if (!comment.trim()) {

        setError(
          "Rejection comment is required."
        );

        return;
      }

      try {

        await rejectWorkflowRequest(
          selectedRequest.id,
          comment
        );

        setComment("");

        setDetailsOpen(false);

        await loadRequests();

      } catch (err) {

        console.error(err);

        setError(
          "Unable to reject request."
        );

      }
    };


  // =========================================================
  // CANCEL
  // =========================================================

  const handleCancel =
    async () => {

      if (!selectedRequest) {
        return;
      }

      try {

        await cancelWorkflowRequest(
          selectedRequest.id,
          comment
        );

        setComment("");

        setDetailsOpen(false);

        await loadRequests();

      } catch (err) {

        console.error(err);

        setError(
          "Unable to cancel request."
        );

      }
    };


  // =========================================================
  // CREATE REQUEST
  // =========================================================

  const handleCreateRequest =
  async () => {

    try {

      setError("");


      const workflow =
        await createWorkflowRequest({
          ...newRequest,
        });

      /*
        Create API creates the request.
        Submit it separately according
        to Task 18 lifecycle.
      */

      if (workflow?.id) {

        await submitWorkflowRequest(
          workflow.id
        );

      }

      setCreateOpen(false);

      setNewRequest({
        request_type:
          "Stock Adjustment",
        related_record: "",
        requested_changes: {},
        reason: "",
        priority: "Normal"
      });

      await loadRequests();

    } catch (err) {

      console.error(
        "Unable to create workflow request:",
        err
      );

      setError(
        "Unable to create workflow request."
      );

    }

  };


  // =========================================================
  // CREATE CONFIG
  // =========================================================

  const handleCreateConfig =
    async () => {

      try {

        await createWorkflowConfig(
          config
        );

        setConfigOpen(false);

        setError("");

      } catch (err) {

        console.error(err);

        setError(
          "Unable to create workflow configuration."
        );

      }

    };


  // =========================================================
  // SEARCH
  // =========================================================

  const handleSearch =
    async () => {

      await loadRequests();

    };


  // =========================================================
  // RENDER
  // =========================================================

  return (

    <>

      <Sidebar />

      <Navbar />

      <div className="workflows-page">

        <div className="workflows-container">

          {/* ================================================= */}
          {/* HEADER */}
          {/* ================================================= */}

          <div className="workflows-header">

            <div>

              <h1>
                Workflows & Approvals
              </h1>

              <p>
                Manage requests requiring authorization
              </p>

            </div>

            <div className="workflow-header-actions">

              <Button
                variant="contained"
                onClick={() =>
                  setCreateOpen(true)
                }
              >
                Create Request
              </Button>

              <Button
                variant="outlined"
                onClick={() =>
                  setConfigOpen(true)
                }
              >
                Workflow Configuration
              </Button>

            </div>

          </div>


          {/* ================================================= */}
          {/* ERROR */}
          {/* ================================================= */}

          {error && (

            <Alert
              severity="error"
              className="workflow-alert"
            >
              {error}
            </Alert>

          )}


          {/* ================================================= */}
          {/* FILTERS */}
          {/* ================================================= */}

          <Card className="workflow-card">

            <CardContent>

              <div className="workflow-filters">

                <TextField
                  label="Search"
                  value={search}
                  onChange={(e) =>
                    setSearch(
                      e.target.value
                    )
                  }
                  onKeyDown={(e) => {

                    if (
                      e.key === "Enter"
                    ) {
                      handleSearch();
                    }

                  }}
                />


                <FormControl>

                  <InputLabel>
                    Request Type
                  </InputLabel>

                  <Select
                    value={requestType}
                    label="Request Type"
                    onChange={(e) =>
                      setRequestType(
                        e.target.value
                      )
                    }
                  >

                    <MenuItem value="">
                      All
                    </MenuItem>

                    <MenuItem value="Stock Adjustment">
                      Stock Adjustment
                    </MenuItem>

                    <MenuItem value="Product Deactivation">
                      Product Deactivation
                    </MenuItem>

                    <MenuItem value="Product Price Change">
                      Product Price Change
                    </MenuItem>

                    <MenuItem value="Customer Information Change">
                      Customer Information Change
                    </MenuItem>

                    <MenuItem value="Inventory Import Approval">
                      Inventory Import Approval
                    </MenuItem>

                  </Select>

                </FormControl>


                <FormControl>

                  <InputLabel>
                    Status
                  </InputLabel>

                  <Select
                    value={status}
                    label="Status"
                    onChange={(e) =>
                      setStatus(
                        e.target.value
                      )
                    }
                  >

                    <MenuItem value="">
                      All
                    </MenuItem>

                    <MenuItem value="Draft">
                      Draft
                    </MenuItem>

                    <MenuItem value="Submitted">
                      Submitted
                    </MenuItem>

                    <MenuItem value="Pending Approval">
                      Pending Approval
                    </MenuItem>

                    <MenuItem value="Approved">
                      Approved
                    </MenuItem>

                    <MenuItem value="Rejected">
                      Rejected
                    </MenuItem>

                    <MenuItem value="Cancelled">
                      Cancelled
                    </MenuItem>

                  </Select>

                </FormControl>


                <Button
                  variant="outlined"
                  onClick={handleSearch}
                >
                  Search
                </Button>

              </div>

            </CardContent>

          </Card>


          {/* ================================================= */}
          {/* REQUEST TABLE */}
          {/* ================================================= */}

          <Card className="workflow-card">

            <CardContent>

              <Typography
                variant="h6"
                className="workflow-section-title"
              >
                Approval Requests
              </Typography>


              {loading ? (

                <Box className="workflow-loading">

                  Loading requests...

                </Box>

              ) : requests.length === 0 ? (

                <Box className="workflow-empty">

                  No workflow requests found.

                </Box>

              ) : (

                <div className="workflow-table-wrapper">

                  <table className="workflow-table">

                    <thead>

                      <tr>

                        <th>
                          Request ID
                        </th>

                        <th>
                          Type
                        </th>

                        <th>
                          Requested By
                        </th>

                        <th>
                          Related Record
                        </th>

                        <th>
                          Priority
                        </th>

                        <th>
                          Status
                        </th>

                        <th>
                          Created
                        </th>

                        <th>
                          Action
                        </th>

                      </tr>

                    </thead>


                    <tbody>

                      {requests.map(
                        (request) => (

                          <tr
                            key={
                              request.id
                            }
                          >

                            <td>
                              #{request.id}
                            </td>

                            <td>
                              {request.request_type}
                            </td>

                            <td>
                              {request.requested_by}
                            </td>

                            <td>
                              {
                                request.related_record ||
                                "-"
                              }
                            </td>

                            <td>
                              {
                                request.priority ||
                                "Normal"
                              }
                            </td>

                            <td>

                              <span
                                className={`workflow-status ${request.status
                                  .toLowerCase()
                                  .replace(
                                    /\s+/g,
                                    "-"
                                  )}`}
                              >
                                {request.status}
                              </span>

                            </td>

                            <td>
                              {new Date(
                                request.created_at
                              ).toLocaleString()}
                            </td>

                            <td>

                              <Button
                                size="small"
                                variant="outlined"
                                onClick={() =>
                                  handleViewDetails(
                                    request.id
                                  )
                                }
                              >
                                View
                              </Button>

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              )}

            </CardContent>

          </Card>


          {/* ================================================= */}
          {/* DETAILS DIALOG */}
          {/* ================================================= */}

          <Dialog
            open={detailsOpen}
            onClose={() =>
              setDetailsOpen(false)
            }
            fullWidth
            maxWidth="md"
          >

            <DialogTitle>
              Workflow Request Details
            </DialogTitle>


            <DialogContent>

              {selectedRequest && (

                <div className="workflow-details">

                  <div className="workflow-detail-grid">

                    <div>
                      <strong>
                        Request ID
                      </strong>

                      <span>
                        #{selectedRequest.id}
                      </span>
                    </div>


                    <div>
                      <strong>
                        Request Type
                      </strong>

                      <span>
                        {selectedRequest.request_type}
                      </span>
                    </div>


                    <div>
                      <strong>
                        Requested By
                      </strong>

                      <span>
                        {selectedRequest.requested_by}
                      </span>
                    </div>


                    <div>
                      <strong>
                        Status
                      </strong>

                      <span>
                        {selectedRequest.status}
                      </span>
                    </div>


                    <div>
                      <strong>
                        Related Record
                      </strong>

                      <span>
                        {
                          selectedRequest.related_record ||
                          "-"
                        }
                      </span>
                    </div>


                    <div>
                      <strong>
                        Priority
                      </strong>

                      <span>
                        {
                          selectedRequest.priority ||
                          "Normal"
                        }
                      </span>
                    </div>

                  </div>


                  <div className="workflow-detail-section">

                    <strong>
                      Requested Changes
                    </strong>

                    <pre>
                      {selectedRequest.requested_changes
                        ? JSON.stringify(
                            selectedRequest.requested_changes,
                            null,
                            2
                          )
                        : "No changes specified."}
                    </pre>

                  </div>


                  <div className="workflow-detail-section">

                    <strong>
                      Reason
                    </strong>

                    <p>
                      {
                        selectedRequest.reason ||
                        "No reason provided."
                      }
                    </p>

                  </div>


                  {/* HISTORY */}

                  <div className="workflow-history">

                    <h3>
                      Approval History
                    </h3>


                    {history.length === 0 ? (

                      <p>
                        No history available.
                      </p>

                    ) : (

                      history.map(
                        (item) => (

                          <div
                            className="workflow-history-item"
                            key={item.id}
                          >

                            <div>

                              <strong>
                                {item.action}
                              </strong>

                              <span>
                                {new Date(
                                  item.created_at
                                ).toLocaleString()}
                              </span>

                            </div>

                            <p>
                              {
                                item.comment ||
                                "No comment"
                              }
                            </p>

                          </div>

                        )
                      )

                    )}

                  </div>


                  {/* COMMENT */}

                  {(
                    selectedRequest.status ===
                    "Pending Approval"
                  ) && (

                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      label="Comment"
                      value={comment}
                      onChange={(e) =>
                        setComment(
                          e.target.value
                        )
                      }
                      className="workflow-comment"
                    />

                  )}

                </div>

              )}

            </DialogContent>


            <DialogActions>

              {selectedRequest &&
                selectedRequest.status.trim().toLowerCase() ===
                  "pending approval" && (
                <>

                  <Button
                    color="error"
                    onClick={handleReject}
                  >
                    Reject
                  </Button>

                  <Button
                    color="success"
                    variant="contained"
                    onClick={handleApprove}
                  >
                    Approve
                  </Button>

                </>

              )}


              {selectedRequest &&
                (
                  selectedRequest.status.trim().toLowerCase() === "draft" ||
                  selectedRequest.status.trim().toLowerCase() === "submitted" ||
                  selectedRequest.status.trim().toLowerCase() === "pending approval"
                ) && (

                <Button
                  color="warning"
                  onClick={handleCancel}
                >
                  Cancel
                </Button>

              )}


              <Button
                onClick={() =>
                  setDetailsOpen(false)
                }
              >
                Close
              </Button>

            </DialogActions>

          </Dialog>


          {/* ================================================= */}
          {/* CREATE REQUEST DIALOG */}
          {/* ================================================= */}

          <Dialog
            open={createOpen}
            onClose={() =>
              setCreateOpen(false)
            }
            fullWidth
            maxWidth="sm"
          >

            <DialogTitle>
              Create Approval Request
            </DialogTitle>

            <DialogContent>

              <FormControl
                fullWidth
                margin="normal"
              >

                <InputLabel>
                  Request Type
                </InputLabel>

                <Select
                  value={
                    newRequest.request_type
                  }
                  label="Request Type"
                  onChange={(e) =>
                    setNewRequest({
                      ...newRequest,
                      request_type:
                        e.target.value
                    })
                  }
                >

                  <MenuItem value="Stock Adjustment">
                    Stock Adjustment
                  </MenuItem>

                  <MenuItem value="Product Deactivation">
                    Product Deactivation
                  </MenuItem>

                  <MenuItem value="Product Price Change">
                    Product Price Change
                  </MenuItem>

                  <MenuItem value="Customer Information Change">
                    Customer Information Change
                  </MenuItem>

                  <MenuItem value="Inventory Import Approval">
                    Inventory Import Approval
                  </MenuItem>

                </Select>

              </FormControl>


              <TextField
                fullWidth
                label="Related Record"
                margin="normal"
                value={
                  newRequest.related_record
                }
                onChange={(e) =>
                  setNewRequest({
                    ...newRequest,
                    related_record:
                      e.target.value
                  })
                }
              />


              <TextField
  fullWidth
  multiline
  rows={5}
  label="Requested Changes (JSON)"
  margin="normal"
  value={requestedChangesText}
  onChange={(e) =>
    setRequestedChangesText(e.target.value)
  }
  placeholder={`{
  "product_id": 1,
  "new_stock": 150
}`}
/>

              <TextField
                fullWidth
                multiline
                rows={3}
                label="Reason"
                margin="normal"
                value={
                  newRequest.reason
                }
                onChange={(e) =>
                  setNewRequest({
                    ...newRequest,
                    reason:
                      e.target.value
                  })
                }
              />


              <FormControl
                fullWidth
                margin="normal"
              >

                <InputLabel>
                  Priority
                </InputLabel>

                <Select
                  value={
                    newRequest.priority
                  }
                  label="Priority"
                  onChange={(e) =>
                    setNewRequest({
                      ...newRequest,
                      priority:
                        e.target.value
                    })
                  }
                >

                  <MenuItem value="Low">
                    Low
                  </MenuItem>

                  <MenuItem value="Normal">
                    Normal
                  </MenuItem>

                  <MenuItem value="High">
                    High
                  </MenuItem>

                  <MenuItem value="Critical">
                    Critical
                  </MenuItem>

                </Select>

              </FormControl>

            </DialogContent>


            <DialogActions>

              <Button
                onClick={() =>
                  setCreateOpen(false)
                }
              >
                Cancel
              </Button>

              <Button
                variant="contained"
                onClick={
                  handleCreateRequest
                }
              >
                Submit Request
              </Button>

            </DialogActions>

          </Dialog>


          {/* ================================================= */}
          {/* CONFIGURATION DIALOG */}
          {/* ================================================= */}

          <Dialog
            open={configOpen}
            onClose={() =>
              setConfigOpen(false)
            }
            fullWidth
            maxWidth="sm"
          >

            <DialogTitle>
              Workflow Configuration
            </DialogTitle>


            <DialogContent>

              <FormControl
                fullWidth
                margin="normal"
              >

                <InputLabel>
                  Request Type
                </InputLabel>

                <Select
                  value={
                    config.request_type
                  }
                  label="Request Type"
                  onChange={(e) =>
                    setConfig({
                      ...config,
                      request_type:
                        e.target.value
                    })
                  }
                >

                  <MenuItem value="Stock Adjustment">
                    Stock Adjustment
                  </MenuItem>

                  <MenuItem value="Product Deactivation">
                    Product Deactivation
                  </MenuItem>

                  <MenuItem value="Product Price Change">
                    Product Price Change
                  </MenuItem>

                  <MenuItem value="Customer Information Change">
                    Customer Information Change
                  </MenuItem>

                  <MenuItem value="Inventory Import Approval">
                    Inventory Import Approval
                  </MenuItem>

                </Select>

              </FormControl>


              <TextField
                fullWidth
                label="Approver Role"
                margin="normal"
                value={
                  config.approver_role
                }
                onChange={(e) =>
                  setConfig({
                    ...config,
                    approver_role:
                      e.target.value
                  })
                }
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={config.approval_required}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        approval_required:
                          e.target.checked
                      })
                    }
                  />
                }
                label="Approval Required"
              />
            
              <FormControlLabel
                control={
                  <Switch
                    checked={config.allow_self_approval}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        allow_self_approval:
                          e.target.checked
                      })
                    }
                  />
                }
                label="Allow Self Approval"
              />
            
              <FormControlLabel
                control={
                  <Switch
                    checked={config.is_active}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        is_active:
                          e.target.checked
                      })
                    }
                  />
                }
                label="Active"
              />

            </DialogContent>


            <DialogActions>

              <Button
                onClick={() =>
                  setConfigOpen(false)
                }
              >
                Cancel
              </Button>

              <Button
                variant="contained"
                onClick={
                  handleCreateConfig
                }
              >
                Save Configuration
              </Button>

            </DialogActions>

          </Dialog>

        </div>

      </div>

    </>

  );
}