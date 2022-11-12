import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object

# Формат для упаковки файлов
PACK_FORMAT = ">2i8i20sh{name_length}s3x"

# Формат для распаковки файлов
UNPACK_FORMAT = ">2i8i20sh{name_length}s"

# Размер всех атрибутов за исключением name известен, и в сумме составляет 62 байта
DEFINITE_PACK_SIZE = 62

# Байты в начале и конце файла index
INDEX_START_BYTES, INDEX_END_BYTES = (
    b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03",
    b"k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
)


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        attr_dict = self._asdict()
        attr_dict['name'] = self.name.encode('utf-8')
        return struct.pack(
            PACK_FORMAT.format(name_length=len(self.name)), *list(attr_dict.values()))

    @classmethod
    def unpack(cls, data: bytes) -> "GitIndexEntry":
        name_size = len(data) - DEFINITE_PACK_SIZE
        unpack_data = struct.unpack(
            UNPACK_FORMAT.format(name_length=name_size), data)

        name_value: str = unpack_data[-1].decode().rstrip("\x00")
        return cls(*unpack_data[:-1], name=name_value)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index_path = gitdir / "index"
    if not index_path.exists():
        return []

    index_data = index_path.read_bytes()
    read_start, read_end = (
        len(INDEX_START_BYTES) + 1,
        len(index_data) - len(INDEX_END_BYTES)
    )
    pack_files_list = index_data[read_start:read_end].split(b"\x00\x00\x00^")

    return [GitIndexEntry.unpack(b"^" + pack_data) for pack_data in pack_files_list]


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index_data_for_write = INDEX_START_BYTES
    for index_entry in entries:
        index_data_for_write += index_entry.pack()

    index_path = gitdir / 'index'
    index_path.write_bytes(
        index_data_for_write + INDEX_END_BYTES)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    git_index_entry_list = []

    for file in paths:
        if not file.exists():
            continue

        file_hash = hash_object(
            data=file.read_bytes(), fmt="blob", write=True)

        stat_info = os.stat(file)
        git_index_entry = GitIndexEntry(
            ctime_s=int(stat_info.st_ctime),
            ctime_n=0,
            mtime_s=int(stat_info.st_mtime),
            mtime_n=0,
            dev=stat_info.st_dev,
            ino=stat_info.st_ino,
            mode=stat_info.st_mode,
            uid=stat_info.st_uid,
            gid=stat_info.st_gid,
            size=stat_info.st_size,
            sha1=file_hash.encode(),
            flags=7,
            name=file.name
        )

        git_index_entry_list.append(git_index_entry)

    write_index(gitdir, entries=git_index_entry_list)
