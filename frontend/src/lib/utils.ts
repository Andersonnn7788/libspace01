import { type ClassValue, clsx } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString();
}

export function formatTime(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleTimeString();
}

export function getStatusColor(status: string): string {
  if (!status) {
    return 'text-gray-600 bg-gray-50';
  }

  switch (status.toLowerCase()) {
    case 'available':
      return 'text-green-600 bg-green-50';
    case 'busy':
      return 'text-yellow-600 bg-yellow-50';
    case 'full':
      return 'text-red-600 bg-red-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
}

export function getOccupancyColor(rate: number): string {
  if (rate < 50) return 'text-green-600';
  if (rate < 80) return 'text-yellow-600';
  return 'text-red-600';
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`;
}

export function formatUptime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`;
  } else {
    return `${secs}s`;
  }
}
