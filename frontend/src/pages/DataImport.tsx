import { useState } from "react";
import type { ChangeEvent } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  Alert,
  Button,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

import type { SelectChangeEvent } from "@mui/material";

import {
  getImportErrors,
  getImportHistory,
  processImport,
  uploadImport,
  validateImport,
} from "../services/importService";

import "../styles/dataImport.css";


type ImportType =
  | "products"
  | "customers"
  | "sales";


interface ValidationResult {
  import_type: string;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  duplicate_records: number;
  errors: {
    row_number: number;
    error_type: string;
    error_message: string;
  }[];
  can_import: boolean;
}


interface UploadResult {
  import_id: number;
  import_type: string;
  filename: string;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  duplicate_records: number;
  columns: string[];
  preview: Record<string, string>[];
}


interface ImportHistory {
  id: number;
  import_type: string;
  filename: string;
  uploaded_by: number;
  total_records: number;
  successful_records: number;
  failed_records: number;
  duplicate_records: number;
  status: string;
  created_at: string;
  completed_at?: string;
}


export default function DataImport() {

  const [importType, setImportType] =
    useState<ImportType>("products");

  const [file, setFile] =
    useState<File | null>(null);

  const [uploadResult, setUploadResult] =
    useState<UploadResult | null>(null);

  const [validationResult, setValidationResult] =
    useState<ValidationResult | null>(null);

  const [history, setHistory] =
    useState<ImportHistory[]>([]);

  const [errorRecords, setErrorRecords] =
    useState<any[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");


  // =========================================================
  // Import type
  // =========================================================

  const handleImportTypeChange = (
    event: SelectChangeEvent
  ) => {

    setImportType(
      event.target.value as ImportType
    );

    setFile(null);
    setUploadResult(null);
    setValidationResult(null);
    setErrorRecords([]);
    setMessage("");
    setError("");
  };


  // =========================================================
  // File selection
  // =========================================================

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {

    const selectedFile =
      event.target.files?.[0];

    setError("");
    setMessage("");

    if (!selectedFile) {
      return;
    }


    // CSV validation

    if (
      !selectedFile.name
        .toLowerCase()
        .endsWith(".csv")
    ) {

      setError(
        "Only CSV files are allowed."
      );

      event.target.value = "";

      return;
    }


    // 10 MB validation

    const maxSize =
      10 * 1024 * 1024;

    if (selectedFile.size > maxSize) {

      setError(
        "File size cannot exceed 10 MB."
      );

      event.target.value = "";

      return;
    }


    setFile(selectedFile);

    setUploadResult(null);
    setValidationResult(null);
    setErrorRecords([]);
  };


  // =========================================================
  // Upload
  // =========================================================

  const handleUpload = async () => {

    if (!file) {

      setError(
        "Please select a CSV file first."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setMessage("");

      const result =
        await uploadImport(
          importType,
          file
        );

      setUploadResult(result);

      setMessage(
        "File uploaded and initial validation completed."
      );

    } catch (err: any) {

      setError(
        err.response?.data?.detail ||
        "File upload failed."
      );

    } finally {

      setLoading(false);
    }
  };


  // =========================================================
  // Validation
  // =========================================================

  const handleValidate = async () => {

    if (!file) {

      setError(
        "Please select a CSV file first."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setMessage("");

      const result =
        await validateImport(
          importType,
          file
        );

      setValidationResult(result);

      setMessage(
        "Validation completed successfully."
      );

    } catch (err: any) {

      setError(
        err.response?.data?.detail ||
        "Validation failed."
      );

    } finally {

      setLoading(false);
    }
  };


  // =========================================================
  // Process import
  // =========================================================

  const handleProcess = async () => {

    if (!file) {

      setError(
        "Please select a CSV file first."
      );

      return;
    }


    if (!uploadResult?.import_id) {

      setError(
        "Please upload the file before processing."
      );

      return;
    }


    if (
      validationResult &&
      !validationResult.can_import
    ) {

      setError(
        "There are no valid records available for import."
      );

      return;
    }


    try {

      setLoading(true);
      setError("");
      setMessage("");

      const result =
        await processImport(
          uploadResult.import_id,
          importType,
          file
        );

      setMessage(
        `Import completed: ${result.status}`
      );

      await loadHistory();

    } catch (err: any) {

      setError(
        err.response?.data?.detail ||
        "Import processing failed."
      );

    } finally {

      setLoading(false);
    }
  };


  // =========================================================
  // History
  // =========================================================

  const loadHistory = async () => {

    try {

      const result =
        await getImportHistory();

      setHistory(result);

    } catch (err) {

      console.error(
        "Failed to load import history",
        err
      );
    }
  };


  // =========================================================
  // View errors
  // =========================================================

  const handleViewErrors = async (
    importId: number
  ) => {

    try {

      const result =
        await getImportErrors(
          importId
        );

      setErrorRecords(result);

    } catch (err) {

      setError(
        "Unable to load import errors."
      );
    }
  };


  // =========================================================
  // Load history on button click
  // =========================================================

  const handleLoadHistory = async () => {

    setError("");

    await loadHistory();
  };


  // =========================================================
  // Render
  // =========================================================

  return (

    <>
      <Sidebar />

      <Navbar />

      <div className="data-import-page">

        <div className="data-import-container">

          <div className="data-import-header">

            <h1 className="data-import-title">
              Data Import
            </h1>

            <p className="data-import-subtitle">
              Upload, validate, and import CSV data
            </p>

          </div>


          {/* =====================================================
              Upload Section
          ===================================================== */}

          <Card className="import-card">

            <CardContent>

              <h2 className="import-card-title">
                Upload CSV
              </h2>


              <div className="import-controls">

                <FormControl
                  className="import-type-control"
                >

                  <InputLabel>
                    Import Type
                  </InputLabel>

                  <Select
                    value={importType}
                    label="Import Type"
                    onChange={
                      handleImportTypeChange
                    }
                  >

                    <MenuItem value="products">
                      Products
                    </MenuItem>

                    <MenuItem value="customers">
                      Customers
                    </MenuItem>

                    <MenuItem value="sales">
                      Sales Transactions
                    </MenuItem>

                  </Select>

                </FormControl>


                <input
                  className="import-file-input"
                  type="file"
                  accept=".csv"
                  onChange={
                    handleFileChange
                  }
                />

              </div>


              {file && (

                <div className="selected-file">

                  <span className="selected-file-name">
                    Selected file:{" "}
                    <strong>
                      {file.name}
                    </strong>
                  </span>

                </div>

              )}


              <div className="import-actions">

                <Button
                  className="data-import-btn"
                  variant="contained"
                  onClick={handleUpload}
                  disabled={
                    !file ||
                    loading
                  }
                >

                  {loading ? (
                    <CircularProgress
                      size={22}
                      color="inherit"
                    />
                  ) : (
                    "Upload & Preview"
                  )}

                </Button>


                <Button
                  className="data-import-btn"
                  variant="contained"
                  onClick={handleValidate}
                  disabled={
                    !file ||
                    loading
                  }
                >
                  Validate
                </Button>


                <Button
                  className="data-import-btn"
                  variant="contained"
                  onClick={handleProcess}
                  disabled={
                    !file ||
                    !uploadResult ||
                    loading
                  }
                >
                  Import Data
                </Button>

              </div>

            </CardContent>

          </Card>


          {/* =====================================================
              Messages
          ===================================================== */}

          {message && (

            <Alert
              className="import-alert"
              severity="success"
            >
              {message}
            </Alert>

          )}


          {error && (

            <Alert
              className="import-alert"
              severity="error"
            >
              {error}
            </Alert>

          )}


          {/* =====================================================
              Preview
          ===================================================== */}

          {uploadResult && (

            <Card className="import-card">

              <CardContent>

                <h2 className="import-card-title">
                  CSV Preview
                </h2>


                <div className="import-details">

                  <p>
                    Filename:{" "}
                    <strong>
                      {uploadResult.filename}
                    </strong>
                  </p>

                  <p>
                    Total Records:{" "}
                    <strong>
                      {uploadResult.total_records}
                    </strong>
                  </p>

                  <p>
                    Detected Columns:{" "}
                    <strong>
                      {uploadResult.columns.join(", ")}
                    </strong>
                  </p>

                </div>


                <div className="import-table-wrapper">

                  <Table className="import-table">

                    <TableHead>

                      <TableRow>

                        {uploadResult.columns.map(
                          (column) => (

                            <TableCell
                              key={column}
                            >
                              <strong>
                                {column}
                              </strong>
                            </TableCell>

                          )
                        )}

                      </TableRow>

                    </TableHead>


                    <TableBody>

                      {uploadResult.preview.map(
                        (row, index) => (

                          <TableRow
                            key={index}
                          >

                            {uploadResult.columns.map(
                              (column) => (

                                <TableCell
                                  key={column}
                                >
                                  {row[column]}
                                </TableCell>

                              )
                            )}

                          </TableRow>

                        )
                      )}

                    </TableBody>

                  </Table>

                </div>

              </CardContent>

            </Card>

          )}


          {/* =====================================================
              Validation Summary
          ===================================================== */}

          {validationResult && (

            <Card className="import-card">

              <CardContent>

                <h2 className="import-card-title">
                  Validation Result
                </h2>


                <div className="validation-summary">

                  <div className="validation-box total-box">

                    <span className="validation-label">
                      Total Records
                    </span>

                    <span className="validation-number total-count">
                      {validationResult.total_records}
                    </span>

                  </div>


                  <div className="validation-box valid-box">

                    <span className="validation-label">
                      Valid Records
                    </span>

                    <span className="validation-number valid-count">
                      {validationResult.valid_records}
                    </span>

                  </div>


                  <div className="validation-box invalid-box">

                    <span className="validation-label">
                      Invalid Records
                    </span>

                    <span className="validation-number invalid-count">
                      {validationResult.invalid_records}
                    </span>

                  </div>


                  <div className="validation-box duplicate-box">

                    <span className="validation-label">
                      Duplicate Records
                    </span>

                    <span className="validation-number duplicate-count">
                      {validationResult.duplicate_records}
                    </span>

                  </div>

                </div>


                {validationResult.errors.length > 0 && (

                  <div className="validation-errors">

                    <h3 className="section-subtitle">
                      Validation Errors
                    </h3>


                    <div className="import-table-wrapper">

                      <Table className="import-table">

                        <TableHead>

                          <TableRow>

                            <TableCell>
                              Row
                            </TableCell>

                            <TableCell>
                              Type
                            </TableCell>

                            <TableCell>
                              Error
                            </TableCell>

                          </TableRow>

                        </TableHead>


                        <TableBody>

                          {validationResult.errors.map(
                            (item, index) => (

                              <TableRow
                                key={index}
                              >

                                <TableCell>
                                  {item.row_number}
                                </TableCell>

                                <TableCell>
                                  {item.error_type}
                                </TableCell>

                                <TableCell>
                                  {item.error_message}
                                </TableCell>

                              </TableRow>

                            )
                          )}

                        </TableBody>

                      </Table>

                    </div>

                  </div>

                )}

              </CardContent>

            </Card>

          )}


          {/* =====================================================
              Import History
          ===================================================== */}

          <Card className="import-card">

            <CardContent>

              <div className="history-header">

                <h2 className="import-card-title">
                  Import History
                </h2>

                <Button
                  className="data-import-btn"
                  variant="contained"
                  onClick={handleLoadHistory}
                >
                  Load History
                </Button>

              </div>


              <div className="import-table-wrapper">

                <Table className="import-table">

                  <TableHead>

                    <TableRow>

                      <TableCell>
                        ID
                      </TableCell>

                      <TableCell>
                        Type
                      </TableCell>

                      <TableCell>
                        Filename
                      </TableCell>

                      <TableCell>
                        Total
                      </TableCell>

                      <TableCell>
                        Successful
                      </TableCell>

                      <TableCell>
                        Failed
                      </TableCell>

                      <TableCell>
                        Duplicates
                      </TableCell>

                      <TableCell>
                        Status
                      </TableCell>

                      <TableCell>
                        Errors
                      </TableCell>

                    </TableRow>

                  </TableHead>


                  <TableBody>

                    {history.map(
                      (item) => (

                        <TableRow
                          key={item.id}
                        >

                          <TableCell>
                            {item.id}
                          </TableCell>

                          <TableCell>
                            {item.import_type}
                          </TableCell>

                          <TableCell>
                            {item.filename}
                          </TableCell>

                          <TableCell>
                            {item.total_records}
                          </TableCell>

                          <TableCell>
                            {item.successful_records}
                          </TableCell>

                          <TableCell>
                            {item.failed_records}
                          </TableCell>

                          <TableCell>
                            {item.duplicate_records}
                          </TableCell>

                          <TableCell>
                            {item.status}
                          </TableCell>

                          <TableCell>

                            <Button
                              className="table-action-btn"
                              size="small"
                              onClick={() =>
                                handleViewErrors(
                                  item.id
                                )
                              }
                            >
                              View
                            </Button>

                          </TableCell>

                        </TableRow>

                      )
                    )}

                  </TableBody>

                </Table>

              </div>

            </CardContent>

          </Card>


          {/* =====================================================
              Error Details
          ===================================================== */}

          {errorRecords.length > 0 && (

            <Card className="import-card">

              <CardContent>

                <h2 className="import-card-title">
                  Import Errors
                </h2>


                <div className="import-table-wrapper">

                  <Table className="import-table">

                    <TableHead>

                      <TableRow>

                        <TableCell>
                          Row
                        </TableCell>

                        <TableCell>
                          Type
                        </TableCell>

                        <TableCell>
                          Message
                        </TableCell>

                      </TableRow>

                    </TableHead>


                    <TableBody>

                      {errorRecords.map(
                        (item, index) => (

                          <TableRow
                            key={index}
                          >

                            <TableCell>
                              {item.row_number}
                            </TableCell>

                            <TableCell>
                              {item.error_type}
                            </TableCell>

                            <TableCell>
                              {item.error_message}
                            </TableCell>

                          </TableRow>

                        )
                      )}

                    </TableBody>

                  </Table>

                </div>

              </CardContent>

            </Card>

          )}

        </div>

      </div>

    </>
  );
}