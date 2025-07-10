import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleJSONHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/device-1":
            payload = {
                "Voltage L1-L2": round(random.uniform(215.0, 230.0), 3),
                "Device-Name": "Json-over-http Simulator 1",
                "Working": True,
                "Temperature": round(random.uniform(15.0, 25.0), 3),
                "Currents": {
                    "L1": round(random.randint(3, 8), 3),
                    "L2": round(random.randint(3, 8), 3),
                    "L3": round(random.randint(3, 8), 3),
                },
                "Active Alarms": [],
            }
            self.respond_with_json(payload)
        elif self.path == "/device-2":
            payload = {
                "Voltage L1-L2": round(random.uniform(400.0, 430.0), 3),
                "Device-Name": "Json-over-http Simulator 2",
                "Working": False,
                "Temperature": round(random.uniform(15.0, 25.0), 3),
                "Active Alarms": ["Overvoltage", "Device not running"],
            }
            self.respond_with_json(payload)
        else:
            self.send_error(404, "Path not found")

    def do_POST(self):
        if self.path == "/device-3":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            try:
                requested_info = json.loads(post_data.decode("utf8").replace("'", '"'))
                requested_info = requested_info[0]
            except Exception:
                self.send_error(400, "Invalid JSON")
                return
            print(requested_info)
            payload = {
                "Voltage L1-L2": round(random.uniform(400.0, 430.0), 3),
                "Device-Name": "Json-over-http Simulator 3 (POST)",
                "Working": False,
                "Temperature": round(random.uniform(15.0, 25.0), 3),
                "Active Alarms": ["Overvoltage", "Device not running"],
            }
            self.respond_with_json(
                payload.get(requested_info, f"{requested_info} not found")
            )
        else:
            self.send_error(404, "Path not found")

    def respond_with_json(self, data):
        response = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleJSONHandler)
    print("Server running on http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing Server")
        httpd.server_close()
