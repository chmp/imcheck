import pathlib
import sys


class Hook:
    def find_spec(self, fullname, path, target=None):
        # ignore non-top level packages
        if path is not None:
            return

        check_import(fullname)

        return None


def install_hook():
    if any(isinstance(hook, Hook) for hook in sys.meta_path):
        return

    sys.meta_path.insert(0, Hook())


def install_path_file(*, overwrite=False):
    path_file = get_path_file()
    if path_file.exists() and not overwrite:
        raise RuntimeError(
            f"imcheck already installed at {path_file}, "
            "pass overwrite=True to re-install"
        )

    with path_file.open("wt") as fobj:
        fobj.write("import imcheck; imcheck.install_hook()")


def uninstall_path_file():
    path_file = get_path_file()
    if path_file.exists():
        path_file.unlink()


def get_path_file():
    for root in sys.path:
        root = pathlib.Path(root)
        if not root.is_dir() and root.name == "site-packages":
            continue

        return root / "imcheck.pth"

    raise RuntimeError("Could not find the site-packages folder")


def check_import(name):
    locations = []

    for root in sys.path:
        root = pathlib.Path(root)
        if not root.is_dir():
            continue

        if (root / f"{name}.py").exists() or (root / name / "__init__.py").exists():
            locations.append(root)

    if len(locations) > 1:
        print(
            f"Multiple locations for module {name}: {[str(loc) for loc in locations]}"
        )
