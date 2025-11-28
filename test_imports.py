#!/usr/bin/env python3
"""
测试所有导入是否正常工作
用于在打包前验证所有模块都能正确导入
"""

import sys
import os

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_imports():
    """测试所有关键模块的导入"""
    success = True
    error_messages = []
    
    # 测试核心模块
    modules_to_test = [
        ('core.pandoc_converter', 'PandocConverter'),
        ('core.config_manager', 'ConfigManager'),
        ('core.template_manager', 'TemplateManager'),
        ('core.version_checker', 'get_expiration_message'),
        ('ui.format_config', 'FormatConfigDialog'),
        ('ui.about_dialog', 'AboutDialog'),  # 新添加的模块
        ('utils.file_utils', 'get_file_path'),
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {module_name}.{class_name} - 导入成功")
        except Exception as e:
            success = False
            error_messages.append(f"✗ {module_name}.{class_name} - 导入失败: {e}")
            print(error_messages[-1])
    
    # 测试主窗口导入
    try:
        from ui.main_window import PandocGUI
        print("✓ ui.main_window.PandocGUI - 导入成功")
    except Exception as e:
        success = False
        error_messages.append(f"✗ ui.main_window.PandocGUI - 导入失败: {e}")
        print(error_messages[-1])
    
    # 测试入口文件导入
    try:
        import app_minimal_fixed
        print("✓ app_minimal_fixed - 导入成功")
    except Exception as e:
        success = False
        error_messages.append(f"✗ app_minimal_fixed - 导入失败: {e}")
        print(error_messages[-1])
    
    return success, error_messages

if __name__ == '__main__':
    print("正在测试模块导入...")
    print("-" * 50)
    
    success, errors = test_imports()
    
    print("-" * 50)
    if success:
        print("所有模块导入测试通过！")
        print("可以安全地使用 rebuild_app.bat 进行打包。")
    else:
        print(f"导入测试失败，发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"  - {error}")
        print("请修复这些错误后再尝试打包。")
    
    input("按任意键退出...")