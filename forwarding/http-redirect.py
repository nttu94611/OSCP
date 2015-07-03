
# Author: Oleg Mitrofanov (reider-roque) 2015

import sys, SimpleHTTPServer, SocketServer

if len(sys.argv) != 3:
    print("""Usage: python {0} PORT REDIR_ADDR
Example: python {0} 80 http://example.com/\n""".format(__file__))
    sys.exit(1)

port = int(sys.argv[1])
redir_addr = sys.argv[2]

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', redir_addr)
        self.end_headers()

handler = SocketServer.TCPServer(("", port), myHandler)
print("Serving HTTP on 0.0.0.0 port {0} ...".format(port))
handler.serve_forever()
