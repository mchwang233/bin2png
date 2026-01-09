#!/usr/bin/env python3

import argparse
import math
from pathlib import Path

from PIL import Image


PIXEL_FORMATS = {
    "rgb888": ("RGB", 3),
    "rgb8888": ("RGBA", 4),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a binary file into a PNG image.")
    parser.add_argument("--bin", required=True, help="Path to the input .bin file")
    parser.add_argument(
        "--format",
        required=True,
        choices=PIXEL_FORMATS.keys(),
        help="Pixel format of the input data (rgb888 or rgb8888)",
    )
    parser.add_argument(
        "--out",
        help="Output PNG path (defaults to input filename with .png extension)",
    )
    return parser.parse_args()


def compute_dimensions(pixel_count: int) -> tuple[int, int]:
    if pixel_count <= 0:
        raise ValueError("Input does not contain any pixel data.")
    width = math.ceil(math.sqrt(pixel_count))
    height = math.ceil(pixel_count / width)
    return width, height


def main() -> None:
    args = parse_args()
    input_path = Path(args.bin)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    mode, bytes_per_pixel = PIXEL_FORMATS[args.format]
    raw = input_path.read_bytes()
    pixel_count = len(raw) // bytes_per_pixel
    width, height = compute_dimensions(pixel_count)

    expected_size = width * height * bytes_per_pixel
    if len(raw) < expected_size:
        raw += b"\x00" * (expected_size - len(raw))
    elif len(raw) > expected_size:
        raw = raw[:expected_size]

    image = Image.frombytes(mode, (width, height), raw)

    output_path = Path(args.out) if args.out else input_path.with_suffix(".png")
    image.save(output_path)
    print(f"Saved PNG: {output_path}")


if __name__ == "__main__":
    main()
