"""视频人体关键点识别模块。

该模块负责逐帧读取视频、调用 MediaPipe Pose 识别人体关键点，并输出绘制骨架后的结果视频。
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

ProgressCallback = Callable[[int, int], None]


@dataclass
class VideoPoseResult:
    """视频识别结果。"""

    output_path: Path
    output_size_bytes: int
    total_frames: int
    processed_frames: int
    pose_frames: int
    fps: float
    width: int
    height: int


def _build_output_path(output_dir: str | Path, filename_prefix: str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{filename_prefix}_{int(time.time())}.mp4"


def _validate_video_properties(width: int, height: int, fps: float) -> None:
    """校验视频导出所需的基础属性。"""

    if width <= 0 or height <= 0:
        raise RuntimeError("无法获取有效的视频宽高，不能导出结果视频。")
    if fps <= 0:
        raise RuntimeError("无法获取有效的视频帧率，不能导出结果视频。")


def process_video_pose(
    input_path: str | Path,
    output_dir: str | Path = "outputs/video_result",
    filename_prefix: str = "video_pose_result",
    progress_callback: ProgressCallback | None = None,
    max_frames: int | None = None,
) -> VideoPoseResult:
    """逐帧识别视频中的人体关键点并保存结果视频。

    Args:
        input_path: 输入视频路径。
        output_dir: 输出目录。
        filename_prefix: 输出视频文件名前缀。
        progress_callback: 进度回调函数，参数为已处理帧数和总帧数。
        max_frames: 最多处理的帧数，主要用于快速测试。

    Returns:
        VideoPoseResult: 视频处理统计信息。
    """

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"输入视频不存在：{input_path}")

    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频文件：{input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    _validate_video_properties(width, height, fps)

    if max_frames is not None and max_frames > 0:
        total_frames = min(total_frames, max_frames) if total_frames > 0 else max_frames

    output_path = _build_output_path(output_dir, filename_prefix)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError(f"无法创建输出视频：{output_path}")

    processed_frames = 0
    pose_frames = 0

    try:
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as pose:
            while True:
                if max_frames is not None and processed_frames >= max_frames:
                    break

                success, frame = cap.read()
                if not success:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    pose_frames += 1
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                    )

                writer.write(frame)
                processed_frames += 1

                if progress_callback is not None:
                    progress_callback(processed_frames, total_frames)
    finally:
        cap.release()
        writer.release()

    if processed_frames == 0:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("没有成功处理任何视频帧，未生成结果视频。")

    output_size_bytes = output_path.stat().st_size if output_path.exists() else 0
    if output_size_bytes <= 0:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("结果视频导出失败，输出文件为空。")

    return VideoPoseResult(
        output_path=output_path,
        output_size_bytes=output_size_bytes,
        total_frames=total_frames,
        processed_frames=processed_frames,
        pose_frames=pose_frames,
        fps=fps,
        width=width,
        height=height,
    )


def main() -> None:
    """命令行测试入口。"""

    parser = argparse.ArgumentParser(description="视频人体关键点识别")
    parser.add_argument("video", help="输入视频路径")
    parser.add_argument("--output-dir", default="outputs/video_result", help="输出目录")
    parser.add_argument("--max-frames", type=int, default=None, help="最多处理帧数，用于快速测试")
    args = parser.parse_args()

    result = process_video_pose(
        args.video,
        output_dir=args.output_dir,
        max_frames=args.max_frames,
        progress_callback=lambda done, total: print(f"已处理 {done}/{total} 帧", end="\r"),
    )
    print()
    print(f"结果视频：{result.output_path}")
    print(f"输出大小：{result.output_size_bytes} 字节")
    print(f"处理帧数：{result.processed_frames}")
    print(f"检测到人体的帧数：{result.pose_frames}")
    print(f"视频尺寸：{result.width}x{result.height}，FPS：{result.fps:.2f}")


if __name__ == "__main__":
    main()
