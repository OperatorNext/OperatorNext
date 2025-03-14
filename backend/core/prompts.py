from browser_use import SystemPrompt


class ChineseSystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # 获取父类的规则
        existing_rules = super().important_rules()

        # 添加中文输出的规则
        new_rules = """
9. MOST IMPORTANT RULE:
- All evaluation messages, memory messages, and next goal messages MUST be in Chinese language!
- 所有评估信息(evaluation)必须使用中文输出!
- 所有记忆信息(memory)必须使用中文输出!
- 所有下一步目标(next goal)必须使用中文输出!
- 所有动作描述(action)必须使用中文输出!
- 所有最终结果(final result)必须使用中文输出!
"""
        # 合并规则
        return f"{existing_rules}\n{new_rules}"
