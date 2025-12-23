"""
Task Management System - Data Layer
Shared in-memory database for all frameworks
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DataStore:
    """Centralized data store for task management"""
    
    def __init__(self):
        self.tasks: List[Dict] = []
        self.next_id: int = 1
        self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate random sample tasks for demonstration"""
        statuses = ["pending", "in_progress", "completed"]
        priorities = ["low", "medium", "high"]
        categories = ["Development", "Design", "Testing", "Documentation", "Meeting"]
        
        task_templates = [
            "Implement user authentication module",
            "Design landing page mockups",
            "Write unit tests for API endpoints",
            "Update project documentation",
            "Review pull requests",
            "Fix responsive layout issues",
            "Optimize database queries",
            "Conduct code review session",
            "Prepare sprint planning meeting",
            "Research new technology stack",
            "Deploy application to staging",
            "Configure CI/CD pipeline",
            "Refactor legacy codebase",
            "Create user flow diagrams",
            "Integrate third-party API"
        ]
        
        for i, template in enumerate(task_templates):
            task = {
                "id": self.next_id,
                "title": f"Task {self.next_id}: {template}",
                "description": f"Complete {random.choice(['implementation', 'review', 'testing', 'documentation', 'optimization'])} for {template.lower()}",
                "status": random.choice(statuses),
                "priority": random.choice(priorities),
                "category": random.choice(categories),
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                "due_date": (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat()
            }
            self.tasks.append(task)
            self.next_id += 1
    
    def get_all_tasks(self) -> List[Dict]:
        """Retrieve all tasks"""
        return self.tasks
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a single task by ID"""
        return next((t for t in self.tasks if t["id"] == task_id), None)
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        task = {
            "id": self.next_id,
            "created_at": datetime.now().isoformat(),
            **task_data
        }
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def update_task(self, task_id: int, task_data: Dict) -> Optional[Dict]:
        """Update an existing task"""
        task = self.get_task(task_id)
        if task:
            task.update(task_data)
            return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def get_stats(self) -> Dict:
        """Calculate task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completed"])
        in_progress = len([t for t in self.tasks if t["status"] == "in_progress"])
        pending = len([t for t in self.tasks if t["status"] == "pending"])
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        }

# Global singleton instance
db = DataStore()