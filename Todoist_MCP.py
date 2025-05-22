# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import logging
import sys
import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

load_dotenv()

# 设置日志记录
logger = logging.getLogger('TodoistTool')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

mcp = FastMCP("TodoistTool")

# TODOIST_API_TOKEN = os.environ.get("TODOIST_API_TOKEN")
TODOIST_API_TOKEN = "..."  # For testing purposes, replace with your actual token

if not TODOIST_API_TOKEN:
    logger.error("Todoist API token not found. Please set TODOIST_API_TOKEN in the .env file")
    api = None
else:
    api = TodoistAPI(TODOIST_API_TOKEN)
    logger.info("Successfully initialized Todoist API")

@mcp.tool()
def add_task(content: str, description: str = "", due_string: str = "", project_id: str = None, priority: int = 1) -> dict:
    """Add a new task to Todoist
    
    Parameters:
        content: Task content
        description: Task description
        due_string: Due date (natural language, e.g., "tomorrow at 3pm", "next Monday")
        project_id: Project ID (optional)
        priority: Priority (1-4, 4 is highest)
        
    Returns:
        Task information
    """
    if not api:
        return {"success": False, "error": "Todoist API not initialized"}
    
    try:
        # 调整参数
        task_args = {
            "content": content
        }
        
        if description:
            task_args["description"] = description
        
        if due_string:
            task_args["due_string"] = due_string
        
        if project_id:
            task_args["project_id"] = project_id
        
        # 验证优先级范围
        if priority and 1 <= priority <= 4:
            task_args["priority"] = priority
        
        logger.info(f"Adding task with parameters: {task_args}")
        task = api.add_task(**task_args)
        
        # 调试信息
        logger.info(f"Task return type: {type(task)}, dir: {dir(task)}")
        
        # 安全地构建返回数据
        task_data = {"success": True, "task": {}}
        
        # 安全地添加属性
        for attr in ["id", "content", "description", "priority"]:
            if hasattr(task, attr):
                task_data["task"][attr] = getattr(task, attr)
        
        # 特殊处理 due 属性
        if hasattr(task, "due") and task.due:
            if hasattr(task.due, "string"):
                task_data["task"]["due"] = task.due.string
            else:
                task_data["task"]["due"] = str(task.due)
        else:
            task_data["task"]["due"] = None
        
        logger.info(f"Task added successfully: {content}")
        return task_data
    except Exception as e:
        import traceback
        error_msg = f"Error adding task: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"success": False, "error": str(e), "details": error_msg}

@mcp.tool()
def get_tasks(project_id: str = None) -> dict:
    """Get Todoist task list
    
    Parameters:
        project_id: Optional project ID, if not provided, get all tasks
        
    Returns:
        Task list
    """
    if not api:
        return {"success": False, "error": "Todoist API not initialized"}
    
    try:
        tasks_result = api.get_tasks(project_id=project_id if project_id else None)
        
        # Convert the result to a list
        tasks_container = list(tasks_result)
        logger.info(f"Tasks container type: {type(tasks_container)}, count: {len(tasks_container)}")
        
        # Extract the actual task list
        if len(tasks_container) == 0:
            # Case when there are no tasks
            task_list = []
        elif isinstance(tasks_container[0], list):
            # If it's a nested list, extract the inner task list
            task_list = tasks_container[0]
            logger.info(f"Found nested list with {len(task_list)} tasks")
        else:
            # If it's not a nested list, use it directly
            task_list = tasks_container
            logger.info(f"Using container directly with {len(task_list)} tasks")
        
        # Process the task list
        processed_tasks = []
        for task in task_list:
            task_data = {}
            
            # Extract common attributes
            for attr in ["id", "content", "priority", "project_id", "description"]:
                if hasattr(task, attr):
                    task_data[attr] = getattr(task, attr)
            
            # Process the nested due attribute
            if hasattr(task, "due") and task.due:
                if hasattr(task.due, "string"):
                    task_data["due"] = task.due.string
                else:
                    task_data["due"] = str(task.due)
            else:
                task_data["due"] = None
            
            processed_tasks.append(task_data)
        
        logger.info(f"Processed {len(processed_tasks)} tasks")
        return {"success": True, "tasks": processed_tasks}
    except Exception as e:
        import traceback
        error_msg = f"Error getting tasks: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"success": False, "error": str(e), "details": error_msg}
    
@mcp.tool()
def complete_task(task_id: str) -> dict:
    """Complete a Todoist task
    
    Parameters:
        task_id: ID of the task to mark as completed
        
    Returns:
        Operation status
    """
    if not api:
        return {"success": False, "error": "Todoist API not initialized"}
    
    try:
        is_success = api.complete_task(task_id=task_id)
        
        if is_success:
            logger.info(f"Completed task ID: {task_id}")
            return {"success": True, "message": f"Task {task_id} has been marked as completed"}
        else:
            logger.error(f"Unable to complete task ID: {task_id}")
            return {"success": False, "error": "Unable to complete task"}
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_projects() -> dict:
    """Get Todoist project list
    
    Returns:
        Project list
    """
    if not api:
        return {"success": False, "error": "Todoist API not initialized"}
    
    try:
        projects = api.get_projects()
        
        project_list = []
        for project in projects:
            project_list.append({
                "id": project.id,
                "name": project.name,
                "color": project.color,
                "is_favorite": project.is_favorite
            })
        
        logger.info(f"Retrieved {len(project_list)} projects")
        return {"success": True, "projects": project_list}
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")