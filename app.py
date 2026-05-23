"""人体关键点识别软件 Streamlit 主程序。"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import tempfile

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from pose_image import estimate_pose_in_image
from pose_video import process_video_pose


APP_TITLE = "人体关键点识别软件"


def pil_to_bgr(image: Image.Image) -> np.ndarray:
    """将 PIL 图片转换为 OpenCV BGR 格式。"""

    image_rgb = image.convert("RGB")
    return cv2.cvtColor(np.array(image_rgb), cv2.COLOR_RGB2BGR)


def bgr_to_rgb(image_bgr: np.ndarray) -> np.ndarray:
    """将 OpenCV BGR 图片转换为 RGB，供 Streamlit 显示。"""

    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def image_to_download_bytes(image_bgr: np.ndarray) -> bytes:
    """将 BGR 图片编码为 JPEG 字节流。"""

    success, encoded = cv2.imencode(".jpg", image_bgr)
    if not success:
        raise RuntimeError("结果图片编码失败。")
    return encoded.tobytes()


def render_image_page() -> None:
    """渲染 v1.0.0 图片识别页面。"""

    st.header("v1.0.0 图片人体关键点识别")
    st.write("上传一张包含人体的图片，程序会识别主要人体关键点并绘制骨架。")

    uploaded_file = st.file_uploader(
        "请选择图片文件",
        type=["jpg", "jpeg", "png", "bmp"],
        accept_multiple_files=False,
    )

    if uploaded_file is None:
        st.info("请先上传一张图片。")
        return

    original_image = Image.open(BytesIO(uploaded_file.getvalue()))
    image_bgr = pil_to_bgr(original_image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始图片")
        st.image(original_image, use_container_width=True)

    if st.button("开始识别图片关键点", type="primary"):
        with st.spinner("正在识别人体关键点，请稍候……"):
            result = estimate_pose_in_image(image_bgr)

        with col2:
            st.subheader("识别结果")
            st.image(bgr_to_rgb(result.annotated_image), use_container_width=True)

        if result.has_pose:
            st.success(f"识别完成：检测到人体姿态，共绘制 {result.keypoint_count} 个关键点。")
        else:
            st.warning("识别完成，但未检测到清晰人体姿态。请尝试更换包含完整人体的图片。")

        st.write(f"结果图片已保存到：`{Path(result.output_path).as_posix()}`")
        st.download_button(
            "下载结果图片",
            data=image_to_download_bytes(result.annotated_image),
            file_name="image_pose_result.jpg",
            mime="image/jpeg",
        )


def render_video_page() -> None:
    """渲染 v1.0.1 视频识别页面。"""

    st.header("v1.0.1 视频人体关键点识别")
    st.write("上传一个视频文件，程序会逐帧识别人体关键点并输出绘制骨架后的结果视频。")

    uploaded_video = st.file_uploader(
        "请选择视频文件",
        type=["mp4", "avi", "mov", "mkv"],
        accept_multiple_files=False,
    )

    if uploaded_video is None:
        st.info("请先上传一个视频文件。")
        return

    st.subheader("原始视频")
    st.video(uploaded_video)

    if st.button("开始识别视频关键点", type="primary"):
        suffix = Path(uploaded_video.name).suffix or ".mp4"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_video.getvalue())
            temp_input_path = Path(temp_file.name)

        progress_bar = st.progress(0)
        progress_text = st.empty()

        def update_progress(done: int, total: int) -> None:
            total = total if total > 0 else done
            percent = min(done / total, 1.0) if total else 0.0
            progress_bar.progress(percent)
            progress_text.write(f"视频处理中：{done}/{total} 帧")

        try:
            with st.spinner("正在处理视频，请稍候……"):
                result = process_video_pose(temp_input_path, progress_callback=update_progress)
        finally:
            temp_input_path.unlink(missing_ok=True)

        st.success(
            f"视频处理完成：共处理 {result.processed_frames} 帧，"
            f"其中 {result.pose_frames} 帧检测到人体姿态。"
        )
        st.write(f"结果视频已保存到：`{Path(result.output_path).as_posix()}`")
        st.write(f"结果视频大小：`{result.output_size_bytes / 1024 / 1024:.2f} MB`")
        st.subheader("处理后视频")
        st.video(str(result.output_path))

        st.download_button(
            "下载结果视频",
            data=Path(result.output_path).read_bytes(),
            file_name=Path(result.output_path).name,
            mime="video/mp4",
        )


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🧍", layout="wide")
    st.title(APP_TITLE)
    st.caption("课程实验项目：基于 Git 与 GitHub 的人体关键点识别软件版本管理实验")

    page = st.sidebar.radio("请选择功能", ["图片关键点识别", "视频关键点识别"])
    if page == "图片关键点识别":
        render_image_page()
    else:
        render_video_page()


if __name__ == "__main__":
    main()
