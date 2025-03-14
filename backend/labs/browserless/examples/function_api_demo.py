"""
Browserless Function API 示例

本示例实现多种方式调用函数API的方法：
1. 基本用法 - 生成随机数并访问示例网站
2. 导入库 - 使用faker库生成随机数据
3. JSON API - 使用JSON格式发送代码和上下文
4. 自适应格式 - 使用优化方法自动选择最佳格式
"""

import asyncio
import json
import sys
from pathlib import Path

import requests

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from labs.browserless.config import (
    check_browserless_status,
    get_browserless_token,
    get_browserless_url,
    print_status_info,
)
from labs.browserless.utils import HTTPBrowserlessClient


def get_function_api_url():
    """获取Function API的URL"""
    base_url = get_browserless_url()
    token = get_browserless_token()
    return f"{base_url}/function?token={token}"


async def example_1_basic_usage():
    """
    示例1: 基本用法 - 使用原始HTTP请求访问API
    """
    print("\n" + "=" * 60)
    print("🔍 示例1: 基本用法 - 生成随机数并访问示例网站")
    print("=" * 60)

    try:
        # 获取API URL和Token
        TOKEN = get_browserless_token()
        url = f"{get_browserless_url()}/function?token={TOKEN}&sourceType=module"

        # 使用 Content-Type: application/javascript
        headers = {"Content-Type": "application/javascript"}

        # 完全按照官方文档格式的ESM代码
        code = """
export default async function ({ page }) {
  const rndNumber = () => {
    return Math.floor(Math.random() * (10**6 - 0));
  };

  await page.goto("https://example.com/");
  const url = await page.title();
  const numbers = Array.from({length: 5}, () => rndNumber());

  return {
    data: {
      url,
      numbers,
    },
    type: "application/json",
  };
}
"""
        print("📤 发送请求到Function API...")
        response = requests.post(url, headers=headers, data=code)

        # 检查响应
        if response.status_code != 200:
            print(f"❌ ESM格式请求失败: {response.status_code} - {response.text}")

            # 尝试使用传统CommonJS格式，不包含sourceType=module参数
            print("\n📤 尝试使用传统CommonJS格式...")

            # 重新定义URL，不包含sourceType=module
            commonjs_url = f"{get_browserless_url()}/function?token={TOKEN}"

            # 使用application/javascript内容类型
            headers = {"Content-Type": "application/javascript"}

            # 传统CommonJS格式的代码
            commonjs_code = """
function handler({ page }) {
  const rndNumber = () => {
    return Math.floor(Math.random() * (10**6 - 0));
  };

  return page.goto("https://example.com/")
    .then(() => page.title())
    .then(title => {
      const numbers = Array.from({length: 5}, () => rndNumber());
      
      return {
        data: {
          url: title,
          numbers: numbers,
        },
        type: "application/json"
      };
    });
}
"""
            response = requests.post(commonjs_url, headers=headers, data=commonjs_code)

            if response.status_code != 200:
                print(f"❌ CommonJS也失败: {response.status_code} - {response.text}")
                return
            else:
                print("✅ CommonJS格式请求成功!")
        else:
            print("✅ ESM格式请求成功!")

        # 解析并输出结果
        try:
            result = response.json()
            print("\n📋 结果:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ 解析响应失败: {str(e)}")
            print(f"响应内容: {response.text[:200]}...")

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")


async def example_2_importing_libraries():
    """
    示例2: 导入库 - 使用faker库生成随机数据
    """
    print("\n" + "=" * 60)
    print("🔍 示例2: 导入库 - 使用faker库生成随机数据")
    print("=" * 60)

    try:
        # 获取API URL和Token
        TOKEN = get_browserless_token()
        url = f"{get_browserless_url()}/function?token={TOKEN}&sourceType=module"

        # 使用 Content-Type: application/javascript
        headers = {"Content-Type": "application/javascript"}

        # ESM模块代码，使用esm.sh提供的CDN
        esm_code = """
import { faker } from "https://esm.sh/@faker-js/faker";

export default async function () {
  const Internet = faker.internet;
  const rndData = [...Array(5)].map(() => ({
    domain: Internet.domainName(),
    ip: Internet.ip(),
    mac: Internet.mac(),
    protocol: Internet.protocol(),
  }));

  return {
    data: { domains: rndData },
    type: "application/json",
  };
}
"""

        print("📤 发送ESM格式请求...")
        response = requests.post(url, headers=headers, data=esm_code)

        # 检查响应
        if response.status_code != 200:
            print(f"❌ ESM执行失败: {response.status_code} - {response.text}")

            # 尝试直接在容器中使用安装的模块
            print("\n📤 尝试使用容器内安装的模块...")

            # 修改ESM代码，使用require方式
            commonjs_url = f"{get_browserless_url()}/function?token={TOKEN}"
            commonjs_code = """
function handler() {
  const faker = require('@faker-js/faker').faker;
  
  const Internet = faker.internet;
  const rndData = Array.from({length: 5}, () => ({
    domain: Internet.domainName(),
    ip: Internet.ip(),
    mac: Internet.mac(),
    protocol: Internet.protocol(),
  }));

  return {
    data: { domains: rndData },
    type: "application/json",
  };
}
"""
            response = requests.post(commonjs_url, headers=headers, data=commonjs_code)

            if response.status_code != 200:
                print(
                    f"❌ 容器内模块加载也失败: {response.status_code} - {response.text}"
                )
                return
            else:
                print("✅ 容器内模块加载成功!")
        else:
            print("✅ ESM模块加载成功!")

        # 解析并输出结果
        try:
            result = response.json()
            print("\n📋 结果:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ 解析响应失败: {str(e)}")
            print(f"响应内容: {response.text[:200]}...")

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")


