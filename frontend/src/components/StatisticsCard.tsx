'use client';

import { useStatistics } from '@/lib/hooks';
import { BarChart3, Users, TrendingUp, Activity } from 'lucide-react';
import { formatTime } from '@/lib/utils';

export default function StatisticsCard() {
  const { data, isLoading, isError } = useStatistics();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div className="grid grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-24 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return null;
  }

  const availability = data.current_availability;

  const stats = [
    {
      label: 'Total Seats',
      value: availability?.total_seats || 0,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Current Detections',
      value: availability?.detections?.length || 0,
      icon: Activity,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      label: 'Available Now',
      value: availability?.available_seats || 0,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      label: 'Occupancy',
      value: `${(availability?.occupancy_rate || 0).toFixed(1)}%`,
      icon: BarChart3,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-800">Statistics</h3>
        <span className="text-xs text-gray-500">
          Updated: {formatTime(availability?.last_updated || data.timestamp)}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className={`${stat.bgColor} rounded-lg p-4 transition-all hover:shadow-md`}
          >
            <div className="flex items-center justify-between mb-2">
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            <p className="text-sm text-gray-600 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {(data.average_occupancy_today !== undefined ||
        data.peak_occupancy_today !== undefined) && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-sm">
            {data.average_occupancy_today !== undefined && (
              <div>
                <p className="text-gray-600">Avg Today</p>
                <p className="text-lg font-semibold text-gray-900">
                  {data.average_occupancy_today.toFixed(1)}%
                </p>
              </div>
            )}
            {data.peak_occupancy_today !== undefined && (
              <div>
                <p className="text-gray-600">Peak Today</p>
                <p className="text-lg font-semibold text-gray-900">
                  {data.peak_occupancy_today.toFixed(1)}%
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
