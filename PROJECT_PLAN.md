# 项目实施计划

本文件用于跟踪《基于 Git 与 GitHub 的人体关键点识别软件版本管理实验》的实施进度。  
说明：`✔` 表示已完成，`□` 表示待完成。

## 一、前期确认

- ✔ 确认使用 GitHub 替代 Gitee。
- ✔ 确认使用原远程仓库地址：`https://github.com/reneryi/human-pose-keypoint-recognition`。
- ✔ 确认旧仓库文件无参考价值，采用“保留仓库、清空旧文件、重新建设项目”的方式。
- ✔ 确认使用 Streamlit 作为本地 Web 界面。
- ✔ 确认 Python 解释器环境为 conda 环境 `jc_env`。

## 二、基础 Git 与版本管理任务

- ✔ 检查 Git 是否可用。
- ✔ 检查 conda 环境 `jc_env` 是否可用。
- ✔ 关联原 GitHub 远程仓库。
- ✔ 切换并建立本地 `master` 分支。
- ✔ 清空旧项目跟踪文件并形成独立提交。
- □ 完成任务一：版本管理与 Git 基础认知说明。
- □ 完成任务二：本地仓库建立、文件增删改查、`diff`、`log` 和多次提交记录。

## 三、v1.0.0 图片人体关键点识别

- □ 创建基础项目结构。
- □ 编写项目依赖文件 `requirements.txt`。
- □ 编写图片关键点识别模块。
- □ 编写 Streamlit 图片上传与结果展示界面。
- □ 实现结果图片保存功能。
- □ 测试图片识别功能。
- □ 在 `master` 分支发布 `v1.0.0` 标签。

## 四、v1.0.1 视频人体关键点识别

- □ 从 `master` 创建 `feature/video-pose` 分支。
- □ 编写视频逐帧关键点识别模块。
- □ 编写 Streamlit 视频上传与处理界面。
- □ 实现结果视频导出功能。
- □ 测试视频识别功能。
- □ 将 `feature/video-pose` 合并回 `master`。
- □ 在 `master` 分支发布 `v1.0.1` 标签。

## 五、远程仓库与交付材料

- □ 推送 `master` 分支到 GitHub。
- □ 推送 `feature/video-pose` 分支到 GitHub。
- □ 推送 `v1.0.0` 与 `v1.0.1` 标签到 GitHub。
- □ 整理 `README.md`。
- □ 整理 `docs/实验报告.md`。
- □ 整理 `docs/Git操作记录.md`。
- □ 整理 `docs/运行说明.md`。
- □ 准备结果截图或截图说明。
