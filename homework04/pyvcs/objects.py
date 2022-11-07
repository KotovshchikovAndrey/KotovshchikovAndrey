import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def _write_hash_in_repo(hash: str, store: str) -> None:
    hash_title, hash_content = hash[:2], hash[2:]

    gitdir = repo_find()
    hash_path = gitdir / "objects" / hash_title
    hash_path.mkdir(exist_ok=True, parents=True)
    with open(hash_path / hash_content, 'wb') as hash_file:
        hash_file.write(zlib.compress(store.encode()))


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    decoded_data = data.decode(encoding="UTF-8")
    store = f"{fmt} {len(decoded_data)}\0" + decoded_data
    hash = hashlib.sha1(store.encode()).hexdigest()
    if write:
        _write_hash_in_repo(hash, store)

    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
