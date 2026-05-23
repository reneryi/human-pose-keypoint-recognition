# 人体关键点识别软件版本管理实验

本项目是课程实验项目，主题为“基于 Git 与 GitHub 的人体关键点识别软件版本管理实验”。项目使用 Python、OpenCV、MediaPipe 与 Streamlit 实现图片和视频中的人体关键点识别，并通过 Git 分支、提交和标签展示完整的软件版本管理流程。

## 项目目标

- 使用 Git 完成本地仓库与远程仓库管理。
- 在 `master` 分支完成图片人体关键点识别版本 `v1.0.0`。
- 在 `feature/video-pose` 分支完成视频人体关键点识别功能，并合并发布 `v1.0.1`。
- 输出源码、运行说明、Git 操作记录和实验报告。

## 技术路线

- Python 3.10+
- OpenCV
- MediaPipe Pose
- Streamlit

## 当前版本规划

| 版本 | 功能 | 分支 |
| --- | --- | --- |
| v1.0.0 | 图片人体关键点识别 | master |
| v1.0.1 | 视频人体关键点识别 | feature/video-pose -> master |

## 快速运行

```powershell
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env pip install -r requirements.txt
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env streamlit run app.py
```

详细说明见 `docs/运行说明.md`。
