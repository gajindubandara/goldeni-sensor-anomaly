import websocket
import json
import csv
import time

try:
    import thread
except ImportError:
    import _thread as thread

# Define WebSocket callback functions
def on_message(ws, message):
    try:
        data = json.loads(message)
        # Example data: {'id': 1, 'name': 'Alice', 'timestamp': '2021-01-01T12:00:00Z'}
        print("Received data: ", data)

        # Write to CSV
        with open('output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Assuming your JSON objects always contain these fields
            writer.writerow([data['timestamp'], data['ultrasonicHead'], data['ultrasonicMid'], 
                 data['latitude'], data['longitude'], data['gyroX'], data['gyroY'], data['gyroZ'], 
                 data['irFront'], data['irBack'], data['isHeadObstacle'], data['isMidObstacle'], data['isStaircase']])

    except json.JSONDecodeError:
        print("Received invalid JSON data, ignoring.")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### WebSocket Closed ###")

def on_open(ws):
    def run(*args):
        # Here you can send a message to WebSocket server if necessary
        # ws.send('{"event": "subscribe", "channel": "myChannel"}')
        pass
    thread.start_new_thread(run, ())

# WebSocket connect
if __name__ == "__main__":
    websocket.enableTrace(True)
    # Replace the following URL with your actual WebSocket URL
    ws_url = "wss://demo-g54s.onrender.com/device?id=1199&secret=213123"
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Prepare the CSV file for writing
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV Header
        writer.writerow(['Timestamp', 'UltrasonicHead', 'UltrasonicMid', 
                         'Latitude', 'Longitude', 'GyroX', 'GyroY', 'GyroZ', 
                         'IRFront', 'IRBack', 'IsHeadObstacle', 'IsMidObstacle', 'IsStaircase'])

    # Run forever
    ws.run_forever()

