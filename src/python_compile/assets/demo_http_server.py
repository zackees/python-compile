# pylint: disable=invalid-name

import os
import socket
from http.server import test  # type: ignore
from http.server import (
    CGIHTTPRequestHandler,
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer,
)

if __name__ == "__main__":
    import argparse
    import contextlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--cgi", action="store_true", help="run as CGI server")
    parser.add_argument(
        "--bind",
        "-b",
        metavar="ADDRESS",
        help="specify alternate bind address " "(default: all interfaces)",
    )
    parser.add_argument(
        "--directory",
        "-d",
        default=os.getcwd(),
        help="specify alternate directory " "(default: current directory)",
    )
    parser.add_argument(
        "port",
        action="store",
        default=8000,
        type=int,
        nargs="?",
        help="specify alternate port (default: 8000)",
    )
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler  # type: ignore
    else:
        handler_class = SimpleHTTPRequestHandler  # type: ignore

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):

        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(
                request, client_address, self, directory=args.directory
            )

    test(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
