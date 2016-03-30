import argparse

import webhttp.server

content_dir = 'content'

# Create and start the HTTP Server
# Use `python webserver.py --help` to display command line options
if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="HTTP Server")
    parser.add_argument("-a", "--address", type=str, default='localhost')
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument("-t", "--timeout", type=int, default=15)
    args = parser.parse_args()

    # Start server
    server = webhttp.server.Server(args.address, args.port, args.timeout)
    try:
        print('server running')
        server.run()
        print('server not running anymore')
    except KeyboardInterrupt:
        server.shutdown()
        print('Keyboard interruption')
