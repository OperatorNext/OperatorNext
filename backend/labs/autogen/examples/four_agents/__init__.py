"""
四代理协作系统 - 网络检索、代码执行、数据分析的多智能体系统

这个包实现了一个由四个专业代理组成的协作团队：
1. Planner(规划者) - 团队"大脑"，负责协调整个流程
2. BrowserAgent(浏览器代理) - 负责网络浏览和内容检索
3. CodeAgent(代码代理) - 负责代码执行和文件处理
4. AnalystAgent(分析师代理) - 负责数据分析和结果解释

使用方法：
    from labs.autogen.examples.four_agents.team_four_agent import main
    asyncio.run(main())
"""

from .team_four_agent import main

__all__ = ["main"]
