"""
FastAPI REST API - Task Management System
RESTful API with automatic OpenAPI documentation
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uvicorn
from data_store import db

# Pydantic Models for Request/Response validation
class TaskCreate(BaseModel):
    """Model for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, max_length=1000, description="Task description")
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$", description="Task status")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$", description="Task priority")
    category: str = Field(..., min_length=1, max_length=50, description="Task category")
    due_date: str = Field(..., description="Due date in ISO format")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "status": "pending",
                "priority": "high",
                "category": "Development",
                "due_date": "2024-12-31T23:59:59"
            }
        }

class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    due_date: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress",
                "priority": "high"
            }
        }

class TaskResponse(BaseModel):
    """Model for task response"""
    id: int
    title: str
    description: str
    status: str
    priority: str
    category: str
    created_at: str
    due_date: str

class StatsResponse(BaseModel):
    """Model for statistics response"""
    total: int
    completed: int
    in_progress: int
    pending: int
    completion_rate: float

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="RESTful API for managing tasks with full CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Welcome endpoint with API information
    """
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "documentation": "/docs",
        "alternative_docs": "/redoc",
        "endpoints": {
            "tasks": "/tasks",
            "task_by_id": "/tasks/{task_id}",
            "statistics": "/stats"
        }
    }

# Task endpoints
@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
def get_all_tasks():
    """
    Retrieve all tasks from the database
    
    Returns a list of all tasks with their complete information
    """
    return db.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int):
    """
    Retrieve a specific task by ID
    
    - **task_id**: The unique identifier of the task
    """
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate):
    """
    Create a new task
    
    - **title**: Task title (required)
    - **description**: Detailed description (required)
    - **status**: pending, in_progress, or completed (default: pending)
    - **priority**: low, medium, or high (default: medium)
    - **category**: Task category (required)
    - **due_date**: Due date in ISO format (required)
    """
    new_task = db.create_task(task.dict())
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: TaskUpdate):
    """
    Update an existing task
    
    - **task_id**: The unique identifier of the task
    - Provide only the fields you want to update
    """
    # Filter out None values
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )
    
    updated_task = db.update_task(task_id, update_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return updated_task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task by ID
    
    - **task_id**: The unique identifier of the task to delete
    """
    success = db.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return {
        "message": f"Task {task_id} deleted successfully",
        "deleted_id": task_id
    }

# Statistics endpoint
@app.get("/stats", response_model=StatsResponse, tags=["Statistics"])
def get_statistics():
    """
    Get task statistics
    
    Returns counts and completion rate for all tasks
    """
    return db.get_stats()

# Health check endpoint
@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Task Management API"
    }

def run_fastapi():
    """Run FastAPI application"""
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='warning')

if __name__ == '__main__':
    run_fastapi()