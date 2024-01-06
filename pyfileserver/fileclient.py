import os
import socket
from pathlib import Path
from typing import Optional

from tqdm import tqdm


class FileClient:
    """
    Client object to connect to FileServer and send files.

    Params:

    basepath: str or os.Pathlike - Path to the folder where the file is saved on the
    client machine.

    host: str - "localhost" or ip address of FileServer (AF_INET).

    port: int - Port that FileServer is listening on.

    encode_fmt: str - Encoding parameter passed to struct.pack() to encode the filesize.
    """

    def __init__(
        self,
        basepath: str | os.PathLike,
        host: str,
        port: int,
    ) -> None:
        self.basepath = Path(basepath)
        self._address = host, port
        self._sock: Optional[socket.SocketType] = None
        self._SEPARATOR = "<SEPARATOR>"

    def _parse_file_info(self, filename: str) -> tuple[Path, str]:
        path = self.basepath.absolute().joinpath(filename)
        filesize = str(os.path.getsize(path))

        return path, filesize

    def send_file(self, filename: str) -> None:
        if not isinstance(self._sock, socket.SocketType):
            raise ConnectionError("No connection to the server has been made.")

        path, filesize = self._parse_file_info(filename)
        header = filesize + self._SEPARATOR + filename

        self._sock.sendall(header.encode("utf-8"))

        progress = tqdm(
            range(int(filesize)),
            f"Sending {filename}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        with open(path, "rb") as f:
            while read_bytes := f.read(1024):
                self._sock.sendall(read_bytes)
                progress.update(len(read_bytes))

        print(f"{filename} sent successfully.")

        return

    def connect(self) -> None:
        try:
            self._sock = socket.create_connection(self._address)
            print(f"Connected to {self._sock.getsockname()}")
        except Exception as e:
            print(f"Couldn't connect to server - got exception {e}")
        finally:
            return

    def disconnect(self) -> None:
        if not isinstance(self._sock, socket.SocketType):
            print("No connection to the server has been made.")
        else:
            return self._sock.close()

    @property
    def address(self) -> tuple[str, int]:
        return self._address

    @property
    def sock(self) -> Optional[socket.SocketType]:
        return self._sock

    def __repr__(self) -> str:
        return "FileClient object"
