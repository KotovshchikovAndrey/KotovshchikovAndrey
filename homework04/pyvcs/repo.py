import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    ...


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    path = pathlib.Path(workdir)
    (path / ".git").mkdir(exist_ok=False, parents=True)
    (path / ".git" / "refs" / "heads").mkdir(exist_ok=True, parents=True)
    (path / ".git" / "refs" / "tags").mkdir(exist_ok=True, parents=True)
    (path / ".git" / "objects").mkdir(exist_ok=True, parents=True)

    with (
        open(path / ".git" / "HEAD", 'w') as head,
        open(path / ".git" / "config", 'w') as config,
        open(path / ".git" / "description", 'w') as description
    ):
        head.write(
            "ref: refs/heads/master\n")
        config.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
        description.write(
            "Unnamed pyvcs repository.\n")

    return workdir / ".git"
