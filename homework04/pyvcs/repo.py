import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    current_dir = pathlib.Path(workdir)
    git_dir = os.environ["GIT_DIR"] if os.environ.get(
        "GIT_DIR", None) is not None else ".git"

    if (current_dir / git_dir).exists():
        return pathlib.Path(workdir) / git_dir

    for dir in current_dir.parents:
        if dir.name == git_dir:
            return dir

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    path = pathlib.Path(workdir)
    if not path.is_dir():
        raise Exception(f"{path.name} is not a directory")

    git_dir = os.environ["GIT_DIR"] if os.environ.get(
        "GIT_DIR", None) is not None else ".git"

    (path / git_dir).mkdir(exist_ok=False, parents=True)
    (path / git_dir / "refs" / "heads").mkdir(exist_ok=True, parents=True)
    (path / git_dir / "refs" / "tags").mkdir(exist_ok=True, parents=True)
    (path / git_dir / "objects").mkdir(exist_ok=True, parents=True)

    with (
        open(path / git_dir / "HEAD", 'w') as head,
        open(path / git_dir / "config", 'w') as config,
        open(path / git_dir / "description", 'w') as description
    ):
        head.write(
            "ref: refs/heads/master\n")
        config.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
        description.write(
            "Unnamed pyvcs repository.\n")

    return path / git_dir
