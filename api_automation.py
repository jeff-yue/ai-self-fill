#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自助提报自动化脚本
功能：
1. 调用获取会话ID接口获取conversationId
2. 调用发送对话消息接口，从Excel读取输入内容，将响应写回Excel
"""

import requests
import pandas as pd
import json
import re
from typing import Optional, Dict, Any, Tuple, List
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIConfig:
    """API配置类"""
    def __init__(self, x_auth: str, period_start_date: str, period_end_date: str):
        """
        初始化API配置
        
        Args:
            x_auth: 认证token
            period_start_date: 周期开始日期，格式：YYYY-MM-DD
            period_end_date: 周期结束日期，格式：YYYY-MM-DD
        """
        self.x_auth = x_auth
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.base_url = "https://appwx-in-hrowx-test.ciwork.cn/api/ess/hroAttendance/ai-self-fill"
        self.headers = {
            "Content-Type": "application/json",
            "X-AUTH": self.x_auth
        }


class SelfReportAPI:
    """自助提报API客户端"""
    
    def __init__(self, config: APIConfig):
        """
        初始化API客户端
        
        Args:
            config: API配置对象
        """
        self.config = config
    
    def get_conversation_id(self, collection_group_record_id: str = "166") -> Optional[str]:
        """
        获取会话ID
        
        Args:
            collection_group_record_id: 采集组记录ID，默认为166
            
        Returns:
            conversationId或None（如果失败）
        """
        url = f"{self.config.base_url}/start"
        payload = {
            "periodStartDate": self.config.period_start_date,
            "periodEndDate": self.config.period_end_date,
            "collectionGroupRecordId": collection_group_record_id
        }
        
        try:
            logger.info(f"正在调用获取会话ID接口: {url}")
            logger.info(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")
            
            response = requests.post(
                url,
                headers=self.config.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"响应结果: {json.dumps(result, ensure_ascii=False)}")
            
            # 兼容code为字符串"200"或数字0的情况
            code = result.get("code")
            if code in [0, "0", "200", 200]:
                conversation_id = result.get("data", {}).get("conversationId")
                welcome_message = result.get("data", {}).get("welcomeMessage")
                logger.info(f"成功获取会话ID: {conversation_id}")
                if welcome_message:
                    logger.info(f"欢迎消息: {welcome_message}")
                return conversation_id
            else:
                logger.error(f"接口返回错误: {result.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"发生异常: {str(e)}")
            return None
    
    def send_message(
        self,
        content: str,
        conversation_id: str,
        user_id: str = "346568"
    ) -> Optional[str]:
        """
        发送对话消息
        
        Args:
            content: 消息内容
            conversation_id: 会话ID
            user_id: 用户ID，默认为346568
            
        Returns:
            响应的content内容或None（如果失败）
        """
        url = f"{self.config.base_url}/chat"
        payload = {
            "userId": user_id,
            "content": content,
            "conversationId": conversation_id,
            "periodStartDate": self.config.period_start_date,
            "periodEndDate": self.config.period_end_date
        }
        
        try:
            logger.info(f"正在发送对话消息: {content}")
            
            response = requests.post(
                url,
                headers=self.config.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 兼容code为字符串"200"或数字0的情况
            code = result.get("code")
            if code in [0, "0", "200", 200]:
                response_content = result.get("data", {}).get("content")
                logger.info(f"成功接收响应: {response_content}")
                return response_content
            else:
                logger.error(f"接口返回错误: {result.get('message')}")
                return f"错误: {result.get('message')}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            return f"请求失败: {str(e)}"
        except Exception as e:
            logger.error(f"发生异常: {str(e)}")
            return f"异常: {str(e)}"


def parse_say_count(input_content: str) -> Tuple[int, List[str]]:
    """
    解析输入中的 "say" 关键字，提取对话次数和消息列表

    Args:
        input_content: 输入内容

    Returns:
        Tuple[对话次数, 消息列表]
        - 有say时：返回 (say个数, [消息1, 消息2, ...])
        - 无say时：返回 (1, [原始输入])
    """
    input_str = str(input_content).strip()

    # 找到所有say关键字的位置（支持中英文冒号）
    say_pattern = r'say\s*[:：]'
    say_positions = [m.start() for m in re.finditer(say_pattern, input_str, re.IGNORECASE)]

    if not say_positions:
        # 没有 "say" 关键字，默认对话次数为1，返回原始输入
        return 1, [input_str]

    # 提取每个say后的内容
    messages = []
    for i, pos in enumerate(say_positions):
        # 找到say关键字后的冒号位置
        colon_match = re.search(r'say\s*[:：]', input_str[pos:], re.IGNORECASE)
        if colon_match:
            content_start = pos + colon_match.end()
            # 确定内容结束位置（下一个say关键字前或字符串末尾）
            if i + 1 < len(say_positions):
                content_end = say_positions[i + 1]
            else:
                content_end = len(input_str)
            # 提取内容
            content = input_str[content_start:content_end].strip()
            if content:
                messages.append(content)

    if messages:
        # 有say关键字，返回say个数和消息列表
        return len(messages), messages
    else:
        # say关键字后没有内容，返回原始输入
        return 1, [input_str]


def process_multi_turn_dialog(
    api_client: SelfReportAPI,
    messages: List[str],
    conversation_id: str,
    user_id: str,
    add_prefix: bool = True
) -> str:
    """
    处理多轮对话

    Args:
        api_client: API客户端
        messages: 消息列表，每轮对话使用对应的消息
        conversation_id: 会话ID
        user_id: 用户ID
        add_prefix: 是否在回答前添加 "answer:" 前缀，默认为True

    Returns:
        拼接后的回答结果，用换行符分隔
    """
    answers = []
    turn_count = len(messages)

    logger.info(f"  多轮对话参数: turn_count={turn_count}, add_prefix={add_prefix}")

    for turn, current_message in enumerate(messages, 1):
        logger.info(f"  第 {turn}/{turn_count} 轮对话: {current_message}")

        # 调用API发送消息
        response_content = api_client.send_message(
            content=current_message,
            conversation_id=conversation_id,
            user_id=user_id
        )

        # 根据add_prefix参数决定是否拼接 "answer:" 前缀
        if add_prefix:
            if response_content:
                answer = f"answer: {response_content}"
            else:
                answer = f"answer: 处理失败"
            logger.info(f"  第 {turn}轮回答（带前缀）: {answer}")
        else:
            if response_content:
                answer = response_content
            else:
                answer = "处理失败"
            logger.info(f"  第 {turn}轮回答（无前缀）: {answer}")

        answers.append(answer)

    # 用换行符连接所有回答
    result = "\n".join(answers)
    logger.info(f"  多轮对话最终结果: {result}")
    return result


def process_excel(
    excel_path: str,
    config: APIConfig,
    input_column: str = "输入",
    output_column: str = "实际输出",
    user_id: str = "346568",
    collection_group_record_id: str = "166"
) -> bool:
    """
    处理Excel文件，调用API并写回结果

    Args:
        excel_path: Excel文件路径
        config: API配置对象
        input_column: 输入列名，默认为"输入"
        output_column: 输出列名，默认为"实际输出"
        user_id: 用户ID
        collection_group_record_id: 采集组记录ID

    Returns:
        处理是否成功
    """
    try:
        # 读取Excel文件
        logger.info(f"正在读取Excel文件: {excel_path}")
        df = pd.read_excel(excel_path)
        logger.info(f"Excel文件列名: {df.columns.tolist()}")
        logger.info(f"共有 {len(df)} 行数据")

        # 检查必需的列是否存在
        if input_column not in df.columns:
            logger.error(f"未找到输入列: {input_column}")
            return False

        # 如果输出列不存在，创建它
        if output_column not in df.columns:
            df[output_column] = ""
            logger.info(f"创建输出列: {output_column}")

        # 确保输出列为字符串类型，避免pandas类型转换错误
        df[output_column] = df[output_column].astype(str).replace('nan', '')

        # 初始化API客户端
        api_client = SelfReportAPI(config)

        # 处理每一行数据
        success_count = 0
        for index, row in df.iterrows():
            # 为每行数据获取新的会话ID
            conversation_id = api_client.get_conversation_id(collection_group_record_id)
            if not conversation_id:
                logger.error(f"第 {index + 1} 行无法获取会话ID，跳过")
                continue

            input_content = row[input_column]

            # 跳过空值
            if pd.isna(input_content) or str(input_content).strip() == "":
                logger.info(f"第 {index + 1} 行输入为空，跳过")
                continue

            # 解析 "say" 关键字，获取对话次数和消息列表
            turn_count, messages = parse_say_count(str(input_content))

            logger.info(f"处理第 {index + 1} 行: {input_content}")
            logger.info(f"  解析结果: 对话次数={turn_count}, 消息列表={messages}")

            # 处理多轮对话
            # 当turn_count == 1（没有say）时，不添加前缀；当turn_count > 1（有say）时，添加前缀
            response_content = process_multi_turn_dialog(
                api_client=api_client,
                messages=messages,
                conversation_id=conversation_id,
                user_id=user_id,
                add_prefix=(turn_count > 1)
            )

            # 写入响应结果
            if response_content:
                df.at[index, output_column] = response_content
                success_count += 1
                logger.info(f"第 {index + 1} 行处理成功")
            else:
                df.at[index, output_column] = "处理失败"
                logger.warning(f"第 {index + 1} 行处理失败")

        # 保存Excel文件
        logger.info(f"正在保存Excel文件: {excel_path}")
        df.to_excel(excel_path, index=False)
        logger.info(f"处理完成！成功处理 {success_count}/{len(df)} 行数据")

        return True

    except FileNotFoundError:
        logger.error(f"文件不存在: {excel_path}")
        return False
    except Exception as e:
        logger.error(f"处理Excel文件时发生异常: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def main():
    """主函数"""
    # ========== 配置参数区域 ==========
    # 请根据实际情况修改以下配置
    
    # API认证token
    X_AUTH = "AFC0937794E21C554173E597B33640BA"
    
    # 周期日期
    PERIOD_START_DATE = "2025-12-01"
    PERIOD_END_DATE = "2025-12-31"
    
    # Excel文件路径
    EXCEL_PATH = r"e:\同道\HCM\自助提报自动化\自助填报会话.xlsx"
    
    # 用户ID
    USER_ID = "346568"
    
    # 采集组记录ID
    COLLECTION_GROUP_RECORD_ID = "166"
    
    # Excel列名
    INPUT_COLUMN = "输入"
    OUTPUT_COLUMN = "实际输出"
    
    # ===================================
    
    logger.info("=" * 60)
    logger.info("自助提报自动化脚本开始运行")
    logger.info("=" * 60)
    logger.info(f"配置信息:")
    logger.info(f"  - X-AUTH: {X_AUTH}")
    logger.info(f"  - 周期: {PERIOD_START_DATE} 至 {PERIOD_END_DATE}")
    logger.info(f"  - Excel文件: {EXCEL_PATH}")
    logger.info(f"  - 用户ID: {USER_ID}")
    logger.info(f"  - 采集组记录ID: {COLLECTION_GROUP_RECORD_ID}")
    logger.info("=" * 60)
    
    # 创建配置对象
    config = APIConfig(
        x_auth=X_AUTH,
        period_start_date=PERIOD_START_DATE,
        period_end_date=PERIOD_END_DATE
    )
    
    # 处理Excel文件
    success = process_excel(
        excel_path=EXCEL_PATH,
        config=config,
        input_column=INPUT_COLUMN,
        output_column=OUTPUT_COLUMN,
        user_id=USER_ID,
        collection_group_record_id=COLLECTION_GROUP_RECORD_ID
    )
    
    if success:
        logger.info("=" * 60)
        logger.info("脚本执行成功！")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("脚本执行失败！")
        logger.error("=" * 60)


if __name__ == "__main__":
    main()
