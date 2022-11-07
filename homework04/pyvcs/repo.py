import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    current_dir = pathlib.Path(workdir)
    if (current_dir / os.environ["GIT_DIR"]).exists():
        return pathlib.Path(workdir) / os.environ["GIT_DIR"]

    for dir in current_dir.parents:
        print(dir, dir.name)
        if dir.name == os.environ["GIT_DIR"]:
            return dir

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if not workdir.is_dir():
        raise Exception(f"{workdir.name} is not a directory")

    git_dir = os.environ["GIT_DIR"]
    path = pathlib.Path(workdir)
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

    return workdir / git_dir
