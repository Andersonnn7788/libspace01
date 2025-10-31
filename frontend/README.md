# LibSpace Frontend

Next.js web application for real-time library seat availability monitoring.

## Features

- **Real-time Seat Availability**: Live updates of available and occupied seats
- **Live Camera Feed**: MJPEG stream from Raspberry Pi camera
- **Zone-wise Statistics**: Occupancy data for different library zones
- **Interactive Charts**: Visual representation of seat occupancy
- **System Status**: Health monitoring of backend services
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Auto-refresh**: Data updates every 5 seconds (configurable)

## Technology Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **SWR**: Data fetching and caching
- **Recharts**: Data visualization
- **Lucide React**: Icon library
- **Axios**: HTTP client

## Prerequisites

- Node.js 18+ and npm/yarn
- Running LibSpace backend (Raspberry Pi)

## Installation

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
# or
yarn install
```

3. **Configure environment variables**:
```bash
cp .env.example .env
nano .env
```

Update the `.env` file:
```env
NEXT_PUBLIC_API_URL=http://192.168.1.100:8000
NEXT_PUBLIC_REFRESH_INTERVAL=5000
```

Replace `192.168.1.100` with your Raspberry Pi's IP address.

## Development

Run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

The page auto-updates as you edit files.

## Production Build

1. **Build the application**:
```bash
npm run build
# or
yarn build
```

2. **Start the production server**:
```bash
npm start
# or
yarn start
```

The app will be available at `http://localhost:3000`.

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── page.tsx        # Main dashboard page
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   ├── components/         # React components
│   │   ├── SeatAvailabilityCard.tsx
│   │   ├── StatisticsCard.tsx
│   │   ├── ZoneList.tsx
│   │   ├── LiveCameraFeed.tsx
│   │   ├── OccupancyChart.tsx
│   │   └── SystemStatus.tsx
│   ├── lib/               # Utilities
│   │   ├── api.ts        # API client
│   │   ├── hooks.ts      # Custom React hooks
│   │   └── utils.ts      # Utility functions
│   └── types/            # TypeScript types
│       └── index.ts
├── public/               # Static assets
├── .env.example         # Environment variables template
├── next.config.js       # Next.js configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json
```

## Components

### SeatAvailabilityCard
Main component displaying:
- Available seats count
- Occupied seats count
- Total seats
- Occupancy rate with progress bar
- Current status (Available/Busy/Full)

### StatisticsCard
Shows comprehensive statistics:
- Total seats
- Current detections
- Available seats
- Occupancy percentage

### ZoneList
Displays zone-wise occupancy:
- Individual zone status
- Seats per zone
- Zone occupancy rate
- Visual progress bars

### LiveCameraFeed
Live video feed component:
- MJPEG stream from backend
- Camera status indicator
- FPS display
- Resolution info

### OccupancyChart
Bar chart visualization:
- Zone-wise occupancy comparison
- Color-coded by occupancy level
- Interactive tooltips

### SystemStatus
Backend health monitoring:
- System status
- Camera status
- Detection service status
- Uptime display

## API Integration

The frontend consumes the following backend APIs:

- `GET /api/v1/seats/availability` - Seat data
- `GET /api/v1/statistics/current` - Statistics
- `GET /api/v1/camera/status` - Camera status
- `GET /api/v1/camera/stream` - Live stream
- `GET /health` - System health

All API calls use SWR for automatic caching, revalidation, and polling.

## Configuration

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (required)
- `NEXT_PUBLIC_REFRESH_INTERVAL`: Data refresh interval in ms (default: 5000)

### Refresh Interval

Adjust the refresh rate by modifying `NEXT_PUBLIC_REFRESH_INTERVAL`:
- Development: 5000ms (5 seconds)
- Production: 5000-10000ms recommended

### CORS Configuration

Ensure the backend `.env` includes your frontend URL:
```
CORS_ORIGINS=http://localhost:3000,http://your-domain.com
```

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t libspace-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://your-pi-ip:8000 libspace-frontend
```

### Static Export (Optional)

For static hosting:

1. Update `next.config.js`:
```javascript
const nextConfig = {
  output: 'export',
}
```

2. Build:
```bash
npm run build
```

3. Deploy the `out` folder to any static host.

**Note**: Live features require server-side rendering.

## Customization

### Colors

Edit `tailwind.config.js` to customize the color scheme:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      },
    },
  },
}
```

### Layout

Modify `src/app/page.tsx` to change the dashboard layout.

### Styling

All components use Tailwind CSS. Customize styles directly in component files.

## Performance Optimization

1. **Reduce Refresh Interval**: Increase `NEXT_PUBLIC_REFRESH_INTERVAL`
2. **Enable Caching**: SWR automatically caches responses
3. **Optimize Images**: Next.js Image component (for future enhancements)
4. **Code Splitting**: Automatic with Next.js

## Troubleshooting

### Cannot connect to backend
- Check `NEXT_PUBLIC_API_URL` in `.env`
- Verify Raspberry Pi is running and accessible
- Check CORS configuration in backend

### Camera feed not loading
- Ensure backend camera service is running
- Check network connectivity
- Verify `/api/v1/camera/stream` endpoint is accessible

### Data not updating
- Check browser console for errors
- Verify SWR hooks are properly configured
- Check refresh interval setting

### Build errors
```bash
# Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run build
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Check backend connection first
- Review browser console for errors
- Check backend API documentation

---

Built with Next.js and TypeScript
