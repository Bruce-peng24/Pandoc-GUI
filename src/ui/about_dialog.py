"""
关于与鸣谢对话框
包含应用程序信息、版本和开源协议声明
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTabWidget, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

# 添加当前目录到路径，以便导入模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AboutDialog(QDialog):
    """关于与鸣谢对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于与鸣谢")
        self.setModal(True)
        self.resize(700, 600)
        
        # 获取项目根目录
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        tabs = QTabWidget()
        
        # 关于选项卡
        about_tab = self.create_about_tab()
        tabs.addTab(about_tab, "关于")
        
        # 鸣谢选项卡
        credits_tab = self.create_credits_tab()
        tabs.addTab(credits_tab, "鸣谢")
        
        # 许可协议选项卡
        license_tab = self.create_license_tab()
        tabs.addTab(license_tab, "许可协议")
        
        layout.addWidget(tabs)
        
        # 添加关闭按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
    def create_about_tab(self):
        """创建关于选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 应用图标和名称
        header_layout = QHBoxLayout()
        
        # 尝试加载应用图标（如果有的话）
        icon_path = os.path.join(self.root_dir, "assets", "icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
            header_layout.addWidget(icon_label)
        else:
            # 如果没有图标，添加一个占位符
            icon_label = QLabel("📄")
            icon_label.setStyleSheet("font-size: 48px;")
            header_layout.addWidget(icon_label)
        
        # 应用名称和版本信息
        info_layout = QVBoxLayout()
        
        app_name = QLabel("Pandoc GUI")
        app_name.setFont(QFont("Arial", 16, QFont.Bold))
        info_layout.addWidget(app_name)
        
        version = QLabel("版本: 1.0.0")
        info_layout.addWidget(version)
        
        description = QLabel("一个简单易用的Pandoc图形界面工具")
        description.setWordWrap(True)
        info_layout.addWidget(description)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # 应用说明
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
            <h3>应用简介</h3>
            <p>Pandoc GUI 是一个基于 Pandoc 的文档转换工具的图形用户界面。</p>
            <p>它提供了一个简单易用的界面，让用户无需记忆复杂的命令行参数即可轻松地转换文档格式。</p>
            
            <h3>主要功能</h3>
            <ul>
                <li>支持多种文档格式之间的转换，包括 Markdown、Word、PDF、HTML 等</li>
                <li>提供直观的图形用户界面</li>
                <li>支持自定义模板</li>
                <li>支持文档排版配置</li>
            </ul>
            
            <h3>技术支持</h3>
            <p>如需技术支持或有任何问题，请参考文档或联系开发者。</p>
        """)
        
        layout.addWidget(about_text)
        
        return widget
    
    def create_credits_tab(self):
        """创建鸣谢选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        
        # 尝试读取第三方开源协议文件
        third_party_licenses_path = os.path.join(self.root_dir, "dist", "第三方开源协议.txt")
        if os.path.exists(third_party_licenses_path):
            with open(third_party_licenses_path, 'r', encoding='utf-8') as f:
                content = f.read()
                credits_text.setPlainText(content)
        else:
            # 如果文件不存在，使用默认内容
            credits_text.setHtml("""
                <h2>第三方开源组件协议声明</h2>
                <p>本软件使用了以下开源组件，特此声明其版权及许可信息：</p>
                
                <h3>1. Pandoc (核心组件)</h3>
                <p>授权协议：GPL v2+</p>
                <p>版权所有者：John MacFarlane</p>
                <p>官方网址：<a href="https://pandoc.org/">https://pandoc.org/</a></p>
                <p>要求：必须保留版权声明和授权信息</p>
                
                <h3>2. PyQt5</h3>
                <p>授权协议：GPL v3</p>
                <p>版权所有者：Riverbank Computing Limited</p>
                <p>官方网址：<a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a></p>
                
                <h3>版权声明</h3>
                <p>本软件是依据上述开源组件的许可协议分发的。</p>
                <p>这些组件的版权和许可协议的完整文本可以在各自的官方网站上找到。</p>
            """)
        
        layout.addWidget(credits_text)
        
        return widget
    
    def create_license_tab(self):
        """创建许可协议选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建可滚动的文本区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        
        # 尝试读取LICENSE文件
        license_path = os.path.join(self.root_dir, "LICENSE")
        if os.path.exists(license_path):
            with open(license_path, 'r', encoding='utf-8') as f:
                content = f.read()
                license_text.setPlainText(content)
        else:
            # 如果文件不存在，使用默认内容
            license_text.setHtml("""
                <h2>GNU通用公共许可证</h2>
                <p>本程序是自由软件：您可以根据自由软件基金会发布的GNU通用公共许可证条款（第3版或更新版本）重新分发和/或修改它。</p>
                <p>分发本程序是希望它能发挥作用，但没有任何担保；甚至没有对适销性或特定用途适用性的暗示担保。有关详细信息，请参阅GNU通用公共许可证。</p>
                <p>您应该随本程序收到一份GNU通用公共许可证。如果没有，请参阅<a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>。</p>
            """)
        
        scroll_area.setWidget(license_text)
        layout.addWidget(scroll_area)
        
        return widget