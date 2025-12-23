
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
