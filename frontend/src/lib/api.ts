import axios from 'axios';
import type {
  SeatAvailability,
  SeatStatus,
  DetectionData,
  Statistics,
  CameraStatus,
  CameraInfo,
  HealthStatus,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Seat endpoints
export const getSeatAvailability = async (): Promise<SeatAvailability> => {
  const response = await api.get<SeatAvailability>('/api/v1/seats/availability');
  return response.data;
};

export const getSeatStatus = async (): Promise<SeatStatus> => {
  const response = await api.get<SeatStatus>('/api/v1/seats/status');
  return response.data;
};

export const getDetections = async (): Promise<DetectionData> => {
  const response = await api.get<DetectionData>('/api/v1/seats/detections');
  return response.data;
};

// Statistics endpoints
export const getStatistics = async (): Promise<Statistics> => {
  const response = await api.get<Statistics>('/api/v1/statistics/current');
  return response.data;
};

// Camera endpoints
export const getCameraStatus = async (): Promise<CameraStatus> => {
  const response = await api.get<CameraStatus>('/api/v1/camera/status');
  return response.data;
};

export const getCameraInfo = async (): Promise<CameraInfo> => {
  const response = await api.get<CameraInfo>('/api/v1/camera/info');
  return response.data;
};

export const getCameraStreamUrl = (): string => {
  return `${API_URL}/api/v1/camera/stream`;
};

export const getCameraSnapshotUrl = (): string => {
  return `${API_URL}/api/v1/camera/snapshot`;
};

// Health endpoint
export const getHealth = async (): Promise<HealthStatus> => {
  const response = await api.get<HealthStatus>('/health');
  return response.data;
};

export default api;
