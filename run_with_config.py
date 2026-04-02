#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用配置文件运行自助提报自动化脚本
"""

import json
import os
import sys
from api_automation import APIConfig, process_excel
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.json") -> dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(config_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, config_path)
        
        logger.info(f"正在加载配置文件: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info("配置文件加载成功")
        return config
        
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"加载配置文件时发生异常: {str(e)}")
        sys.exit(1)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("自助提报自动化脚本开始运行（使用配置文件）")
    logger.info("=" * 60)
    
    # 加载配置
    config_dict = load_config()
    
    # 显示配置信息
    logger.info("配置信息:")
    logger.info(f"  - X-AUTH: {config_dict.get('x_auth', 'N/A')}")
    logger.info(f"  - 周期: {config_dict.get('period_start_date', 'N/A')} 至 {config_dict.get('period_end_date', 'N/A')}")
    logger.info(f"  - Excel文件: {config_dict.get('excel_path', 'N/A')}")
    logger.info(f"  - 用户ID: {config_dict.get('user_id', 'N/A')}")
    logger.info(f"  - 采集组记录ID: {config_dict.get('collection_group_record_id', 'N/A')}")
    logger.info(f"  - 输入列: {config_dict.get('input_column', 'N/A')}")
    logger.info(f"  - 输出列: {config_dict.get('output_column', 'N/A')}")
    logger.info("=" * 60)
    
    # 创建API配置对象
    api_config = APIConfig(
        x_auth=config_dict.get('x_auth'),
        period_start_date=config_dict.get('period_start_date'),
        period_end_date=config_dict.get('period_end_date')
    )
    
    # 处理Excel文件
    success = process_excel(
        excel_path=config_dict.get('excel_path'),
        config=api_config,
        input_column=config_dict.get('input_column', '输入'),
        output_column=config_dict.get('output_column', '实际输出'),
        user_id=config_dict.get('user_id', '346568'),
        collection_group_record_id=config_dict.get('collection_group_record_id', '166')
    )
    
    if success:
        logger.info("=" * 60)
        logger.info("脚本执行成功！")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("脚本执行失败！")
        logger.error("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
