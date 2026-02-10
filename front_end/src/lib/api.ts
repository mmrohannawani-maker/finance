// src/lib/api.ts
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// File operations
export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/files/upload', formData, {
    // headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getFiles = async () => {
  return api.get('/files');
};

export const getFileData = async (fileId: string, page = 1, limit = 50) => {
  return api.get(`/files/${fileId}/data`, { params: { page, limit } });
};

export const deleteFile = async (fileId: string) => {
  return api.delete(`/files/${fileId}`);
};

// Analysis APIs
export const startAnalysis = async (fileId: string, analysisType: string) => {
  return api.post('/analysis/', {
    file_id: fileId,
    analysis_type: analysisType,
    status: "running"
  });
};

export const getAnalysis = async (analysisId: string) => {
  return api.get(`/analysis/${analysisId}`);
};

export const getFileAnalyses = async (fileId: string) => {
  return api.get(`/analysis/file/${fileId}`);
};

// Quick analysis endpoints
export const runSummaryAnalysis = async (fileId: string) => {
  return api.post(`/analysis/run/summary/${fileId}`);
};

export const runTrendAnalysis = async (fileId: string) => {
  return api.post(`/analysis/run/trend/${fileId}`);
};

export const runCorrelationAnalysis = async (fileId: string) => {
  return api.post(`/analysis/run/correlation/${fileId}`);
};