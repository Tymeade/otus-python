import SimpleHTTPServer
import mimetypes
import socket
import os
HOST = '127.0.0.1'
PORT = 80
DOCUMENT_ROOT = 'C://Users//Elizaveta//Documents//otus python//homeworks/httptest'


sample_response = \
    """HTTP/1.x 200 OK
Date: Sat, 28 Nov 2009 04:36:25 GMT
Content-Type: {content_type}
Content-Length: {length}

"""

error_response = \
    """HTTP/1.x 405 Method Not Allowed
Allow: GET, HEAD
Date: Sat, 28 Nov 2009 04:36:25 GMT
Content-Type: text/html; charset=UTF-8

'Specified method is invalid for this resource.'"""


class HTTPServer(object):
    def __init__(self, host, port, buffer_size=500):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

    def get_file(self, path):
        if path.endswith('/'):
            path += 'index.html'
        # full_path = os.path.join(DOCUMENT_ROOT, path)
        full_path = DOCUMENT_ROOT + path
        print full_path
        with open(full_path, 'rb') as fp:
            length = os.stat(full_path).st_size
            content = fp.read(length)

        extension = '.' + full_path.split('.')[-1]

        return content, content_types[extension], length

    def handle_request(self, connection):
        # print connection.recv(10000)
        fp = connection.makefile("rb")
        # print fp.readlines()

        version_line = fp.readline()
        if not version_line:
            raise RuntimeError
        request, path, version = version_line.split()
        self.request = request
        self.path = path
        self.version = version
        print request, version
        while True:
            line = fp.readline()
            if not line:
                raise RuntimeError
            line = line.rstrip('\r\n')
            if not line:
                break

    def send_response(self, connection):
        if self.request not in ['GET', 'HEAD']:
            connection.sendall(error_response)
        else:
            content, content_type, length = self.get_file(self.path)
            print len(content)
            print length
            response = sample_response.format(
                content_type=content_type,
                length=length
            )
            connection.sendall(response)
            connection.sendall(content)

    def serve_forever(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)
        while True:
            c, a = s.accept()
            print c, a
            self.handle_request(c)
            self.send_response(c)
            c.close()


if not mimetypes.inited:
    mimetypes.init()
content_types = mimetypes.types_map.copy()

# content_types = {
#     'js',
#     'swf',
#     'html',
#     'css',
#     'jpg',
#     'jpeg',
#     'png',
#     'gif'
# }


if __name__ == '__main__':
    # print content_types
    server = HTTPServer(HOST, PORT)
    server.serve_forever()
