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
    headers: { 'Content-Type': 'multipart/form-data' },
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