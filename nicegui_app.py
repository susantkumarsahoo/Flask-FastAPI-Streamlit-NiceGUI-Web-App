"""
NiceGUI Desktop Interface - Task Management System
Modern desktop-style GUI application
"""
from nicegui import ui
from datetime import datetime
from data_store import db

def run_nicegui():
    """Run NiceGUI application"""
    
    # Set color scheme
    ui.colors(primary='#667eea', secondary='#764ba2', accent='#48bb78')
    
    @ui.page('/')
    def main_page():
        """Main page with tabbed interface"""
        
        # Header
        with ui.header(elevated=True).classes('items-center justify-between px-8 py-4'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('task_alt', size='lg').classes('text-white')
                ui.label('Task Management System').classes('text-h4 text-white font-bold')
            ui.label('NiceGUI Desktop Interface').classes('text-subtitle1 text-white opacity-80')
        
        # Main container
        with ui.column().classes('w-full p-8 gap-6'):
            
            # Statistics Cards at the top
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
                
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-purple-500 to-pink-600'):
                    ui.label('Completion Rate').classes('text-white text-sm opacity-80')
                    ui.label(f"{stats['completion_rate']}%").classes('text-white text-4xl font-bold mt-2')
            
            # Tabs for different sections
            with ui.tabs().classes('w-full') as tabs:
                tasks_tab = ui.tab('📋 All Tasks', icon='list')
                create_tab = ui.tab('➕ Create Task', icon='add_circle')
                filter_tab = ui.tab('🔍 Filter & Search', icon='filter_list')
            
            with ui.tab_panels(tabs, value=tasks_tab).classes('w-full'):
                
                # ===== TASKS TAB =====
                with ui.tab_panel(tasks_tab):
                    ui.label('All Tasks').classes('text-h5 font-bold mb-4')
                    
                    tasks = db.get_all_tasks()
                    
                    with ui.grid(columns=3).classes('w-full gap-4'):
                        for task in tasks:
                            with ui.card().classes('p-6 hover:shadow-2xl transition-shadow'):
                                # Task header
                                with ui.row().classes('w-full items-start justify-between mb-4'):
                                    ui.label(task['title']).classes('text-lg font-bold flex-1')
                                    
                                    # Priority badge
                                    priority_colors = {
                                        'high': 'bg-red-500',
                                        'medium': 'bg-yellow-500',
                                        'low': 'bg-green-500'
                                    }
                                    with ui.badge(task['priority'].upper()).classes(
                                        f"{priority_colors.get(task['priority'], 'bg-gray-500')} text-white px-3 py-1"
                                    ):
                                        pass
                                
                                # Description
                                ui.label(task['description']).classes('text-sm text-gray-600 mb-3')
                                
                                # Category badge
                                with ui.badge(f"📁 {task['category']}").classes('bg-purple-600 text-white px-3 py-1'):
                                    pass
                                
                                # Metadata
                                ui.separator().classes('my-3')
                                
                                with ui.row().classes('w-full justify-between text-xs text-gray-500'):
                                    ui.label(f"📅 Due: {task['due_date'][:10]}")
                                    ui.label(f"Created: {task['created_at'][:10]}")
                                
                                # Status badge
                                status_colors = {
                                    'completed': 'bg-green-500',
                                    'in_progress': 'bg-blue-500',
                                    'pending': 'bg-yellow-500'
                                }
                                with ui.badge(task['status'].replace('_', ' ').title()).classes(
                                    f"{status_colors.get(task['status'], 'bg-gray-500')} text-white px-4 py-2 mt-3 w-full text-center"
                                ):
                                    pass
                
                # ===== CREATE TASK TAB =====
                with ui.tab_panel(create_tab):
                    ui.label('Create New Task').classes('text-h5 font-bold mb-4')
                    
                    with ui.card().classes('p-8 max-w-3xl'):
                        with ui.column().classes('w-full gap-4'):
                            # Form fields
                            title_input = ui.input('Task Title', placeholder='Enter a descriptive title').classes('w-full')
                            title_input.props('outlined')
                            
                            desc_input = ui.textarea('Description', placeholder='Provide detailed description of the task').classes('w-full')
                            desc_input.props('outlined')
                            
                            with ui.row().classes('w-full gap-4'):
                                priority_select = ui.select(
                                    ['low', 'medium', 'high'],
                                    label='Priority',
                                    value='medium'
                                ).classes('flex-1')
                                priority_select.props('outlined')
                                
                                status_select = ui.select(
                                    ['pending', 'in_progress', 'completed'],
                                    label='Status',
                                    value='pending'
                                ).classes('flex-1')
                                status_select.props('outlined')
                            
                            with ui.row().classes('w-full gap-4'):
                                category_input = ui.input('Category', placeholder='e.g., Development, Design').classes('flex-1')
                                category_input.props('outlined')
                                
                                due_date_input = ui.input('Due Date', placeholder='YYYY-MM-DD').classes('flex-1')
                                due_date_input.props('outlined type=date')
                            
                            ui.separator().classes('my-4')
                            
                            # Submit button
                            def create_new_task():
                                """Handle task creation"""
                                if not title_input.value or not desc_input.value or not category_input.value or not due_date_input.value:
                                    ui.notify('Please fill in all required fields', color='negative', position='top')
                                    return
                                
                                task_data = {
                                    'title': title_input.value,
                                    'description': desc_input.value,
                                    'priority': priority_select.value,
                                    'status': status_select.value,
                                    'category': category_input.value,
                                    'due_date': due_date_input.value + 'T00:00:00'
                                }
                                
                                db.create_task(task_data)
                                ui.notify('✅ Task created successfully!', color='positive', position='top')
                                
                                # Clear form
                                title_input.value = ''
                                desc_input.value = ''
                                category_input.value = ''
                                due_date_input.value = ''
                                priority_select.value = 'medium'
                                status_select.value = 'pending'
                            
                            with ui.row().classes('w-full justify-end gap-4'):
                                ui.button('Clear Form', on_click=lambda: [
                                    setattr(title_input, 'value', ''),
                                    setattr(desc_input, 'value', ''),
                                    setattr(category_input, 'value', ''),
                                    setattr(due_date_input, 'value', '')
                                ], color='secondary', icon='clear').classes('px-8')
                                
                                ui.button('Create Task', on_click=create_new_task, color='primary', icon='add').classes('px-8')
                
                # ===== FILTER TAB =====
                with ui.tab_panel(filter_tab):
                    ui.label('Filter & Search Tasks').classes('text-h5 font-bold mb-4')
                    
                    with ui.card().classes('p-6 mb-6'):
                        with ui.row().classes('w-full gap-4'):
                            status_filter = ui.select(
                                ['All', 'pending', 'in_progress', 'completed'],
                                label='Status',
                                value='All'
                            ).classes('flex-1')
                            status_filter.props('outlined')
                            
                            priority_filter = ui.select(
                                ['All', 'low', 'medium', 'high'],
                                label='Priority',
                                value='All'
                            ).classes('flex-1')
                            priority_filter.props('outlined')
                            
                            categories = ['All'] + list(set(t['category'] for t in db.get_all_tasks()))
                            category_filter = ui.select(
                                categories,
                                label='Category',
                                value='All'
                            ).classes('flex-1')
                            category_filter.props('outlined')
                    
                    # Filtered results container
                    results_container = ui.column().classes('w-full gap-4')
                    
                    def apply_filters():
                        """Apply filters and update display"""
                        results_container.clear()
                        
                        tasks = db.get_all_tasks()
                        filtered = tasks
                        
                        if status_filter.value != 'All':
                            filtered = [t for t in filtered if t['status'] == status_filter.value]
                        if priority_filter.value != 'All':
                            filtered = [t for t in filtered if t['priority'] == priority_filter.value]
                        if category_filter.value != 'All':
                            filtered = [t for t in filtered if t['category'] == category_filter.value]
                        
                        with results_container:
                            ui.label(f'Found {len(filtered)} tasks').classes('text-lg font-bold mb-4')
                            
                            if not filtered:
                                ui.label('No tasks match the selected filters').classes('text-gray-500')
                            else:
                                with ui.grid(columns=2).classes('w-full gap-4'):
                                    for task in filtered:
                                        with ui.card().classes('p-6'):
                                            ui.label(task['title']).classes('text-lg font-bold mb-2')
                                            ui.label(task['description']).classes('text-sm text-gray-600 mb-2')
                                            
                                            with ui.row().classes('gap-2'):
                                                ui.badge(task['priority'].upper()).classes('bg-purple-600 text-white')
                                                ui.badge(task['status'].replace('_', ' ').title()).classes('bg-blue-600 text-white')
                                                ui.badge(task['category']).classes('bg-green-600 text-white')
                    
                    # Auto-apply filters on change
                    status_filter.on_value_change(lambda: apply_filters())
                    priority_filter.on_value_change(lambda: apply_filters())
                    category_filter.on_value_change(lambda: apply_filters())
                    
                    # Initial display
                    apply_filters()
        
        # Footer
        with ui.footer().classes('bg-gray-100'):
            with ui.row().classes('w-full justify-center items-center py-4'):
                ui.label('Task Management System v1.0 | Powered by NiceGUI').classes('text-sm text-gray-600')
    
    # Start the UI
    ui.run(port=8084, reload=False, show=False, title='Task Management System')

if __name__ == '__main__':
    run_nicegui()