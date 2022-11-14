import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_hash_sum = b""
    for index_entry in index:
        path = str(pathlib.Path(dirname) / index_entry.name).replace('\\', '/')
        split_path = path.split('/')

        tree_content = (
            oct(index_entry.mode)[2:].encode() + b" " +
            f"{split_path[-1]}".encode() + b"\0" +
            index_entry.sha1
        )

        if len(split_path) > 1:
            for subdir in split_path[:-1]:
                tree_hash_sum += b"40000 "
                tree_hash_sum += subdir.encode() + b"\0"

            file_hash = hash_object(
                tree_content,
                fmt='tree',
                write=True
            )

            tree_content = bytes.fromhex(file_hash)

        tree_hash_sum += tree_content

    return hash_object(tree_hash_sum, 'tree', write=True)


def _get_author_time():
    unix_timestamp = int(time.mktime(time.localtime()))
    time_zone = time.timezone
    if time_zone > 0:
        return f"{unix_timestamp} -0{abs(time_zone) // 3600}{(abs(time_zone) // 60) % 60}0"

    return f"{unix_timestamp} +0{abs(time_zone) // 3600}{(abs(time_zone) // 60) % 60}0"


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    commit_content = f"tree {tree}\n"
    if parent is not None:
        commit_content += f"parent {parent}\n"

    author_time = _get_author_time()
    commit_content += "\n".join(
        (
            f"author {author} {author_time}",
            f"committer {author} {author_time}",
            f"\n{message}\n"
        )
    )

    commit_hash = hash_object(commit_content.encode(), "commit", True)
    return commit_hash
