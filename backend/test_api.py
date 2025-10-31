"""
Simple test client for LibSpace API
Tests all major endpoints
"""
import requests
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"  # Update with your Raspberry Pi IP


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_seats_availability():
    """Test seat availability endpoint"""
    print("\n=== Testing Seat Availability ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/seats/availability", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total Seats: {data.get('total_seats')}")
        print(f"Occupied: {data.get('occupied_seats')}")
        print(f"Available: {data.get('available_seats')}")
        print(f"Occupancy Rate: {data.get('occupancy_rate'):.2f}%")
        print(f"Detections: {len(data.get('detections', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_statistics():
    """Test statistics endpoint"""
    print("\n=== Testing Statistics ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/statistics/current", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        
        # Overall stats
        avail = data.get('current_availability', {})
        print(f"\nOverall Statistics:")
        print(f"  Total: {avail.get('total_seats')}")
        print(f"  Available: {avail.get('available_seats')}")
        print(f"  Occupancy: {avail.get('occupancy_rate'):.2f}%")
        
        # Zone stats
        print(f"\nZone Statistics:")
        for zone in data.get('zones', []):
            print(f"  {zone['zone_name']}:")
            print(f"    Total: {zone['total_seats']}")
            print(f"    Available: {zone['available_seats']}")
            print(f"    Occupancy: {zone['occupancy_rate']:.2f}%")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_camera_status():
    """Test camera status endpoint"""
    print("\n=== Testing Camera Status ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/camera/status", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Camera Running: {data.get('is_running')}")
        print(f"Resolution: {data.get('width')}x{data.get('height')}")
        print(f"FPS: {data.get('fps')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_snapshot():
    """Test snapshot endpoint"""
    print("\n=== Testing Snapshot ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/camera/snapshot", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Save snapshot
            filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Snapshot saved: {filename}")
            print(f"Size: {len(response.content)} bytes")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("LibSpace API Test Suite")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now()}")
    
    results = {
        "Health Check": test_health(),
        "Seat Availability": test_seats_availability(),
        "Statistics": test_statistics(),
        "Camera Status": test_camera_status(),
        "Snapshot": test_snapshot()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 50)


if __name__ == "__main__":
    # Update BASE_URL if needed
    import sys
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    
    run_all_tests()
