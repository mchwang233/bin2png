# bin2png

一个将二进制（.bin）文件转换为 PNG 图像的工具。

## 功能

- 将二进制文件按像素格式映射为图像
- 支持 `xrgb8888`、`bgrx8888`、`argb8888` 像素格式
- 自动计算接近平方的输出尺寸，并可按块大小对齐
- 可将数据按块（tile）方式重组并导出扩展后的 `.bin`

## 环境依赖

- Python 3.8+
- Pillow

安装依赖：

```
pip install pillow
```

## 使用方式

```
python bin2png.py --bin INPUT.bin --format xrgb8888 [--out OUTPUT.png] [--dir OUTPUT_DIR] [--cpress 16x4]
```

参数说明：

- `--bin`：输入的二进制文件路径（必填）
- `--format`：像素格式，支持 `xrgb8888`、`bgrx8888`、`argb8888`
- `--out`：输出 PNG 路径（可选，默认使用输入文件名并替换为 `.png`）
- `--dir`：输出目录（可选，会创建目录）
- `--cpress`：按块重排输入数据，格式为 `列x行`，如 `16x4`（默认 `16x4`）

示例：

```
python bin2png.py --bin input.bin --format xrgb8888 --out output.png
```

按块重排并输出扩展 bin：

```
python bin2png.py --bin input.bin --format argb8888 --cpress 8x8 --dir out
```

该模式会在输出目录中额外生成 `*_ex.bin`（按图像顺序重排后的原始数据）。

## 输出

- 生成的 PNG 图像文件
- 若启用 `--cpress`，会额外生成扩展后的 bin 文件（`*_ex.bin`）

## 适用场景

- 可视化内存或显存数据
- 快速查看二进制分布特征
- 作为图像处理或机器学习的输入数据

## 许可

如仓库未声明，请默认遵循项目实际代码中的许可说明。

---

# bin2png (English)

A tool that converts binary (`.bin`) data into PNG images.

## Features

- Maps raw binary data into image pixels
- Supports `xrgb8888`, `bgrx8888`, and `argb8888` pixel formats
- Automatically computes near-square image dimensions with optional block alignment
- Optional tiled (block) reordering and export of an extended `.bin`

## Requirements

- Python 3.8+
- Pillow

Install dependencies:

```
pip install pillow
```

## Usage

```
python bin2png.py --bin INPUT.bin --format xrgb8888 [--out OUTPUT.png] [--dir OUTPUT_DIR] [--cpress 16x4]
```

Arguments:

- `--bin`: input binary file path (required)
- `--format`: pixel format (`xrgb8888`, `bgrx8888`, `argb8888`)
- `--out`: output PNG path (optional; defaults to input filename with `.png`)
- `--dir`: output directory (optional; will be created if missing)
- `--cpress`: treat input as tiled data in `COLxROW` (e.g., `16x4`)

Example:

```
python bin2png.py --bin input.bin --format xrgb8888 --out output.png
```

Tiled reordering with extended bin output:

```
python bin2png.py --bin input.bin --format argb8888 --cpress 8x8 --dir out
```

This mode also writes `*_ex.bin`, containing the reordered raw bytes.

## Output

- PNG image file
- If `--cpress` is used, an extra extended bin file (`*_ex.bin`)

## Use cases

- Visualizing memory or GPU buffer dumps
- Inspecting binary distribution patterns
- Feeding binary data into image processing or ML pipelines

## License

If not specified in the repository, follow the license in the codebase.