async def example_3_json_api():
    """
    示例3: JSON API - 使用utils.py中的HTTPBrowserlessClient
    """
    print("\n" + "=" * 60)
    print("🔍 示例3: JSON API - 使用JSON格式发送代码和上下文")
    print("=" * 60)

    try:
        # 创建HTTP客户端
        client = HTTPBrowserlessClient()
        await client.connect()

        # 压缩的代码和上下文
        code = """
function handler(args) {
  // 访问上下文对象
  const len = args.context.len || 5;
  
  // 生成随机域名数据
  function generateDomainData() {
    return {
      domain: 'example-' + Math.random().toString(36).substring(2, 8) + '.com',
      ip: '192.168.1.' + Math.floor(Math.random() * 255),
      mac: Array.from({length: 6}, () => Math.floor(Math.random() * 256).toString(16).padStart(2, '0')).join(':'),
      protocol: ['http', 'https', 'ftp', 'ssh'][Math.floor(Math.random() * 4)]
    };
  }
  
  // 生成指定数量的随机数据
  const domains = Array.from({length: len}, () => generateDomainData());
  
  return {
    data: {
      domains: domains,
      length: len
    },
    type: 'application/json'
  };
}
"""
        context = {"len": 10}

        print("📤 使用execute_function发送请求...")
        result = await client.execute_function(code, context)
        print("✅ 请求成功!")
        print("\n📋 结果:")
        print(json.dumps(result, indent=2))

        await client.close()

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")


async def example_4_optimal_format():
    """
    示例4: 自适应格式 - 使用新增的自适应方法自动选择最佳格式
    """
    print("\n" + "=" * 60)
    print("🔍 示例4: 自适应格式 - 使用智能方法处理不同类型的代码")
    print("=" * 60)

    try:
        # 创建HTTP客户端
        client = HTTPBrowserlessClient()
        await client.connect()

        # 1. ESM 格式代码
        esm_code = """
export default async function({ page }) {
  // 访问网页
  await page.goto('https://example.com');
  
  // 获取页面信息
  const title = await page.title();
  const url = page.url();
  
  // 获取页面内容
  const content = await page.content();
  const textContent = await page.evaluate(() => document.body.textContent);
  
  // 返回数据
  return {
    data: {
      title,
      url,
      contentLength: content.length,
      textLength: textContent.length,
      timestamp: new Date().toISOString()
    },
    type: 'application/json'
  };
}
"""

        print("📤 使用execute_function_with_optimal_format发送ESM格式代码请求...")
        try:
            result = await client.execute_function_with_optimal_format(esm_code)
            print("✅ 自适应执行成功!")
            print("\n📋 结果:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ 自适应执行失败: {str(e)}")

        # 2. 传统格式代码
        traditional_code = """
function handler(args) {
  const page = args.page;
  
  // 生成随机ID
  const generateId = () => Math.random().toString(36).substring(2, 15);
  
  // 返回一些随机生成的数据
  return {
    data: {
      id: generateId(),
      numbers: Array.from({length: 5}, () => Math.floor(Math.random() * 100)),
      timestamp: new Date().toISOString()
    },
    type: 'application/json'
  };
}
"""

        print("\n📤 使用execute_function_with_optimal_format发送传统格式代码请求...")
        try:
            result = await client.execute_function_with_optimal_format(traditional_code)
            print("✅ 自适应执行成功!")
            print("\n📋 结果:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ 自适应执行失败: {str(e)}")

        await client.close()

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")


async def run_demos():
    """运行所有示例"""
    # 检查Browserless服务状态
    success, metrics = await check_browserless_status()
    if not success:
        print("❌ Browserless服务未启动或不可用")
        return

    print("🌟 Browserless Function API 演示程序")
    print("=" * 60)

    # 打印服务状态
    if metrics:
        print_status_info(metrics)

    # 运行所有示例
    await example_1_basic_usage()
    await example_2_importing_libraries()
    await example_3_json_api()
    await example_4_optimal_format()

    print("\n" + "=" * 60)
    print("🏁 演示结束")


if __name__ == "__main__":
    asyncio.run(run_demos())
