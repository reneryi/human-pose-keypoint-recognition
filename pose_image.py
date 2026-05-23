"""图片人体关键点识别模块。

该模块封装 MediaPipe Pose 的图片识别逻辑，供 Streamlit 页面和命令行测试复用。
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


@dataclass
class ImagePoseResult:
    """图片识别结果。"""

    annotated_image: np.ndarray
    output_path: Path
    has_pose: bool
    keypoint_count: int


def _save_image_with_unicode_path(image_bgr: np.ndarray, output_path: Path) -> None:
    """保存图片，兼容 Windows 中文路径。"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix if output_path.suffix else ".jpg"
    ok, buffer = cv2.imencode(suffix, image_bgr)
    if not ok:
        raise RuntimeError(f"图片编码失败，无法保存到：{output_path}")
    buffer.tofile(str(output_path))


def estimate_pose_in_image(
    image_bgr: np.ndarray,
    output_dir: str | Path = "outputs/image_result",
    filename_prefix: str = "image_pose_result",
) -> ImagePoseResult:
    """识别单张图片中的人体关键点并保存绘制结果。

    Args:
        image_bgr: OpenCV BGR 格式图片。
        output_dir: 结果图片保存目录。
        filename_prefix: 输出文件名前缀。

    Returns:
        ImagePoseResult: 包含绘制后图片、保存路径和关键点数量。
    """

    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("输入图片为空，无法进行人体关键点识别。")

    annotated_image = image_bgr.copy()
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
    ) as pose:
        results = pose.process(image_rgb)

    has_pose = results.pose_landmarks is not None
    keypoint_count = 0

    if has_pose:
        keypoint_count = len(results.pose_landmarks.landmark)
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        )

    output_dir = Path(output_dir)
    output_path = output_dir / f"{filename_prefix}_{int(time.time())}.jpg"
    _save_image_with_unicode_path(annotated_image, output_path)

    return ImagePoseResult(
        annotated_image=annotated_image,
        output_path=output_path,
        has_pose=has_pose,
        keypoint_count=keypoint_count,
    )


def read_image(image_path: str | Path) -> np.ndarray:
    """读取图片，兼容中文路径。"""

    image_path = Path(image_path)
    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"无法读取图片：{image_path}")
    return image


def main() -> None:
    """命令行测试入口。"""

    parser = argparse.ArgumentParser(description="图片人体关键点识别")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--output-dir", default="outputs/image_result", help="输出目录")
    args = parser.parse_args()

    image = read_image(args.image)
    result = estimate_pose_in_image(image, output_dir=args.output_dir)
    print(f"是否检测到人体：{result.has_pose}")
    print(f"关键点数量：{result.keypoint_count}")
    print(f"结果图片：{result.output_path}")


if __name__ == "__main__":
    main()
