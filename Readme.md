# imcheck - check you imports

A small package to warn if a module is defined in multiple locations inspired by
[this twitter thread][thread].

Usage:

```bash
pip install .
python -c "import imcheck; imcheck.install_path_file()"
```

To uninstall the hook:

```bash
python -c "import imcheck; imcheck.uninstall_path_file()"
```

## How does it work

1. `imcheck.install_path_file` creates a `.pth` file in your `site-packages`
   directory that installs an import hook every time Python is started
2. The import hook does not modify the import mechanism, but checks for any
   module not imported before, whether it is found in multiple locations

Limitations: Due to the flexibility of Pythons import system is is really hard
to cover all possible locations where a module could be found. In principle, it
is for example possible to dynamically generate modules at runtime without ever
writing it to disk. This implementation only checks file based modules that are
found in `sys.path`. 

[thread]: https://twitter.com/francoisfleuret/status/1454378864608780290
