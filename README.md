# XiaozhiMCP-MapNAVI | MCP地图导航工具

A powerful MCP tool that integrates with Amap API services, allowing AI to access geographic information, weather data, and route planning.

一个强大的MCP工具，集成了高德地图API服务，使AI能够访问地理信息、天气数据和路线规划。
![image](https://github.com/user-attachments/assets/2a8f95c0-f69e-4da8-b059-c04faaa9250a)
![image](https://github.com/user-attachments/assets/62974a24-02fc-4efe-948d-30c8edab707a)

## Overview | 概述

MCP-MapNAVI is based on the Model Context Protocol (MCP), which allows AI language models to interact with external map services. Through this tool, AI can geocode addresses, check weather information, and plan driving routes - extending its capabilities beyond text generation.

MCP-MapNAVI基于模型上下文协议(MCP)，允许AI语言模型与外部地图服务交互。通过这个工具，AI可以进行地理编码、查询天气信息和规划驾驶路线 - 将其能力扩展到文本生成之外。

## Features | 特性

- 🗺️ **地理编码** - 将地址转换为经纬度坐标
- 🌤️ **天气查询** - 获取特定城市或地区的天气信息
- 🚗 **驾车路线规划** - 规划两点之间的驾驶路线
- 🔄 **自动重连** - 具有指数退避的WebSocket连接恢复机制
- 🔒 **安全通信** - 通过WebSocket的安全数据传输

## Quick Start | 快速开始

1. Install dependencies | 安装依赖:
```bash
pip install -r requirements.txt
```

2. Set up environment variables | 设置环境变量:
```bash
export MCP_ENDPOINT=<your_mcp_endpoint>
```

3. Run the map_navi example :
```bash
python mcp_pipe.py map.py
```

## Project Structure | 项目结构

- `mcp_pipe.py`: Main communication pipe that handles WebSocket connections and process management | 处理WebSocket连接和进程管理的主通信管道
- `calculator.py`: Example MCP tool implementation for mathematical calculations | 用于数学计算的MCP工具示例实现
- `requirements.txt`: Project dependencies | 项目依赖

## Creating Your Own MCP Tools | 创建自己的MCP工具

Here's a simple example of creating an MCP tool | 以下是一个创建MCP工具的简单示例:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("YourToolName")

@mcp.tool()
def your_tool(parameter: str) -> dict:
    """Tool description here"""
    # Your implementation
    return {"success": True, "result": result}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Use Cases | 使用场景

- Mathematical calculations | 数学计算
- Email operations | 邮件操作
- Knowledge base search | 知识库搜索
- Remote device control | 远程设备控制
- Data processing | 数据处理
- Custom tool integration | 自定义工具集成

## Requirements | 环境要求

- Python 3.7+
- websockets>=11.0.3
- python-dotenv>=1.0.0
- mcp>=1.8.1
- pydantic>=2.11.4

## Contributing | 贡献指南

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。

## License | 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详情请查看LICENSE文件。

## Acknowledgments | 致谢

- Thanks to all contributors who have helped shape this project | 感谢所有帮助塑造这个项目的贡献者
- Inspired by the need for extensible AI capabilities | 灵感来源于对可扩展AI能力的需求
