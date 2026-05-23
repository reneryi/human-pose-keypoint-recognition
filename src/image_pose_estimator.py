"""图片人体关键点识别核心模块。

本模块使用 MediaPipe Pose 对单张图片进行人体关键点检测，并使用 OpenCV
将关键点和骨架连线绘制到结果图中。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import mediapipe as mp


@dataclass
class PoseEstimationResult:
    """图片人体关键点识别结果。"""

    input_path: Path
    output_path: Path
    success: bool
    pose_detected: bool
    landmark_count: int
    message: str


class ImagePoseEstimator:
    """基于 MediaPipe Pose 的图片人体关键点识别器。"""

    def __init__(
        self,
        static_image_mode: bool = True,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
    ) -> None:
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self._mp_pose = mp.solutions.pose
        self._mp_drawing = mp.solutions.drawing_utils
        self._drawing_spec_point = self._mp_drawing.DrawingSpec(
            color=(0, 255, 0), thickness=3, circle_radius=3
        )
        self._drawing_spec_line = self._mp_drawing.DrawingSpec(
            color=(255, 0, 0), thickness=2, circle_radius=2
        )

    def estimate(self, input_path: str | Path, output_path: str | Path) -> PoseEstimationResult:
        """识别单张图片中的人体关键点并保存结果图。

        Args:
            input_path: 输入图片路径。
            output_path: 输出图片路径。

        Returns:
            PoseEstimationResult: 识别结果对象。
        """
        input_file = Path(input_path)
        output_file = Path(output_path)

        if not input_file.exists():
            raise FileNotFoundError(f"输入图片不存在：{input_file}")

        image_bgr = cv2.imread(str(input_file))
        if image_bgr is None:
            raise ValueError(f"无法读取图片，请检查文件格式：{input_file}")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        with self._mp_pose.Pose(
            static_image_mode=self.static_image_mode,
            model_complexity=self.model_complexity,
            enable_segmentation=False,
            min_detection_confidence=self.min_detection_confidence,
        ) as pose:
            results = pose.process(image_rgb)

        pose_detected = results.pose_landmarks is not None
        landmark_count = 0

        if pose_detected:
            landmark_count = len(results.pose_landmarks.landmark)
            self._mp_drawing.draw_landmarks(
                image_bgr,
                results.pose_landmarks,
                self._mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self._drawing_spec_point,
                connection_drawing_spec=self._drawing_spec_line,
            )
            message = f"识别成功，检测到 {landmark_count} 个人体关键点。"
        else:
            message = "未检测到人体姿态，已保存原图作为结果图。"

        saved = cv2.imwrite(str(output_file), image_bgr)
        if not saved:
            raise IOError(f"结果图片保存失败：{output_file}")

        return PoseEstimationResult(
            input_path=input_file,
            output_path=output_file,
            success=True,
            pose_detected=pose_detected,
            landmark_count=landmark_count,
            message=message,
        )


def build_default_output_path(input_path: str | Path, output_dir: str | Path = "outputs") -> Path:
    """根据输入图片路径生成默认输出路径。"""
    input_file = Path(input_path)
    suffix = input_file.suffix or ".jpg"
    return Path(output_dir) / f"{input_file.stem}_pose_result{suffix}"


def estimate_image_pose(
    input_path: str | Path,
    output_path: Optional[str | Path] = None,
) -> PoseEstimationResult:
    """便捷函数：识别图片人体关键点并保存结果。"""
    final_output_path = Path(output_path) if output_path else build_default_output_path(input_path)
    estimator = ImagePoseEstimator()
    return estimator.estimate(input_path, final_output_path)
