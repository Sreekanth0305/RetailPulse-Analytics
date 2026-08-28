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