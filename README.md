# Flask-FastAPI-Streamlit-NiceGUI-Web-App
Flask builds small apps, FastAPI powers fast APIs, Streamlit makes data dashboards, and NiceGUI creates sleek UIs — all together enabling web apps in your browser.
# 🎯 Task Management System

A comprehensive, industry-grade Python application demonstrating the integration of **Flask**, **FastAPI**, **Streamlit**, and **NiceGUI** into a unified task management system.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Learning Objectives](#learning-objectives)
- [Technologies](#technologies)

## 🌟 Overview

This project showcases best practices for building professional-grade Python applications by integrating four powerful frameworks, each serving a distinct purpose:

- **Flask**: Web-based dashboard with beautiful UI
- **FastAPI**: RESTful API with automatic documentation
- **Streamlit**: Interactive analytics dashboard
- **NiceGUI**: Modern desktop-style interface

## ✨ Features

### Core Functionality
- ✅ **CRUD Operations**: Create, Read, Update, Delete tasks
- 📊 **Real-time Statistics**: Track completion rates and task distribution
- 🔍 **Advanced Filtering**: Filter by status, priority, and category
- 📱 **Responsive Design**: Works across all frameworks
- 💾 **Shared Data Layer**: All services access the same data store

### Framework-Specific Features

#### Flask (Port 5000)
- Beautiful gradient-based UI
- Task cards with hover effects
- Comprehensive statistics dashboard
- Mobile-responsive design

#### FastAPI (Port 8000)
- RESTful API endpoints
- Automatic OpenAPI/Swagger documentation at `/docs`
- ReDoc alternative documentation at `/redoc`
- Pydantic validation
- Comprehensive error handling

#### Streamlit (Port 8501)
- Interactive data filtering
- Real-time metrics
- Expandable task cards
- Category and priority distribution
- Sorting capabilities

#### NiceGUI (Port 8084)
- Modern desktop-style interface
- Tabbed navigation
- Task creation form
- Live filtering
- Beautiful card-based layouts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  run.py                         │
│         (Main Application Launcher)             │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴────────┐
       │  data_store.py │
       │  (Shared Data) │
       └───────┬────────┘
               │
    ┏━━━━━━━━━┻━━━━━━━━━┓
    ┃                    ┃
┌───▼────┐  ┌────▼────┐  ┌────▼─────┐  ┌────▼────┐
│ Flask  │  │ FastAPI │  │Streamlit │  │ NiceGUI │
│:5000   │  │ :8000   │  │ :8501    │  │ :8084   │
└────────┘  └─────────┘  └──────────┘  └─────────┘
```

### Design Patterns Used
- **Singleton Pattern**: Single shared data store
- **Separation of Concerns**: Each framework handles specific responsibilities
- **Thread-based Concurrency**: Parallel execution of services
- **Factory Pattern**: Application creation and configuration

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or create the project directory**
```bash
mkdir task_management_system
cd task_management_system
```

2. **Create all the files** (copy the content from each artifact):
   - `data_store.py`
   - `flask_app.py`
   - `fastapi_app.py`
   - `streamlit_app.py`
   - `nicegui_app.py`
   - `run.py`
   - `requirements.txt`

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Starting the Application

Simply run the main launcher:
```bash
python run.py
```

This single command starts all four services simultaneously!

### Accessing the Services

Once running, access the services at:

| Service | URL | Description |
|---------|-----|-------------|
| Flask | http://localhost:5000 | Web dashboard with task cards |
| FastAPI | http://localhost:8000 | RESTful API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc | Alternative API documentation |
| Streamlit | http://localhost:8501 | Analytics dashboard |
| NiceGUI | http://localhost:8084 | Desktop interface |

### Stopping the Application

Press `Ctrl+C` in the terminal to stop all services gracefully.

## 📁 Project Structure

```
task_management_system/
│
├── data_store.py          # Shared in-memory database
├── flask_app.py           # Flask web dashboard
├── fastapi_app.py         # FastAPI REST API
├── streamlit_app.py       # Streamlit analytics
├── nicegui_app.py         # NiceGUI desktop interface
├── run.py                 # Main application launcher
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

### File Descriptions

- **`data_store.py`**: Centralized data management with sample data generation
- **`flask_app.py`**: HTML template-based web dashboard with CSS styling
- **`fastapi_app.py`**: RESTful API with Pydantic models and OpenAPI docs
- **`streamlit_app.py`**: Interactive dashboard with filters and metrics
- **`nicegui_app.py`**: Modern GUI with tabs and forms
- **`run.py`**: Orchestrates all services using threading

## 🎓 Learning Objectives

This project teaches:

1. **Multi-Framework Integration**: How to combine different Python frameworks
2. **Shared State Management**: Maintaining consistency across services
3. **Threading**: Running multiple services concurrently
4. **REST API Design**: Building professional APIs with FastAPI
5. **Web Development**: Creating responsive UIs with Flask
6. **Data Visualization**: Interactive dashboards with Streamlit
7. **GUI Development**: Modern desktop interfaces with NiceGUI
8. **Code Organization**: Professional project structure
9. **Documentation**: Writing comprehensive docs
10. **Best Practices**: Industry-standard coding patterns

## 🛠️ Technologies

### Core Frameworks
- **Flask 3.0.0**: Micro web framework for Python
- **FastAPI 0.109.0**: Modern API framework with automatic docs
- **Streamlit 1.30.0**: Data app framework
- **NiceGUI 1.4.0**: Python-based GUI framework

### Supporting Libraries
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and settings management

### Python Features Used
- Threading for concurrency
- Type hints for code clarity
- List comprehensions for data processing
- Decorators for routing
- Context managers
- Generator functions

## 📊 Sample Data

The application comes pre-loaded with 15 sample tasks featuring:
- Various priorities (low, medium, high)
- Different statuses (pending, in_progress, completed)
- Multiple categories (Development, Design, Testing, etc.)
- Realistic due dates and timestamps

## 🔧 Customization

### Adding New Tasks
Use any of the interfaces:
- NiceGUI "Create Task" tab
- Streamlit interface
- FastAPI POST endpoint at `/tasks`

### Modifying Data Store
Edit `data_store.py` to:
- Change sample data generation
- Add persistence (database, files)
- Modify data structure

### Styling
- **Flask**: Edit the HTML template in `flask_app.py`
- **Streamlit**: Modify custom CSS in `streamlit_app.py`
- **NiceGUI**: Adjust Tailwind classes in `nicegui_app.py`

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new features
- Improve styling
- Add persistence
- Enhance error handling
- Add authentication

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🙏 Acknowledgments

Built to demonstrate best practices in Python application development and framework integration.

---

**Made with ❤️ for learning and demonstration purposes**




# 2. Open browser to:
http://localhost:5000
