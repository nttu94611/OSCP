
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
print("Redirecting HTTP requests from 0.0.0.0:{0} to {1} ...".format(port, redir_addr))
handler.serve_forever()
