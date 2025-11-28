# Pandoc-GUI 重新打包指南

## 概述

本指南详细说明了如何重新打包 Pandoc-GUI 应用程序，基于已成功的配置。

## 方法一：使用重新打包脚本（推荐）

最简单的方法是使用项目根目录中的 `rebuild_app.bat` 脚本：

```bash
rebuild_app.bat
```

这个脚本包含了所有必要的依赖项配置，基于你之前成功打包的设置。

## 方法二：手动打包命令

如果脚本无法使用，你可以手动执行以下命令：

1. 打开命令提示符（不是PowerShell）

2. 导航到项目目录：
   ```bash
   cd /d C:\Practice-code\Pandoc-GUI
   ```

3. 执行打包命令：
   ```bash
   pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --collect-all PyQt5 --collect-all docx --collect-all python-docx --collect-all ntplib app_minimal_fixed.py
   ```

4. 测试结果：
   ```bash
   dist\Pandoc-GUI.exe
   ```

## 关键配置说明

以下是对打包命令中各参数的解释：

- `--onefile`: 将应用程序打包为单个可执行文件
- `--windowed`: 创建GUI应用程序（无控制台窗口）
- `--name="Pandoc-GUI"`: 指定输出文件名
- `--add-data "src;src"`: 包含src目录中的所有文件
- `--collect-all PyQt5`: 包含PyQt5及其所有子模块
- `--collect-all docx`: 包含python-docx库及其所有依赖
- `--collect-all python-docx`: 确保docx模块的完整包含
- `--collect-all ntplib`: 包含网络时间库
- `app_minimal_fixed.py`: 使用修复后的入口点

## 常见问题和解决方案

### 问题1：找不到模块（如 'docx', 'ui' 等）

**解决方案**：
1. 确保使用了 `--collect-all` 选项包含所有必要的库
2. 检查 `--add-data` 是否正确包含了src目录
3. 尝试添加特定的 `--hidden-import` 选项

### 问题2：网络检查失败

**解决方案**：
1. 使用 `app_minimal_fixed.py` 作为入口点，它使用简化的过期检查
2. 确保 `--collect-all ntplib` 选项已包含

### 问题3：批处理文件编码问题

**解决方案**：
1. 使用命令提示符而不是PowerShell
2. 手动执行PyInstaller命令
3. 确保批处理文件使用UTF-8编码保存

## 入口点选择

项目中包含多个入口点文件，各自用途：

- `app_minimal_fixed.py`: **推荐使用** - 成功打包的版本，使用简化的网络检查
- `app_minimal.py`: 原始最小化版本
- `app_robust.py`: 包含更多错误处理的版本

建议始终使用 `app_minimal_fixed.py` 作为入口点，因为它是已验证可以成功打包和运行的版本。

## 依赖项列表

Pandoc-GUI 需要以下Python包：

```
PyQt5
python-docx
ntplib
```

如果需要重新安装这些依赖，可以使用：

```bash
pip install PyQt5 python-docx ntplib pyinstaller
```

## 虚拟环境使用

为避免依赖冲突，建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install PyQt5 python-docx ntplib pyinstaller

# 打包应用程序
pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --collect-all PyQt5 --collect-all docx --collect-all python-docx --collect-all ntplib app_minimal_fixed.py
```

## 测试建议

1. **打包后测试**：始终测试打包后的可执行文件是否能正常运行
2. **依赖检查**：如果程序运行不正常，检查是否缺少依赖
3. **错误日志**：考虑在开发环境中添加更多日志记录，以便在打包后调试

## 更新项目后的重新打包

当更新项目后：

1. 如果只修改了 `src/` 目录中的代码，通常不需要更改打包命令
2. 如果添加了新的依赖，需要更新 `--collect-all` 或 `--hidden-import` 选项
3. 如果修改了入口点文件，需要相应更新打包命令中的入口点参数

## 总结

使用 `rebuild_app.bat` 脚本是最简单的重新打包方法。如果遇到问题，参考本指南中的手动命令和常见问题解决方案。