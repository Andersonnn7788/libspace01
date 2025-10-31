'use client';

import { useStatistics } from '@/lib/hooks';
import { cn, formatPercentage, getOccupancyColor } from '@/lib/utils';
import { MapPin } from 'lucide-react';

export default function ZoneList() {
  const { data, isLoading, isError } = useStatistics();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (isError || !data?.zones) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Zone Occupancy</h3>
        <p className="text-gray-500 text-center py-4">No zone data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
        <MapPin className="w-5 h-5 text-blue-600" />
        Zone Occupancy
      </h3>

      <div className="space-y-3">
        {data.zones.map((zone) => (
          <div
            key={zone.zone_name}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-semibold text-gray-800">{zone.zone_name}</h4>
              <span
                className={cn(
                  'text-sm font-bold',
                  getOccupancyColor(zone.occupancy_rate)
                )}
              >
                {formatPercentage(zone.occupancy_rate)}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>
                {zone.available_seats} / {zone.total_seats} available
              </span>
              <span className="text-gray-500">
                {zone.occupied_seats} occupied
              </span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className={cn(
                  'h-full transition-all duration-500',
                  zone.occupancy_rate < 50
                    ? 'bg-green-500'
                    : zone.occupancy_rate < 80
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                )}
                style={{ width: `${zone.occupancy_rate}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
