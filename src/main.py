"""
FastAPI local server entry point.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

import socket
from app import app
import uvicorn


def find_free_port() -> int:
    """Find a free port on the system by creating a temporary socket."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port


def main():
    port = find_free_port()

    # Print port info in a format that can be easily parsed
    print(f"PORT={port}")

    # Start the server on localhost with disabled logging
    uvicorn.run(
        app,
        host="localhost",
        port=port,
        log_level="critical",  # Most minimal logging
        access_log=False,  # Disable access logs
    )


if __name__ == "__main__":
    main()
