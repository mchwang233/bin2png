#!/usr/bin/env python3

import argparse
import math
from pathlib import Path
from typing import Tuple

from PIL import Image


PIXEL_FORMATS = {
    # format: (PIL mode, raw mode, bytes per pixel)
    # On Little Endian systems (like x86/ARM memory dumps):
    # xrgb8888 (0xXXRRGGBB) is stored as BB GG RR XX -> PIL mode matches: BGRX
    "xrgb8888": ("RGB", "BGRX", 4),
    # bgrx8888 (0xBBGGRRXX) is stored as XX RR GG BB -> PIL mode matches: XRGB
    "bgrx8888": ("RGB", "XRGB", 4),
    "argb8888": ("RGBA", "BGRA", 4),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a binary file into a PNG image.")
    parser.add_argument("--bin", required=True, help="Path to the input .bin file")
    parser.add_argument(
        "--format",
        required=True,
        choices=PIXEL_FORMATS.keys(),
        help="Pixel format of the input data (xrgb8888, bgrx8888, argb8888)",
    )
    parser.add_argument(
        "--out",
        help="Output PNG path (defaults to input filename with .png extension)",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Directory to save output files.",
    )
    parser.add_argument(
        "--cpress",
        action="store_true",
        help="Treat input as tiled data (16x4 pixel blocks) and arrange them into the final image.",
    )
    return parser.parse_args()


def compute_dimensions(pixel_count: int, align_w: int = 1, align_h: int = 1) -> Tuple[int, int]:
    if pixel_count <= 0:
        raise ValueError("Input does not contain any pixel data.")
    
    # Target a roughly square aspect ratio
    side = math.sqrt(pixel_count)
    # Width should be a multiple of align_w
    width = math.ceil(side / align_w) * align_w
    if width == 0:
        width = align_w
        
    # Height is derived from width to contain all pixels, aligned to align_h
    height = math.ceil(pixel_count / width)
    height = math.ceil(height / align_h) * align_h
    
    return width, height


def main() -> None:
    args = parse_args()
    input_path = Path(args.bin)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if args.dir:
        args.dir.mkdir(parents=True, exist_ok=True)

    mode, raw_mode, bytes_per_pixel = PIXEL_FORMATS[args.format]
    raw = input_path.read_bytes()
    pixel_count = len(raw) // bytes_per_pixel

    block_w, block_h = (16, 4) if args.cpress else (1, 1)
    width, height = compute_dimensions(pixel_count, block_w, block_h)

    expected_size = width * height * bytes_per_pixel
    if len(raw) < expected_size:
        raw += b"\x00" * (expected_size - len(raw))
    elif len(raw) > expected_size:
        raw = raw[:expected_size]

    if args.cpress:
        image = Image.new(mode, (width, height))
        bytes_per_block = block_w * block_h * bytes_per_pixel
        blocks_per_row = width // block_w
        
        # Iterate over raw bytes in chunks of bytes_per_block
        for i in range(0, len(raw), bytes_per_block):
            chunk = raw[i : i + bytes_per_block]
            # Although raw should be padded, ensuring chunk size for safety
            if len(chunk) < bytes_per_block:
                chunk += b"\x00" * (bytes_per_block - len(chunk))
            
            block_index = i // bytes_per_block
            bx = (block_index % blocks_per_row) * block_w
            by = (block_index // blocks_per_row) * block_h
            
            # Stop if we exceed image bounds (should not happen if math is correct)
            if by >= height:
                break
                
            tile = Image.frombytes(mode, (block_w, block_h), chunk, "raw", raw_mode)
            image.paste(tile, (bx, by))

        ex_bin_filename = f"{input_path.stem}_ex.bin"
        ex_bin_path = (args.dir / ex_bin_filename) if args.dir else input_path.with_name(ex_bin_filename)
        ex_bin_path.write_bytes(image.tobytes("raw", raw_mode))
        print(f"Saved Extended Bin: {ex_bin_path}")
    else:
        image = Image.frombytes(mode, (width, height), raw, "raw", raw_mode)

    if args.out:
        output_path = Path(args.out)
    else:
        output_filename = input_path.with_suffix(".png").name
        output_path = (args.dir / output_filename) if args.dir else input_path.with_suffix(".png")

    image.save(output_path)
    print(f"Saved PNG: {output_path}")


if __name__ == "__main__":
    main()
