from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse

users = []
messages = []


class ChatHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/users":

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(users).encode()
            )

            return

        elif self.path.startswith("/messages"):

            query = urllib.parse.urlparse(
                self.path
            ).query

            params = urllib.parse.parse_qs(
                query
            )

            current_user = params.get(
                "user",
                [None]
            )[0]

            filtered = []

            for msg in messages:

                # PUBLIC MESSAGE
                if msg["type"] == "public":

                    filtered.append({
                        "type": "public",
                        "from": msg["from"],
                        "text": msg["text"]
                    })

                # PRIVATE MESSAGE
                elif msg["type"] == "private":

                    if current_user in [
                        msg["from"],
                        msg["to"]
                    ]:

                        filtered.append({
                            "type": "private",
                            "from": msg["from"],
                            "to": msg["to"],
                            "text": msg["text"]
                        })

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(filtered).encode()
            )

            return

        else:

            return super().do_GET()

    def do_POST(self):

        if self.path == "/send":

            try:

                length = int(
                    self.headers["Content-Length"]
                )

                body = self.rfile.read(length)

                data = json.loads(body)

                username = data["username"]
                message = data["message"]
                recipient = data["recipient"]

                if username not in users:

                    users.append(username)

                # PUBLIC MESSAGE
                if recipient == "ALL":

                    messages.append({

                        "type": "public",

                        "from": username,

                        "text": message
                    })

                # PRIVATE MESSAGE
                else:

                    messages.append({

                        "type": "private",

                        "from": username,

                        "to": recipient,

                        "text": message
                    })

                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "application/json"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "status": "ok"
                    }).encode()
                )

            except Exception as e:

                print("ERROR:", e)

                self.send_response(500)

                self.end_headers()


PORT = 8000

server = HTTPServer(
    ("0.0.0.0", PORT),
    ChatHandler
)

print(
    f"Chat server running on http://localhost:{PORT}"
)

server.serve_forever()