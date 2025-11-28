#!/usr/bin/env python3
"""
Pandoc GUI 应用程序打包工具
这个脚本提供了简单的界面来重新打包应用程序
"""

import os
import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QTextEdit, QGroupBox,
                            QCheckBox, QProgressBar, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class BuildThread(QThread):
    """后台执行打包操作的线程"""
    output_updated = pyqtSignal(str)
    build_finished = pyqtSignal(bool, str)
    
    def __init__(self, build_command):
        super().__init__()
        self.build_command = build_command
    
    def run(self):
        """执行打包命令"""
        try:
            process = subprocess.Popen(
                self.build_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_updated.emit(output.strip())
            
            return_code = process.poll()
            
            if return_code == 0:
                self.build_finished.emit(True, "Build successful!")
            else:
                self.build_finished.emit(False, f"Build failed with code {return_code}")
                
        except Exception as e:
            self.build_finished.emit(False, f"Error: {str(e)}")

class RebuildTool(QMainWindow):
    """重新打包工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandoc-GUI 打包工具")
        self.setGeometry(100, 100, 800, 600)
        self.build_thread = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("Pandoc-GUI 重新打包工具")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明
        info_label = QLabel("这个工具可以帮助你重新打包 Pandoc-GUI 应用程序。\n使用已验证成功的配置，确保打包顺利。")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 构建选项
        options_group = QGroupBox("构建选项")
        options_layout = QVBoxLayout()
        
        self.onefile_checkbox = QCheckBox("单文件模式 (--onefile)")
        self.onefile_checkbox.setChecked(True)
        options_layout.addWidget(self.onefile_checkbox)
        
        self.windowed_checkbox = QCheckBox("窗口模式 (--windowed)")
        self.windowed_checkbox.setChecked(True)
        options_layout.addWidget(self.windowed_checkbox)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 构建按钮
        build_layout = QHBoxLayout()
        
        self.build_button = QPushButton("开始打包")
        self.build_button.clicked.connect(self.start_build)
        self.build_button.setMinimumHeight(40)
        build_layout.addWidget(self.build_button)
        
        self.test_button = QPushButton("测试可执行文件")
        self.test_button.clicked.connect(self.test_executable)
        self.test_button.setMinimumHeight(40)
        self.test_button.setEnabled(False)
        build_layout.addWidget(self.test_button)
        
        layout.addLayout(build_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 输出日志
        output_group = QGroupBox("输出日志")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFontFamily("Consolas, monospace")
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)
    
    def start_build(self):
        """开始打包过程"""
        if self.build_thread and self.build_thread.isRunning():
            return
        
        # 构建命令
        command = [
            "pyinstaller"
        ]
        
        if self.onefile_checkbox.isChecked():
            command.append("--onefile")
        
        if self.windowed_checkbox.isChecked():
            command.append("--windowed")
        else:
            command.append("--console")
        
        command.extend([
            "--name=Pandoc-GUI",
            "--add-data", "src;src",
            "--collect-all", "PyQt5",
            "--collect-all", "docx",
            "--collect-all", "python-docx",
            "--collect-all", "ntplib",
            "app_minimal_fixed.py"
        ])
        
        # 更新UI
        self.build_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.output_text.clear()
        self.status_label.setText("正在打包...")
        
        # 创建并启动构建线程
        self.build_thread = BuildThread(command)
        self.build_thread.output_updated.connect(self.update_output)
        self.build_thread.build_finished.connect(self.build_finished)
        self.build_thread.start()
    
    def update_output(self, text):
        """更新输出日志"""
        self.output_text.append(text)
        # 滚动到底部
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)
    
    def build_finished(self, success, message):
        """构建完成后的处理"""
        self.progress_bar.setVisible(False)
        self.build_button.setEnabled(True)
        
        if success:
            self.status_label.setText("打包成功!")
            self.test_button.setEnabled(True)
            self.output_text.append(f"\n{message}")
            QMessageBox.information(self, "打包成功", "应用程序已成功打包!")
        else:
            self.status_label.setText("打包失败")
            self.output_text.append(f"\n错误: {message}")
            QMessageBox.critical(self, "打包失败", f"打包过程中发生错误:\n{message}")
    
    def test_executable(self):
        """测试可执行文件"""
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'Pandoc-GUI.exe')
        
        if not os.path.exists(exe_path):
            QMessageBox.warning(self, "文件不存在", "找不到打包后的可执行文件!")
            return
        
        try:
            # 启动可执行文件
            subprocess.Popen([exe_path])
            self.status_label.setText("已启动测试程序")
        except Exception as e:
            QMessageBox.critical(self, "启动失败", f"无法启动可执行文件:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RebuildTool()
    window.show()
    sys.exit(app.exec_())