#!/usr/bin/env python3
"""Download a Project Gutenberg plain-text book into data/raw/."""

from __future__ import annotations

import argparse
import pathlib
import urllib.error
import urllib.request


GUTENBERG_URLS = (
    "https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
    "https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
    "https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
)


def download_text(book_id: int, output_dir: pathlib.Path) -> pathlib.Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    last_error: Exception | None = None
    for template in GUTENBERG_URLS:
        url = template.format(book_id=book_id)
        try:
            with urllib.request.urlopen(url) as response:
                if response.status != 200:
                    continue
                content = response.read()
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            last_error = exc
            continue

        output_path = output_dir / f"pg{book_id}.txt"
        output_path.write_bytes(content)
        return output_path

    raise RuntimeError(
        f"Could not download Gutenberg text for book_id={book_id}."
    ) from last_error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book_id", type=int, help="Project Gutenberg numeric book ID")
    parser.add_argument(
        "--output-dir",
        default="data/raw",
        help="Directory where the downloaded text file is saved",
    )
    args = parser.parse_args()

    output_path = download_text(args.book_id, pathlib.Path(args.output_dir))
    print(f"Downloaded: {output_path}")


if __name__ == "__main__":
    main()
