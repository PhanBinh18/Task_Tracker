import typer
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Duong dan toi file JSON
TASK_FILE = Path("task.json")

# Dinh nghia model cho Task
class Task:
    def __init__(self, id: int, description: str, status: str, create_at: str, update_at: str):
        self.id = id
        self.description = description
        self.status = status
        self.create_at = create_at
        self.update_at = update_at

    def to_dict(self):
        return self.__dict__
    
    
def get_tasks() -> List[Task]:
    """Đọc dữ liệu từ file tasks.json"""
    if not TASK_FILE.exists():
        return []
    with open(TASK_FILE, "r") as f:
        try:
            # Thử đọc file JSON
            data = json.load(f)
        except json.JSONDecodeError:
            # Nếu file trống hoặc bị lỗi, trả về danh sách rỗng
            return []
    return [Task(**task) for task in data]


def save_tasks(tasks: List[Task]):
    """Ghi dữ liệu vào file tasks.json"""
    with open(TASK_FILE, "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)


# Khởi tạo Typer app
app = typer.Typer(help="Một ứng dụng CLI để quản lí các tác vụ")


@app.command(name="add", help="Thêm một tác vụ mới.")
def add_task(description: str):
    """Thêm một tác vụ mới với mô tả."""
    tasks = get_tasks()
    new_id = max([task.id for task in tasks], default=0) + 1
    now = datetime.now().isoformat()
    new_task = Task(id=new_id, description=description, status="todo", create_at=now, update_at=now)
    tasks.append(new_task)
    save_tasks(tasks)
    typer.echo(f"Task added successfully (ID: {new_id})")


@app.command(name="list", help="Liệt kê tất cả các tác vụ hoặc theo trạng thái.")
def list_tasks(status: Optional[str] = typer.Argument(None, help="Trạng thái để lọc (todo, in-progress, done).")):
    """Liệt kê tất cả các tác vụ.
    Args:
        status (str): Trạng thái để lọc (todo, in-progress, done).
    """
    tasks = get_tasks()
    if status:
        tasks = [task for task in tasks if task.status == status]
    if not tasks:
        typer.echo("No tasks.")
        return
    
    typer.echo("List of tasks")
    for task in tasks:
        typer.echo(f"- ID: {task.id:<4} | Status: {task.status:<12} | Description: {task.description}")
    

@app.command(name="update", help="Cập nhật mô tả của một tác vụ.")
def update_task(task_id: int, new_description: str):
    """Cập nhật mô tả của một tác vụ dựa trên ID"""
    tasks = get_tasks()
    found = False
    for task in tasks:
        if task.id == task_id:
            task.description = new_description
            task.update_at = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        typer.echo(f"Task {task_id} updated successfully.")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")

@app.command(name="delete", help="Xóa một tác vụ.")
def delete_task(task_id: int):
    """Xóa một tác vụ dựa trên ID."""
    tasks = get_tasks()
    initial_count = len(tasks)
    tasks = [task for task in tasks if task.id != task_id]

    if len(tasks) < initial_count:
        save_tasks(tasks)
        typer.echo(f"Task {task_id} deleted successfully.") 
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")


@app.command(name="mark-in-progress", help="Đánh dấu một tác vụ là đang thực hiện.")
def mark_in_progress(task_id: int):
    tasks= get_tasks()
    found = False
    for task in tasks:
        if task.id == task_id:
            task.status = "in-progress"
            task.update_at = datetime.now().isoformat()
            found = True
            break
    
    if found:
        save_tasks(tasks)
        typer.echo(f"Task {task_id} marked as 'in-progress'.")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")


@app.command(name="mark-done", help="Mark a task as completed")
def mark_done(task_id: int):
    """Mark an task as 'done' """
    tasks = get_tasks()
    found = False
    for task in tasks:
        if task.id == task_id:
            task.status = "done"
            task.update_at = datetime.now().isoformat()
            found = True
    
    if found:
        save_tasks(tasks)
        typer.echo(f"Task {task_id} marked as 'done'.")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found")


if __name__ == "__main__":
    app()