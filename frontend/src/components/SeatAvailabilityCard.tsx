'use client';

import { useSeatAvailability } from '@/lib/hooks';
import { cn, getStatusColor, formatTime, formatPercentage } from '@/lib/utils';
import { Users, RefreshCw, Clock } from 'lucide-react';

export default function SeatAvailabilityCard() {
  const { data, isLoading, isError, mutate } = useSeatAvailability();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div className="h-32 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-center text-red-600">
          <p className="text-lg font-semibold">Unable to load seat data</p>
          <p className="text-sm mt-2">Please check backend connection</p>
          <button
            onClick={() => mutate()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const statusColorClass = getStatusColor(data.status);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Seat Availability</h2>
        <button
          onClick={() => mutate()}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          title="Refresh"
        >
          <RefreshCw className="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-700 font-medium">Available</p>
              <p className="text-3xl font-bold text-green-600">
                {data.available_seats}
              </p>
            </div>
            <Users className="w-10 h-10 text-green-600 opacity-50" />
          </div>
        </div>

        <div className="bg-red-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-700 font-medium">Occupied</p>
              <p className="text-3xl font-bold text-red-600">
                {data.occupied_seats}
              </p>
            </div>
            <Users className="w-10 h-10 text-red-600 opacity-50" />
          </div>
        </div>

        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-700 font-medium">Total</p>
              <p className="text-3xl font-bold text-blue-600">
                {data.total_seats}
              </p>
            </div>
            <Users className="w-10 h-10 text-blue-600 opacity-50" />
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-gray-700 font-medium">Occupancy Rate</span>
          <span className="text-lg font-bold text-gray-900">
            {formatPercentage(data.occupancy_rate)}
          </span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            className={cn(
              'h-full transition-all duration-500',
              data.occupancy_rate < 50
                ? 'bg-green-500'
                : data.occupancy_rate < 80
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
            )}
            style={{ width: `${data.occupancy_rate}%` }}
          />
        </div>

        <div className="flex items-center justify-between pt-2">
          <span
            className={cn(
              'inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold',
              statusColorClass
            )}
          >
            {data.status ? data.status.toUpperCase() : 'UNKNOWN'}
          </span>
          <span className="text-sm text-gray-500 flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {formatTime(data.last_updated)}
          </span>
        </div>
      </div>
    </div>
  );
}
