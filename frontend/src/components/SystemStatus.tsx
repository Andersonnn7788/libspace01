'use client';

import { useHealth } from '@/lib/hooks';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';
import { formatUptime } from '@/lib/utils';

export default function SystemStatus() {
  const { data, isLoading, isError } = useHealth();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4 animate-pulse">
        <div className="h-20 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center gap-2 text-red-700">
          <XCircle className="w-5 h-5" />
          <span className="font-semibold">System Offline</span>
        </div>
      </div>
    );
  }

  const isHealthy =
    data.status === 'healthy' && data.camera_active && data.detection_active;

  return (
    <div
      className={`rounded-lg shadow-lg p-4 ${
        isHealthy
          ? 'bg-green-50 border border-green-200'
          : 'bg-yellow-50 border border-yellow-200'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {isHealthy ? (
            <CheckCircle className="w-6 h-6 text-green-600" />
          ) : (
            <Activity className="w-6 h-6 text-yellow-600" />
          )}
          <div>
            <h4
              className={`font-semibold ${
                isHealthy ? 'text-green-900' : 'text-yellow-900'
              }`}
            >
              System Status: {data.status.toUpperCase()}
            </h4>
            <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
              <span className="flex items-center gap-1">
                <div
                  className={`w-2 h-2 rounded-full ${
                    data.camera_active ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
                Camera
              </span>
              <span className="flex items-center gap-1">
                <div
                  className={`w-2 h-2 rounded-full ${
                    data.detection_active ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
                Detection
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                Uptime: {formatUptime(data.uptime_seconds)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
