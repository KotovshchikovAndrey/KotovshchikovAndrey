import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def _write_hash_in_repo(hash: str, store: bytes) -> None:
    hash_title, hash_content = hash[:2], hash[2:]

    gitdir = repo_find()
    hash_path = gitdir / "objects" / hash_title
    hash_path.mkdir(exist_ok=True, parents=True)
    with open(hash_path / hash_content, 'wb') as hash_file:
        hash_file.write(zlib.compress(store))


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    store = f"{fmt} {len(data)}\0".encode() + data
    hash = hashlib.sha1(store).hexdigest()
    if write:
        _write_hash_in_repo(hash, store)

    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not (4 <= len(obj_name) <= 40):
        raise Exception(f"Not a valid object name {obj_name}")

    objects_files_list = []
    objects_dir_path = gitdir / "objects" / obj_name[:2]
    for object_title in objects_dir_path.iterdir():
        try:
            full_object_name = find_object(
                obj_name[2:], objects_dir_path / object_title)
        except Exception:
            continue
        else:
            objects_files_list.append(obj_name[:2] + full_object_name)

    return objects_files_list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    full_object_name = gitdir.parts[-1]
    if obj_name in full_object_name:
        return full_object_name

    raise Exception('Object File Does Not Exists!!!!!!!!!!!!!!!!')


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    readed_data = path.read_bytes()
    object_data = zlib.decompress(readed_data)

    header_end_index = object_data.find(b"\x00")
    hash_title = object_data[:header_end_index]
    blob_end_index = hash_title.find(b" ")
    blob = object_data[:blob_end_index]

    hash_content = object_data[header_end_index + 1:]
    return blob.decode(), hash_content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    print(read_object(obj_name, gitdir)[-1].decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
