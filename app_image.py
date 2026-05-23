"""本地图片选择版人体关键点识别入口。"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from src.image_pose_estimator import build_default_output_path, estimate_image_pose


def select_and_process_image() -> None:
    """弹出文件选择框，选择图片并进行人体关键点识别。"""
    root = tk.Tk()
    root.withdraw()

    input_path = filedialog.askopenfilename(
        title="请选择需要识别的人体图片",
        filetypes=[
            ("图片文件", "*.jpg *.jpeg *.png *.bmp"),
            ("所有文件", "*.*"),
        ],
    )

    if not input_path:
        messagebox.showinfo("提示", "未选择图片，程序已退出。")
        return

    output_path = build_default_output_path(Path(input_path))

    try:
        result = estimate_image_pose(input_path, output_path)
    except Exception as exc:  # noqa: BLE001 - 图形入口需要弹窗展示错误
        messagebox.showerror("识别失败", str(exc))
        return

    messagebox.showinfo(
        "识别完成",
        f"{result.message}\n\n结果图片已保存到：\n{result.output_path}",
    )


if __name__ == "__main__":
    select_and_process_image()
