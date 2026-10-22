"""Command-line entry point."""

import argparse

from ikd1d import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ikd1d", description=__doc__)
    parser.add_argument("--version", action="version", version=f"ikd1d {__version__}")
    parser.parse_args(argv)
    return 0
