import socket
import time
import subprocess
import requests

def log_time(operation, start_time):
    end_time = time.time()
    print(f"{operation} took {end_time - start_time:.2f} seconds")
    return end_time

def test_dns():
    start = time.time()
    try:
        socket.gethostbyname('sheets.googleapis.com')
        return time.time() - start
    except socket.gaierror:
        return None

def test_ping():
    try:
        result = subprocess.run(['ping', '-n', '1', 'sheets.googleapis.com'], 
                              capture_output=True, text=True)
        return 'time=' in result.stdout
    except:
        return False

def test_traceroute():
    try:
        result = subprocess.run(['tracert', 'sheets.googleapis.com'], 
                              capture_output=True, text=True)
        return result.stdout
    except:
        return None

def test_google_services():
    endpoints = {
        'Sheets API': 'https://sheets.googleapis.com/v4/spreadsheets',
        'Drive API': 'https://www.googleapis.com/drive/v3/files',
        'Google': 'https://www.google.com'
    }
    
    print("Network Diagnostics:")
    print("-" * 50)
    
    # DNS Test
    dns_time = test_dns()
    print(f"DNS Resolution: {'OK' if dns_time else 'FAILED'}")
    if dns_time:
        print(f"DNS lookup time: {dns_time:.2f}s")
    
    # Ping Test
    print(f"Ping Test: {'OK' if test_ping() else 'FAILED'}")
    
    # Traceroute Test
    print("\nTraceroute Test:")
    traceroute_result = test_traceroute()
    if traceroute_result:
        print(traceroute_result)
    else:
        print("Traceroute failed")
    
    # Endpoints Test
    for service, url in endpoints.items():
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5)
            elapsed = time.time() - start_time
            print(f"\n{service}:")
            print(f"Status: {response.status_code}")
            print(f"Response time: {elapsed:.2f}s")
        except requests.exceptions.RequestException as e:
            print(f"\n{service}:")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_google_services()