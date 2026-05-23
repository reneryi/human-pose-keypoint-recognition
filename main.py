"""图片人体关键点识别命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.image_pose_estimator import build_default_output_path, estimate_image_pose


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="基于 MediaPipe 的图片人体关键点识别程序。"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="输入图片路径，例如 assets/input/person.jpg",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="输出图片路径，未指定时默认保存到 outputs 目录。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else build_default_output_path(input_path)

    try:
        result = estimate_image_pose(input_path, output_path)
    except Exception as exc:  # noqa: BLE001 - 命令行入口需要给出友好错误信息
        print(f"[错误] {exc}", file=sys.stderr)
        return 1

    print(result.message)
    print(f"输入图片：{result.input_path}")
    print(f"输出图片：{result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
