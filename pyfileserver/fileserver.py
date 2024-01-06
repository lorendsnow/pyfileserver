import os
import socket
from logging import Logger
from pathlib import Path
from socketserver import BaseRequestHandler, TCPServer

import tomllib
from config_logger import make_logger

with open("serverconfig.toml", "rb") as f:
    config = tomllib.load(f)
DATA_PATH = config["DATA_PATH"]
LOG_FILE = config["LOG_FILE"]


class FileHandler(BaseRequestHandler):
    def _parse_header(self) -> tuple[str, int]:
        _SEPARATOR = "<SEPARATOR>"
        sock: socket.SocketType = self.request
        logger: Logger = self.server.logger

        try:
            header = sock.recv(1024).decode("utf-8")
            logger.debug(f"Received header: {header}")

            filesize, filename = header.split(_SEPARATOR)
        except Exception as e:
            logger.error(f"Error while parsing header: {e}")
            return

        return int(filesize), filename

    def handle(self) -> None:
        sock: socket.SocketType = self.request
        logger: Logger = self.server.logger
        logger.debug(f"Connected to {self.client_address}")

        try:
            filesize, filename = self._parse_header()
            file_path = server.save_path.joinpath(filename)

            with open(file_path, "wb") as f:
                received_bytes = 0
                while received_bytes < filesize:
                    chunk = sock.recv(1024)
                    if chunk:
                        f.write(chunk)
                        received_bytes += len(chunk)
        except Exception as e:
            logger.error(f"Error while receiving file: {e}")
            return

        logger.debug(
            f"{filename} successfully received and saved at {file_path.as_posix()}"
        )
        return


class FileServer(TCPServer):
    def __init__(
        self,
        save_path: str | os.PathLike,
        host: str = "0.0.0.0",
        port: int = 5001,
        logger: str = "FileServer",
    ) -> None:
        self.save_path = Path(save_path)
        self.logger = make_logger(logger, LOG_FILE)
        super().__init__((host, port), FileHandler)
        self.logger.debug(f"File server started on {self.server_address}")


if __name__ == "__main__":
    path = Path(DATA_PATH)
    with FileServer(path) as server:
        server.serve_forever()
