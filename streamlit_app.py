"""
Streamlit Analytics Dashboard - Task Management System
Interactive analytics and data visualization
"""
import streamlit as st
from datetime import datetime
from data_store import db

# Page configuration
st.set_page_config(
    page_title="Task Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("📊 Task Management Analytics Dashboard")
    st.markdown("---")
    
    # Fetch data
    tasks = db.get_all_tasks()
    stats = db.get_stats()
    
    # Top Statistics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📋 Total Tasks",
            value=stats["total"],
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ Completed",
            value=stats["completed"],
            delta=f"{stats['completion_rate']}%"
        )
    
    with col3:
        st.metric(
            label="🔄 In Progress",
            value=stats["in_progress"],
            delta=None
        )
    
    with col4:
        st.metric(
            label="⏳ Pending",
            value=stats["pending"],
            delta=None
        )
    
    with col5:
        st.metric(
            label="📈 Completion Rate",
            value=f"{stats['completion_rate']}%",
            delta=None
        )
    
    st.markdown("---")
    
    # Sidebar Filters
    st.sidebar.header("🔍 Filters")
    
    # Status filter
    status_options = ["All"] + list(set(t["status"] for t in tasks))
    selected_status = st.sidebar.selectbox(
        "Filter by Status",
        status_options,
        index=0
    )
    
    # Priority filter
    priority_options = ["All"] + ["low", "medium", "high"]
    selected_priority = st.sidebar.selectbox(
        "Filter by Priority",
        priority_options,
        index=0
    )
    
    # Category filter
    category_options = ["All"] + sorted(list(set(t["category"] for t in tasks)))
    selected_category = st.sidebar.selectbox(
        "Filter by Category",
        category_options,
        index=0
    )
    
    # Sort option
    sort_by = st.sidebar.selectbox(
        "Sort by",
        ["Due Date", "Priority", "Status", "Created Date"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Quick Stats")
    st.sidebar.info(f"""
    **Total Tasks:** {stats['total']}  
    **Completion Rate:** {stats['completion_rate']}%
    """)
    
    # Apply filters
    filtered_tasks = tasks.copy()
    
    if selected_status != "All":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == selected_status]
    
    if selected_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == selected_priority]
    
    if selected_category != "All":
        filtered_tasks = [t for t in filtered_tasks if t["category"] == selected_category]
    
    # Sort tasks
    if sort_by == "Due Date":
        filtered_tasks.sort(key=lambda x: x["due_date"])
    elif sort_by == "Priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        filtered_tasks.sort(key=lambda x: priority_order.get(x["priority"], 3))
    elif sort_by == "Status":
        filtered_tasks.sort(key=lambda x: x["status"])
    elif sort_by == "Created Date":
        filtered_tasks.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Display filtered count
    st.subheader(f"📋 Tasks ({len(filtered_tasks)} found)")
    
    if not filtered_tasks:
        st.warning("No tasks found matching the selected filters.")
    else:
        # Display tasks in expandable cards
        for i, task in enumerate(filtered_tasks):
            # Determine status emoji and color
            status_emoji = {
                "completed": "✅",
                "in_progress": "🔄",
                "pending": "⏳"
            }.get(task["status"], "📌")
            
            priority_emoji = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(task["priority"], "⚪")
            
            # Create expandable section
            with st.expander(f"{status_emoji} {task['title']} {priority_emoji}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:**")
                    st.write(task['description'])
                    
                    st.markdown(f"**Category:** `{task['category']}`")
                    
                with col2:
                    st.markdown(f"**Priority:** `{task['priority'].upper()}`")
                    st.markdown(f"**Status:** `{task['status'].replace('_', ' ').title()}`")
                    
                    # Dates
                    created = datetime.fromisoformat(task['created_at'])
                    due = datetime.fromisoformat(task['due_date'])
                    
                    st.markdown(f"**Created:** {created.strftime('%Y-%m-%d')}")
                    st.markdown(f"**Due Date:** {due.strftime('%Y-%m-%d')}")
                    
                    # Days until due
                    days_left = (due - datetime.now()).days
                    if days_left < 0:
                        st.error(f"⚠️ Overdue by {abs(days_left)} days")
                    elif days_left == 0:
                        st.warning("⚠️ Due today!")
                    elif days_left <= 3:
                        st.warning(f"⚠️ Due in {days_left} days")
                    else:
                        st.info(f"📅 {days_left} days remaining")
    
    # Category Distribution
    st.markdown("---")
    st.subheader("📊 Category Distribution")
    
    if tasks:
        category_counts = {}
        for task in tasks:
            cat = task["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Display as columns
        cols = st.columns(len(category_counts))
        for idx, (category, count) in enumerate(category_counts.items()):
            with cols[idx]:
                st.metric(label=category, value=count)
    
    # Priority Distribution
    st.markdown("---")
    st.subheader("🎯 Priority Distribution")
    
    col1, col2, col3 = st.columns(3)
    
    high_priority = len([t for t in tasks if t["priority"] == "high"])
    medium_priority = len([t for t in tasks if t["priority"] == "medium"])
    low_priority = len([t for t in tasks if t["priority"] == "low"])
    
    with col1:
        st.metric("🔴 High Priority", high_priority)
    with col2:
        st.metric("🟡 Medium Priority", medium_priority)
    with col3:
        st.metric("🟢 Low Priority", low_priority)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #888;'>
            <p>Task Management System v1.0 | Powered by Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()