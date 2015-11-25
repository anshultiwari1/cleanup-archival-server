
import jsonrpclib
import sys
import os
from datetime import datetime
s = jsonrpclib.Server("http://172.16.15.221:8000/jsonrpc")


def main(argv=None):
	print "Start"
	print "End"

if __name__ == "__main__":
    sys.exit(main())
