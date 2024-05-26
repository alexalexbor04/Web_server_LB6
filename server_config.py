DIR = 'in_html'
BUFFER_SIZE = 8192
DEF = 'index.html'
ALLOWED_TYPES = ('html',
                 'css',
                 'js',
                 'png', 
                 'jpg', 
                 'mp4')
CODES = {200: 'OK',
         403: 'Forbidden',
         404: 'Not found'}
TYPES = {'html': 'text/html',
         'css': 'text/css',
         'js': 'text/js',
         'png': 'image/png',
         'jpg': 'image/jpg', 
         'mp4': 'video/mp4'}
PAT = '''HTTP/1.1 {} {}
Date: {}
Server: SelfMadeServer v0.0.1
Content-Type: {}
Content-Length: {}
Connection: keep-alive

'''

