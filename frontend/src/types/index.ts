// API Response Types

export interface SeatAvailability {
  available_seats: number;
  occupied_seats: number;
  hogged_seats: number;
  total_seats: number;
  occupancy_rate: number;
  last_updated: string;
  status: 'available' | 'busy' | 'full';
}

export interface SeatStatus {
  available: number;
  occupied: number;
  total: number;
  status: string;
}

export interface Detection {
  class_name: string;
  confidence: number;
  bbox: number[];
}

export interface DetectionData {
  detections: Detection[];
  count: number;
  timestamp: string;
}

export interface ZoneStatistics {
  zone_name: string;
  total_seats: number;
  occupied_seats: number;
  available_seats: number;
  occupancy_rate: number;
}

export interface Statistics {
  current_availability: SeatAvailability;
  zones: ZoneStatistics[];
  timestamp: string;
  average_occupancy_today?: number;
  peak_occupancy_today?: number;
}

export interface CameraStatus {
  is_active: boolean;
  current_fps: number;
  resolution: {
    width: number;
    height: number;
  };
  last_frame_time: string;
}

export interface CameraInfo {
  width: number;
  height: number;
  fps: number;
  rotation: number;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  uptime_seconds: number;
  camera_active: boolean;
  detection_active: boolean;
}
