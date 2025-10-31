'use client';

import SeatAvailabilityCard from '@/components/SeatAvailabilityCard';
import StatisticsCard from '@/components/StatisticsCard';
import ZoneList from '@/components/ZoneList';
import LiveCameraFeed from '@/components/LiveCameraFeed';
import OccupancyChart from '@/components/OccupancyChart';
import SystemStatus from '@/components/SystemStatus';
import { Library } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-blue-600 rounded-lg">
              <Library className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">LibSpace</h1>
              <p className="text-gray-600">
                Real-time Library Seat Availability Monitor
              </p>
            </div>
          </div>
        </div>

        {/* System Status */}
        <div className="mb-6">
          <SystemStatus />
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Left Column */}
          <div className="space-y-6">
            <SeatAvailabilityCard />
            <StatisticsCard />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <LiveCameraFeed />
          </div>
        </div>

        {/* Charts and Zones */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <OccupancyChart />
          <ZoneList />
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500">
          <p>
            LibSpace - Powered by YOLO Object Detection & Raspberry Pi 4
          </p>
          <p className="mt-1">
            Built with Next.js, FastAPI, and Computer Vision
          </p>
        </footer>
      </div>
    </main>
  );
}
