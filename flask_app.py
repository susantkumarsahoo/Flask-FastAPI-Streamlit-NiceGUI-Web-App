"""
Flask Web Dashboard - Task Management System
Beautiful web interface with real-time statistics
"""
from flask import Flask, render_template_string, jsonify, request
from data_store import db

app = Flask(__name__)

# HTML Template for Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Management - Flask Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        
        /* Statistics Cards */
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
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stat-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .stat-card h3 { 
            color: #888; 
            font-size: 0.85rem; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.8rem; 
        }
        .stat-card .value { 
            font-size: 2.5rem; 
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Task Grid */
        .tasks-section h2 {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 1.5rem;
        }
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
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
        }
        .task-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        .task-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 1rem; 
        }
        .task-title { 
            font-size: 1.15rem; 
            font-weight: 600; 
            color: #2d3748;
            flex: 1;
            line-height: 1.4;
        }
        .task-description {
            color: #718096;
            line-height: 1.6;
            margin: 1rem 0;
        }
        
        /* Badges */
        .priority { 
            padding: 0.4rem 1rem; 
            border-radius: 25px; 
            font-size: 0.75rem; 
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .priority-high { background: #fed7d7; color: #c53030; }
        .priority-medium { background: #feebc8; color: #dd6b20; }
        .priority-low { background: #e6fffa; color: #319795; }
        
        .status { 
            display: inline-block; 
            padding: 0.5rem 1.2rem; 
            border-radius: 25px; 
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 1rem; 
        }
        .status-completed { background: #c6f6d5; color: #22543d; }
        .status-in_progress { background: #bee3f8; color: #2c5282; }
        .status-pending { background: #fef5e7; color: #975a16; }
        
        .category { 
            display: inline-block; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 0.4rem 1rem; 
            border-radius: 8px; 
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 0.8rem; 
        }
        
        .task-meta { 
            color: #a0aec0; 
            font-size: 0.85rem; 
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .footer {
            text-align: center;
            padding: 3rem 1rem;
            color: #718096;
        }
        
        @media (max-width: 768px) {
            .tasks-grid { grid-template-columns: 1fr; }
            .stats { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Task Management Dashboard</h1>
        <p>Flask-powered Web Interface | Real-time Task Overview</p>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Total Tasks</h3>
                <div class="value">{{ stats.total }}</div>
            </div>
            <div class="stat-card">
                <h3>Completed</h3>
                <div class="value" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {{ stats.completed }}
                </div>
            </div>
            <div class="stat-card">
                <h3>In Progress</h3>
                <div class="value" style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {{ stats.in_progress }}
                </div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="value" style="background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {{ stats.pending }}
                </div>
            </div>
            <div class="stat-card">
                <h3>Completion Rate</h3>
                <div class="value" style="background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {{ stats.completion_rate }}%
                </div>
            </div>
        </div>
        
        <div class="tasks-section">
            <h2>📋 All Tasks</h2>
            <div class="tasks-grid">
                {% for task in tasks %}
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-title">{{ task.title }}</div>
                        <span class="priority priority-{{ task.priority }}">{{ task.priority }}</span>
                    </div>
                    <p class="task-description">{{ task.description }}</p>
                    <span class="category">📁 {{ task.category }}</span>
                    <div class="task-meta">
                        <span>📅 Due: {{ task.due_date[:10] }}</span>
                        <span>•</span>
                        <span>Created: {{ task.created_at[:10] }}</span>
                    </div>
                    <span class="status status-{{ task.status }}">{{ task.status.replace('_', ' ').title() }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Task Management System v1.0 | Powered by Flask</p>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard view"""
    tasks = db.get_all_tasks()
    stats = db.get_stats()
    return render_template_string(DASHBOARD_TEMPLATE, tasks=tasks, stats=stats)

@app.route('/api/tasks')
def get_tasks():
    """API endpoint to get all tasks as JSON"""
    return jsonify(db.get_all_tasks())

@app.route('/api/stats')
def get_stats():
    """API endpoint to get statistics"""
    return jsonify(db.get_stats())

def run_flask():
    """Run Flask application"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_flask()