# Git 操作记录

本文档用于记录课程项目开发过程中的关键 Git 操作，后续会补充分支、合并、标签和远程仓库截图说明。

## 任务二已执行的关键命令

```bash
git init -b main
git status
git diff
git add README.md .gitignore
git commit -m "初始化项目说明文档"
git add README.md
git commit -m "补充本地仓库建立说明"
git add LICENSE
git commit -m "添加项目开源许可证"
git log --oneline
```

## 说明

任务二阶段重点体现本地仓库初始化、文件新增、文件修改、差异查看和提交历史查看等基础操作。

## 任务三已执行的关键命令

### 1. 依赖安装与环境检查

```bash
git status
git log --oneline --decorate -5
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env python -c "import sys; print(sys.version)"
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env pip install opencv-python mediapipe
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env python -c "import cv2, mediapipe as mp; print(cv2.__version__); print(mp.__version__)"
```

### 2. 图片人体关键点识别版本开发

任务三阶段新增了以下文件：

```text
requirements.txt
main.py
app_image.py
src/__init__.py
src/image_pose_estimator.py
assets/input/.gitkeep
assets/output/.gitkeep
```

对应提交命令：

```bash
git add requirements.txt main.py app_image.py src assets
git commit -m "实现图片人体关键点识别功能"
```

### 3. 运行测试命令

```bash
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env python main.py --help
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env python main.py --input assets/input/test_blank.jpg --output outputs/test_blank_result.jpg
```

### 4. 版本发布命令

```bash
git push origin main
git tag v1.0.0
git push origin v1.0.0
```
