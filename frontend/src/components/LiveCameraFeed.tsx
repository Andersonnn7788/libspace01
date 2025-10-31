'use client';

import { useState } from 'react';
import { useCameraStatus } from '@/lib/hooks';
import { getCameraStreamUrl } from '@/lib/api';
import { Camera, AlertCircle } from 'lucide-react';

export default function LiveCameraFeed() {
  const { data: cameraStatus, isLoading, isError } = useCameraStatus();
  const [imageError, setImageError] = useState(false);

  const streamUrl = getCameraStreamUrl();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="aspect-video bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
          <Camera className="w-5 h-5 text-blue-600" />
          Live Camera Feed
        </h3>
        {cameraStatus && (
          <div className="flex items-center gap-2">
            <span
              className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold ${
                cameraStatus.is_active
                  ? 'bg-green-100 text-green-700'
                  : 'bg-red-100 text-red-700'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  cameraStatus.is_active ? 'bg-green-600' : 'bg-red-600'
                }`}
              />
              {cameraStatus.is_active ? 'Active' : 'Inactive'}
            </span>
            {cameraStatus.is_active && (
              <span className="text-xs text-gray-500">
                {cameraStatus.current_fps.toFixed(1)} FPS
              </span>
            )}
          </div>
        )}
      </div>

      <div className="relative aspect-video bg-gray-900 rounded-lg overflow-hidden">
        {isError || imageError ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
            <AlertCircle className="w-12 h-12 mb-2" />
            <p className="text-sm">Camera feed unavailable</p>
            <button
              onClick={() => setImageError(false)}
              className="mt-4 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
            >
              Retry
            </button>
          </div>
        ) : (
          <img
            src={streamUrl}
            alt="Live camera feed"
            className="w-full h-full object-contain"
            onError={() => setImageError(true)}
          />
        )}
      </div>

      {cameraStatus && cameraStatus.is_active && (
        <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
          <span>
            Resolution: {cameraStatus.resolution.width}x
            {cameraStatus.resolution.height}
          </span>
          <span>Last updated: {new Date().toLocaleTimeString()}</span>
        </div>
      )}
    </div>
  );
}
