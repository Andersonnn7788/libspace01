import useSWR from 'swr';
import {
  getSeatAvailability,
  getStatistics,
  getCameraStatus,
  getHealth,
  getDetections,
} from './api';

const REFRESH_INTERVAL = parseInt(
  process.env.NEXT_PUBLIC_REFRESH_INTERVAL || '5000',
  10
);

export function useSeatAvailability() {
  const { data, error, isLoading, mutate } = useSWR(
    'seat-availability',
    getSeatAvailability,
    {
      refreshInterval: REFRESH_INTERVAL,
      revalidateOnFocus: true,
      dedupingInterval: 2000,
    }
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useStatistics() {
  const { data, error, isLoading, mutate } = useSWR(
    'statistics',
    getStatistics,
    {
      refreshInterval: REFRESH_INTERVAL,
      revalidateOnFocus: true,
      dedupingInterval: 2000,
    }
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useCameraStatus() {
  const { data, error, isLoading } = useSWR(
    'camera-status',
    getCameraStatus,
    {
      refreshInterval: REFRESH_INTERVAL,
      revalidateOnFocus: true,
    }
  );

  return {
    data,
    isLoading,
    isError: error,
  };
}

export function useHealth() {
  const { data, error, isLoading } = useSWR('health', getHealth, {
    refreshInterval: 10000,
    revalidateOnFocus: true,
  });

  return {
    data,
    isLoading,
    isError: error,
  };
}

export function useDetections() {
  const { data, error, isLoading } = useSWR('detections', getDetections, {
    refreshInterval: REFRESH_INTERVAL,
    revalidateOnFocus: true,
  });

  return {
    data,
    isLoading,
    isError: error,
  };
}
