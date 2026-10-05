import axios from "../api/axios";


const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
};


// =========================================================
// 1. Upload
// POST /api/import/upload
// =========================================================

export const uploadImport = async (
  importType: string,
  file: File
) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `/api/import/upload?import_type=${encodeURIComponent(importType)}`,
    formData,
    {
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// =========================================================
// 2. Validate
// POST /api/import/validate
// =========================================================

export const validateImport = async (
  importType: string,
  file: File
) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `/api/import/validate?import_type=${encodeURIComponent(importType)}`,
    formData,
    {
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// =========================================================
// 3. Process
// POST /api/import/process
// =========================================================

export const processImport = async (
  importId: number,
  importType: string,
  file: File
) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `/api/import/process?import_id=${importId}&import_type=${encodeURIComponent(importType)}`,
    formData,
    {
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// =========================================================
// 4. History
// GET /api/import/history
// =========================================================

export const getImportHistory = async () => {

  const response = await axios.get(
    "/api/import/history",
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// 5. Import Details
// GET /api/import/{import_id}
// =========================================================

export const getImportDetails = async (
  importId: number
) => {

  const response = await axios.get(
    `/api/import/${importId}`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// =========================================================
// 6. Import Errors
// GET /api/import/{import_id}/errors
// =========================================================

export const getImportErrors = async (
  importId: number
) => {

  const response = await axios.get(
    `/api/import/${importId}/errors`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};

// =========================================================
// Download Import Error CSV
// GET /api/import/{import_id}/errors/download
// =========================================================

export const downloadImportErrors = async (
  importId: number
): Promise<void> => {

  const response = await axios.get(
    `/api/import/${importId}/errors/download`,
    {
      headers: getAuthHeaders(),
      responseType: "blob",
    }
  );

  const blob = new Blob(
    [response.data],
    { type: "text/csv" }
  );

  const url =
    window.URL.createObjectURL(blob);

  const link =
    document.createElement("a");

  link.href = url;

  link.download =
    `import_${importId}_error_report.csv`;

  document.body.appendChild(link);

  link.click();

  document.body.removeChild(link);

  window.URL.revokeObjectURL(url);
};

export const downloadImportTemplate = async (
    importType: string
): Promise<void> => {
    const response = await axios.get(
        `/api/import/templates/${importType}`,
        {
            headers: getAuthHeaders(),
            responseType: "blob"
        }
    );

    const blob = new Blob(
        [response.data],
        { type: "text/csv" }
    );

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download = `${importType}_import_template.csv`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
};

export const getImportStatus = async (
    importId: number
) => {

    const response = await axios.get(
        `/api/import/${importId}/status`,
        {
          headers: getAuthHeaders(),
        }
    );

    return response.data;
};

export const cancelImport = async (
  importId: number
) => {

  const response = await axios.post(
    `/api/import/${importId}/cancel`,
    {},
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};