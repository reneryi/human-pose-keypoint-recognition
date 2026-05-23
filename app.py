"""人体关键点识别软件 Streamlit 主程序。"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from pose_image import estimate_pose_in_image


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


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🧍", layout="wide")
    st.title(APP_TITLE)
    st.caption("课程实验项目：基于 Git 与 GitHub 的人体关键点识别软件版本管理实验")
    render_image_page()


if __name__ == "__main__":
    main()
