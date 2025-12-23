"""
Task Management System - Complete All-in-One Application
Single file containing Flask, FastAPI, Streamlit, and NiceGUI
Run with: python mainrun.py
"""

# ============================================================================
# IMPORTS
# ============================================================================
import threading
import time
import sys
import subprocess
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Flask imports
from flask import Flask, render_template_string, jsonify

# FastAPI imports
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

# NiceGUI imports
from nicegui import ui

# ============================================================================
# DATA STORE - Shared Database
# ============================================================================
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
        return self.tasks
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        return next((t for t in self.tasks if t["id"] == task_id), None)
    
    def create_task(self, task_data: Dict) -> Dict:
        task = {
            "id": self.next_id,
            "created_at": datetime.now().isoformat(),
            **task_data
        }
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def update_task(self, task_id: int, task_data: Dict) -> Optional[Dict]:
        task = self.get_task(task_id)
        if task:
            task.update(task_data)
            return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def get_stats(self) -> Dict:
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

# Global database instance
db = DataStore()

# ============================================================================
# FLASK APPLICATION
# ============================================================================
flask_app = Flask(__name__)

FLASK_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Management - Flask Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 3rem 2rem; 
            text-align: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .container { max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 1.5rem; 
            margin-bottom: 3rem; 
        }
        .stat-card { 
            background: white; 
            padding: 2rem 1.5rem; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .stat-card h3 { color: #888; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin-bottom: 0.8rem; }
        .stat-card .value { font-size: 2.5rem; font-weight: 700; color: #667eea; }
        .tasks-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); 
            gap: 2rem; 
        }
        .task-card { 
            background: white; 
            padding: 2rem; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
            border-left: 5px solid #667eea;
        }
        .task-card:hover { transform: translateY(-8px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
        .task-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
        .task-title { font-size: 1.15rem; font-weight: 600; color: #2d3748; flex: 1; }
        .task-description { color: #718096; line-height: 1.6; margin: 1rem 0; }
        .priority { padding: 0.4rem 1rem; border-radius: 25px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
        .priority-high { background: #fed7d7; color: #c53030; }
        .priority-medium { background: #feebc8; color: #dd6b20; }
        .priority-low { background: #e6fffa; color: #319795; }
        .status { display: inline-block; padding: 0.5rem 1.2rem; border-radius: 25px; font-size: 0.85rem; font-weight: 600; margin-top: 1rem; }
        .status-completed { background: #c6f6d5; color: #22543d; }
        .status-in_progress { background: #bee3f8; color: #2c5282; }
        .status-pending { background: #fef5e7; color: #975a16; }
        .category { display: inline-block; background: #667eea; color: white; padding: 0.4rem 1rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; margin-top: 0.8rem; }
        .task-meta { color: #a0aec0; font-size: 0.85rem; margin-top: 1rem; }
        @media (max-width: 768px) { .tasks-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Task Management Dashboard</h1>
        <p>Flask-powered Web Interface</p>
    </div>
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Total Tasks</h3>
                <div class="value">{{ stats.total }}</div>
            </div>
            <div class="stat-card">
                <h3>Completed</h3>
                <div class="value" style="color: #48bb78;">{{ stats.completed }}</div>
            </div>
            <div class="stat-card">
                <h3>In Progress</h3>
                <div class="value" style="color: #4299e1;">{{ stats.in_progress }}</div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="value" style="color: #ed8936;">{{ stats.pending }}</div>
            </div>
            <div class="stat-card">
                <h3>Completion Rate</h3>
                <div class="value" style="color: #9f7aea;">{{ stats.completion_rate }}%</div>
            </div>
        </div>
        <div class="tasks-grid">
            {% for task in tasks %}
            <div class="task-card">
                <div class="task-header">
                    <div class="task-title">{{ task.title }}</div>
                    <span class="priority priority-{{ task.priority }}">{{ task.priority }}</span>
                </div>
                <p class="task-description">{{ task.description }}</p>
                <span class="category">📁 {{ task.category }}</span>
                <div class="task-meta">📅 Due: {{ task.due_date[:10] }} • Created: {{ task.created_at[:10] }}</div>
                <span class="status status-{{ task.status }}">{{ task.status.replace('_', ' ').title() }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

UNIFIED_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Management - Unified Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: white; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); position: sticky; top: 0; z-index: 1000; }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .nav-tabs { display: flex; justify-content: center; gap: 1rem; padding: 1.5rem; background: #16213e; flex-wrap: wrap; }
        .tab-btn { padding: 1rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; border-radius: 10px; color: white; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; min-width: 180px; }
        .tab-btn:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5); }
        .tab-btn.active { background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); }
        .content { padding: 2rem; }
        .iframe-container { display: none; width: 100%; height: calc(100vh - 240px); background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
        .iframe-container.active { display: block; }
        iframe { width: 100%; height: 100%; border: none; }
        .status-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #16213e; padding: 1rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; }
        .status-item { display: flex; align-items: center; gap: 0.5rem; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; background: #48bb78; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Task Management System</h1>
        <p>Unified Dashboard - All Services in One Place</p>
    </div>
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('flask')">🌐 Flask Dashboard</button>
        <button class="tab-btn" onclick="switchTab('fastapi')">⚡ FastAPI Docs</button>
        <button class="tab-btn" onclick="switchTab('streamlit')">📊 Streamlit Analytics</button>
        <button class="tab-btn" onclick="switchTab('nicegui')">🖥️ NiceGUI Interface</button>
    </div>
    <div class="content">
        <div id="flask" class="iframe-container active">
            <iframe src="http://localhost:5000/dashboard"></iframe>
        </div>
        <div id="fastapi" class="iframe-container">
            <iframe src="http://localhost:8000/docs"></iframe>
        </div>
        <div id="streamlit" class="iframe-container">
            <iframe src="http://localhost:8501"></iframe>
        </div>
        <div id="nicegui" class="iframe-container">
            <iframe src="http://localhost:8084"></iframe>
        </div>
    </div>
    <div class="status-bar">
        <div class="status-item"><div class="status-dot"></div>Flask (5000)</div>
        <div class="status-item"><div class="status-dot"></div>FastAPI (8000)</div>
        <div class="status-item"><div class="status-dot"></div>Streamlit (8501)</div>
        <div class="status-item"><div class="status-dot"></div>NiceGUI (8084)</div>
    </div>
    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.iframe-container').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
"""

@flask_app.route('/')
def unified():
    return render_template_string(UNIFIED_DASHBOARD)

@flask_app.route('/dashboard')
def dashboard():
    tasks = db.get_all_tasks()
    stats = db.get_stats()
    return render_template_string(FLASK_TEMPLATE, tasks=tasks, stats=stats)

@flask_app.route('/api/tasks')
def get_tasks():
    return jsonify(db.get_all_tasks())

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================
fastapi_app = FastAPI(title="Task Management API", version="1.0.0")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    category: str = Field(..., min_length=1, max_length=50)
    due_date: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[str] = None

@fastapi_app.get("/")
def read_root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@fastapi_app.get("/tasks")
def get_all_tasks():
    return db.get_all_tasks()

@fastapi_app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@fastapi_app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    return db.create_task(task.dict())

@fastapi_app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    updated = db.update_task(task_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@fastapi_app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if not db.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@fastapi_app.get("/stats")
def get_statistics():
    return db.get_stats()

def run_fastapi():
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8000, log_level='warning')

# ============================================================================
# STREAMLIT APPLICATION
# ============================================================================
def create_streamlit_script():
    """Create temporary Streamlit script"""
    streamlit_code = '''
import streamlit as st
from datetime import datetime
import sys
sys.path.insert(0, ".")

# Import from main script
if __name__ == "__main__":
    from mainrun import db
else:
    from __main__ import db

st.set_page_config(page_title="Task Analytics", page_icon="📊", layout="wide")

st.title("📊 Task Management Analytics Dashboard")
st.markdown("---")

stats = db.get_stats()
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📋 Total Tasks", stats["total"])
with col2:
    st.metric("✅ Completed", stats["completed"], f"{stats['completion_rate']}%")
with col3:
    st.metric("🔄 In Progress", stats["in_progress"])
with col4:
    st.metric("⏳ Pending", stats["pending"])
with col5:
    st.metric("📈 Completion Rate", f"{stats['completion_rate']}%")

st.markdown("---")

tasks = db.get_all_tasks()

col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.selectbox("Filter by Status", ["All", "pending", "in_progress", "completed"])
with col2:
    priority_filter = st.selectbox("Filter by Priority", ["All", "low", "medium", "high"])
with col3:
    category_filter = st.selectbox("Filter by Category", ["All"] + list(set(t["category"] for t in tasks)))

filtered_tasks = tasks
if status_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
if priority_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]
if category_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["category"] == category_filter]

st.subheader(f"📋 Tasks ({len(filtered_tasks)} found)")

for task in filtered_tasks:
    status_emoji = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}.get(task["status"], "📌")
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
    
    with st.expander(f"{status_emoji} {task['title']} {priority_emoji}"):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Description:** {task['description']}")
            st.markdown(f"**Category:** `{task['category']}`")
        with col2:
            st.markdown(f"**Priority:** `{task['priority'].upper()}`")
            st.markdown(f"**Status:** `{task['status'].replace('_', ' ').title()}`")
            st.markdown(f"**Due Date:** {task['due_date'][:10]}")
'''
    
    with open('_streamlit_app.py', 'w', encoding='utf-8') as f:
        f.write(streamlit_code)

def run_streamlit():
    create_streamlit_script()
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        '_streamlit_app.py',
        '--server.port', '8501',
        '--server.headless', 'true'
    ])

# ============================================================================
# NICEGUI APPLICATION
# ============================================================================
def run_nicegui():
    ui.colors(primary='#667eea', secondary='#764ba2', accent='#48bb78')
    
    def main_page():
        with ui.header(elevated=True).classes('items-center justify-between px-8 py-4'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('task_alt', size='lg').classes('text-white')
                ui.label('Task Management System').classes('text-h4 text-white font-bold')
            ui.label('NiceGUI Desktop Interface').classes('text-subtitle1 text-white opacity-80')
        
        with ui.column().classes('w-full p-8 gap-6'):
            stats = db.get_stats()
            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-blue-500 to-purple-600'):
                    ui.label('Total Tasks').classes('text-white text-sm opacity-80')
                    ui.label(str(stats['total'])).classes('text-white text-4xl font-bold mt-2')
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-green-500 to-teal-600'):
                    ui.label('Completed').classes('text-white text-sm opacity-80')
                    ui.label(str(stats['completed'])).classes('text-white text-4xl font-bold mt-2')
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-blue-400 to-cyan-600'):
                    ui.label('In Progress').classes('text-white text-sm opacity-80')
                    ui.label(str(stats['in_progress'])).classes('text-white text-4xl font-bold mt-2')
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-yellow-500 to-orange-600'):
                    ui.label('Pending').classes('text-white text-sm opacity-80')
                    ui.label(str(stats['pending'])).classes('text-white text-4xl font-bold mt-2')
            
            with ui.tabs().classes('w-full') as tabs:
                tasks_tab = ui.tab('📋 Tasks', icon='list')
                create_tab = ui.tab('➕ Create', icon='add')
            
            with ui.tab_panels(tabs, value=tasks_tab).classes('w-full'):
                with ui.tab_panel(tasks_tab):
                    ui.label('All Tasks').classes('text-h5 font-bold mb-4')
                    tasks = db.get_all_tasks()
                    with ui.grid(columns=3).classes('w-full gap-4'):
                        for task in tasks:
                            with ui.card().classes('p-6'):
                                with ui.row().classes('w-full items-start justify-between mb-2'):
                                    ui.label(task['title']).classes('text-lg font-bold flex-1')
                                    priority_colors = {'high': 'bg-red-500', 'medium': 'bg-yellow-500', 'low': 'bg-green-500'}
                                    with ui.badge(task['priority'].upper()).classes(f"{priority_colors.get(task['priority'])} text-white px-3 py-1"):
                                        pass
                                ui.label(task['description']).classes('text-sm text-gray-600 mb-3')
                                ui.label(f"📅 Due: {task['due_date'][:10]}").classes('text-xs text-gray-500')
                                status_colors = {'completed': 'bg-green-500', 'in_progress': 'bg-blue-500', 'pending': 'bg-yellow-500'}
                                with ui.badge(task['status'].replace('_', ' ').title()).classes(f"{status_colors.get(task['status'])} text-white px-4 py-2 mt-2 w-full text-center"):
                                    pass
                
                with ui.tab_panel(create_tab):
                    ui.label('Create New Task').classes('text-h5 font-bold mb-4')
                    with ui.card().classes('p-8 max-w-3xl'):
                        title_input = ui.input('Title', placeholder='Enter task title').classes('w-full')
                        desc_input = ui.textarea('Description', placeholder='Task description').classes('w-full')
                        with ui.row().classes('w-full gap-4'):
                            priority_select = ui.select(['low', 'medium', 'high'], label='Priority', value='medium').classes('flex-1')
                            category_input = ui.input('Category', placeholder='e.g., Development').classes('flex-1')
                        due_date_input = ui.input('Due Date (YYYY-MM-DD)', placeholder='2024-12-31').classes('w-full')
                        
                        def create_new_task():
                            if not all([title_input.value, desc_input.value, category_input.value, due_date_input.value]):
                                ui.notify('Please fill all fields', color='negative')
                                return
                            db.create_task({
                                'title': title_input.value,
                                'description': desc_input.value,
                                'priority': priority_select.value,
                                'category': category_input.value,
                                'status': 'pending',
                                'due_date': due_date_input.value + 'T00:00:00'
                            })
                            ui.notify('✅ Task created!', color='positive')
                            title_input.value = ''
                            desc_input.value = ''
                            category_input.value = ''
                            due_date_input.value = ''
                        
                        ui.button('Create Task', on_click=create_new_task, color='primary').classes('mt-4')
    
    # Call the page function directly (no decorator needed)
    main_page()
    ui.run(port=8084, reload=False, show=False, title='Task Management System')

# ============================================================================
# MAIN LAUNCHER
# ============================================================================
def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║           TASK MANAGEMENT SYSTEM - ALL SERVICES                    ║
    ║                                                                    ║
    ║  Complete Python Application Integration:                         ║
    ║  • Flask      - Web Dashboard                                      ║
    ║  • FastAPI    - RESTful API                                        ║
    ║  • Streamlit  - Analytics Dashboard                                ║
    ║  • NiceGUI    - Desktop Interface                                  ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    print("\n🚀 Starting all services...\n")
    
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True, name="Flask-Thread")
    flask_thread.start()
    time.sleep(1)
    print("✅ Flask Dashboard:      http://localhost:5000")
    
    # Start FastAPI
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True, name="FastAPI-Thread")
    fastapi_thread.start()
    time.sleep(1)
    print("✅ FastAPI:              http://localhost:8000")
    print("   📚 API Documentation:  http://localhost:8000/docs")
    
    # Start Streamlit
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True, name="Streamlit-Thread")
    streamlit_thread.start()
    time.sleep(2)
    print("✅ Streamlit Analytics:  http://localhost:8501")
    
    time.sleep(1)
    print("✅ NiceGUI Interface:    http://localhost:8084")
    
    print("\n" + "="*70)
    print("🎉 ALL SERVICES ARE NOW RUNNING!")
    print("="*70)
    print("\n💡 All services share the same in-memory database")
    print("⚠️  Press Ctrl+C to stop all services\n")
    
    try:
        run_nicegui()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        print("✅ All services stopped successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()




# python mainrun.py