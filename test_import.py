#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本，检查依赖包和基本功能
"""

import sys

def test_imports():
    """测试导入所需的包"""
    print("正在测试依赖包...")
    print("=" * 60)
    
    # 测试requests
    try:
        import requests
        print(f"✓ requests {requests.__version__} - 已安装")
    except ImportError:
        print("✗ requests - 未安装")
        print("  请运行: pip install requests")
        return False
    
    # 测试pandas
    try:
        import pandas as pd
        print(f"✓ pandas {pd.__version__} - 已安装")
    except ImportError:
        print("✗ pandas - 未安装")
        print("  请运行: pip install pandas")
        return False
    
    # 测试openpyxl
    try:
        import openpyxl
        print(f"✓ openpyxl {openpyxl.__version__} - 已安装")
    except ImportError:
        print("✗ openpyxl - 未安装")
        print("  请运行: pip install openpyxl")
        return False
    
    print("=" * 60)
    print("所有依赖包检查通过！")
    return True


def test_config():
    """测试配置文件"""
    print("\n正在测试配置文件...")
    print("=" * 60)
    
    try:
        import json
        import os
        
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✓ 配置文件存在且格式正确")
            print(f"  - X-AUTH: {config.get('x_auth', 'N/A')[:20]}...")
            print(f"  - 周期: {config.get('period_start_date')} 至 {config.get('period_end_date')}")
            print(f"  - Excel: {config.get('excel_path', 'N/A')}")
            return True
        else:
            print("✗ 配置文件不存在")
            return False
    except Exception as e:
        print(f"✗ 配置文件错误: {str(e)}")
        return False


def test_excel():
    """测试Excel文件"""
    print("\n正在测试Excel文件...")
    print("=" * 60)
    
    try:
        import json
        import os
        import pandas as pd
        
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        excel_path = config.get('excel_path')
        
        if not os.path.exists(excel_path):
            print(f"✗ Excel文件不存在: {excel_path}")
            return False
        
        df = pd.read_excel(excel_path)
        print(f"✓ Excel文件存在且可读")
        print(f"  - 行数: {len(df)}")
        print(f"  - 列名: {df.columns.tolist()}")
        
        input_col = config.get('input_column', '输入')
        if input_col in df.columns:
            print(f"  - ✓ 找到输入列: {input_col}")
            non_empty = df[input_col].notna().sum()
            print(f"  - 非空行数: {non_empty}")
        else:
            print(f"  - ✗ 未找到输入列: {input_col}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Excel文件错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_api_module():
    """测试API模块"""
    print("\n正在测试API模块...")
    print("=" * 60)
    
    try:
        from api_automation import APIConfig, SelfReportAPI
        print("✓ API模块导入成功")
        
        # 测试创建配置对象
        config = APIConfig(
            x_auth="test",
            period_start_date="2025-12-01",
            period_end_date="2025-12-31"
        )
        print("✓ APIConfig对象创建成功")
        
        # 测试创建API客户端
        api = SelfReportAPI(config)
        print("✓ SelfReportAPI对象创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ API模块错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("自助提报自动化脚本 - 测试工具")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    print("=" * 60 + "\n")
    
    results = []
    
    # 测试依赖包
    results.append(("依赖包", test_imports()))
    
    # 测试API模块
    results.append(("API模块", test_api_module()))
    
    # 测试配置文件
    results.append(("配置文件", test_config()))
    
    # 测试Excel文件
    results.append(("Excel文件", test_excel()))
    
    # 显示总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    all_pass = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
        if not result:
            all_pass = False
    
    print("=" * 60)
    
    if all_pass:
        print("\n所有测试通过！可以运行主脚本了。")
        print("运行命令: python run_with_config.py")
    else:
        print("\n部分测试失败，请先解决上述问题。")
    
    print("\n")


if __name__ == "__main__":
    main()
