import sys
import json
import struct
import urllib

def recevice():
    byteArray = sys.stdin.buffer.read(4)
    if len(byteArray) != 4:
        sys.exit(0)
    return json.loads(sys.stdin.buffer.read(struct.unpack('@I',byteArray)[0]).decode('utf8'))

def send(msg):
    jsonBuf = json.dumps(msg).encode('utf8')
    sys.stdout.buffer.write(struct.pack('@I', len(jsonBuf)))
    sys.stdout.buffer.write(jsonBuf)
    sys.stdout.buffer.flush()

