# Git 操作记录

本文档用于记录本项目从旧仓库清理、重新开发、分支合并到版本发布的 Git 操作过程。

## 一、任务一：版本管理与 Git 基础认知

### 1. 为什么软件开发需要版本管理

软件开发过程中会持续出现需求变更、功能迭代、缺陷修复和多人协作。如果只依赖复制文件夹进行备份，容易出现文件混乱、版本含义不清、无法追踪修改原因、难以回退历史版本等问题。版本管理系统可以记录每一次修改的内容、作者、时间和说明，使项目具备可追踪、可回退和可协作的能力。

### 2. Git 与普通文件备份的区别

- 普通备份通常只能保存某一时刻的文件副本，缺少明确提交说明。
- Git 会以提交记录的形式保存项目历史，每次提交都对应一个快照。
- Git 可以通过分支支持并行开发，通过合并将功能变更纳入主线。
- Git 可以通过标签标记稳定版本，例如本项目的 `v1.0.0` 和 `v1.0.1`。
- Git 可以与 GitHub 远程仓库结合，实现远程备份、拉取、推送和版本发布。

### 3. Git 的基本区域

| 区域 | 说明 |
| --- | --- |
| 工作区 | 当前正在编辑和运行的项目文件。 |
| 暂存区 | 通过 `git add` 加入、准备提交的变更集合。 |
| 本地仓库 | 通过 `git commit` 保存的本地历史记录。 |
| 远程仓库 | GitHub 上的仓库，用于远程同步和共享。 |

### 4. 常用 Git 命令说明

| 命令 | 作用 |
| --- | --- |
| `git init` | 在本地目录初始化 Git 仓库。 |
| `git clone` | 从远程仓库克隆项目到本地。 |
| `git status` | 查看当前工作区和暂存区状态。 |
| `git add` | 将文件变更加入暂存区。 |
| `git commit` | 将暂存区内容提交到本地仓库。 |
| `git log` | 查看提交历史。 |
| `git diff` | 查看工作区或暂存区中的文件差异。 |
| `git branch` | 查看、创建或删除分支。 |
| `git switch` / `git checkout` | 切换分支。 |
| `git merge` | 合并分支。 |
| `git pull` | 从远程仓库拉取并合并更新。 |
| `git push` | 将本地提交推送到远程仓库。 |
| `git tag` | 创建或查看版本标签。 |

### 5. 本项目采用的分支策略

本项目采用简单的主线分支与功能分支开发流程：

1. `master` 分支用于保存稳定代码。
2. 在 `master` 分支完成图片人体关键点识别功能后发布 `v1.0.0`。
3. 从 `master` 创建 `feature/video-pose` 分支开发视频人体关键点识别功能。
4. 视频功能测试通过后，将 `feature/video-pose` 合并回 `master`。
5. 在 `master` 分支发布 `v1.0.1`。

## 二、已执行的仓库准备操作

### 1. 检查 Git 版本

```powershell
git --version
```

结果：

```text
git version 2.45.1.windows.1
```

### 2. 检查 conda 环境

```powershell
& "C:\Users\reneryi\Miniconda3\condabin\conda.bat" run -n jc_env python --version
```

结果：

```text
Python 3.10.20
```

### 3. 查看远程仓库原有分支和标签

```powershell
git ls-remote --heads --tags https://github.com/reneryi/human-pose-keypoint-recognition.git
```

远程仓库原先存在 `main` 分支和旧的 `v1.0.0` 标签。由于旧项目文件无参考价值，后续将清空旧文件并重新发布新的版本标签。

### 4. 初始化本地仓库并关联远程仓库

```powershell
git init
git remote add origin https://github.com/reneryi/human-pose-keypoint-recognition.git
git fetch origin --tags
git switch -c master origin/main
```

说明：本地创建 `master` 分支，并基于远程旧 `main` 分支继续操作，这样既保留远程仓库地址，又可以清理旧文件后重新构建项目。

### 5. 清空旧项目文件

```powershell
git rm -r .
git status --short --branch
git diff --cached --stat
git commit -m "chore: clear legacy project files"
```

该提交用于明确记录“旧项目文件已清空”。

### 6. 创建新的项目实施计划

```powershell
git add PROJECT_PLAN.md
git commit -m "docs: add project implementation plan"
```

### 7. 创建新的基础项目结构

```powershell
git add .gitignore README.md requirements.txt docs/.gitkeep assets/.gitkeep outputs/image_result/.gitkeep outputs/video_result/.gitkeep screenshots/.gitkeep
git commit -m "chore: initialize new project structure"
```

## 三、后续将继续记录的操作

- 图片识别功能开发与 `v1.0.0` 标签发布。
- `feature/video-pose` 分支创建与视频识别功能开发。
- 功能分支合并、`v1.0.1` 标签发布。
- `git pull`、`git push`、分支和标签推送操作。

## 四、任务二：本地仓库建立与文件基本操作记录

### 1. 文件删除操作

旧项目文件通过以下命令统一删除，并形成提交记录：

```powershell
git rm -r .
git diff --cached --stat
git commit -m "chore: clear legacy project files"
```

该步骤体现了“删除文件并纳入版本管理”的过程。

### 2. 文件新增操作

重新创建项目计划、基础目录、依赖文件和说明文档：

```powershell
git add PROJECT_PLAN.md
git commit -m "docs: add project implementation plan"

git add .gitignore README.md requirements.txt docs/.gitkeep assets/.gitkeep outputs/image_result/.gitkeep outputs/video_result/.gitkeep screenshots/.gitkeep
git commit -m "chore: initialize new project structure"
```

该步骤体现了“新增文件并提交到本地仓库”的过程。

### 3. 文件修改操作

随着实验推进，`PROJECT_PLAN.md` 与文档文件会持续修改，并通过 `git diff` 查看差异后提交：

```powershell
git status --short --branch
git diff
git add PROJECT_PLAN.md docs/Git操作记录.md
git commit -m "docs: record local repository operations"
```

### 4. 查看提交历史

使用以下命令查看历史记录：

```powershell
git log --oneline --decorate -10
```

当前项目已经形成多次语义清晰的提交，避免了一次性提交全部内容的问题。

### 5. 本阶段提交记录示例

```text
chore: clear legacy project files
docs: add project implementation plan
chore: initialize new project structure
docs: add git basics and experiment outline
docs: record local repository operations
```
