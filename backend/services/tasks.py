from typing import List
from sqlmodel import Session, select
from sqlmodel import Session

from models import Task, TaskStatus, TaskResponse, TaskFilter
from dependencies.auth import get_current_active_user


class TaskService:
    @staticmethod
    def create_task(db: Session, user_id: int, task_data: dict) -> TaskResponse:
        """Create a new task for a user"""
        task = Task(
            title=task_data["title"],
            description=task_data.get("description"),
            status=task_data.get("status", TaskStatus.PENDING),
            user_id=user_id
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def get_tasks(db: Session, user_id: int, filters: TaskFilter, page: int = 1, per_page: int = 10) -> TaskListResponse:
        """Get tasks for a user with filtering and pagination"""
        base_query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if filters.status:
            base_query = base_query.where(Task.status == filters.status)

        # Apply search filter
        if filters.search:
            base_query = base_query.where(
                (Task.title.ilike(f"%{filters.search}%")) |
                (Task.description.ilike(f"%{filters.search}%"))
            )

        # Get total count
        total = db.exec(base_query).all()
        total_count = len(total)

        # Apply pagination
        offset = (page - 1) * per_page
        paginated_query = base_query.offset(offset).limit(per_page)

        tasks = db.exec(paginated_query).all()

        return TaskListResponse(
            tasks=[TaskResponse.from_orm(task) for task in tasks],
            total=total_count,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_task(db: Session, user_id: int, task_id: int) -> TaskResponse:
        """Get a single task by ID"""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        task = db.exec(statement).first()

        if not task:
            raise ValueError("Task not found")

        return TaskResponse.from_orm(task)

    @staticmethod
    def update_task(db: Session, user_id: int, task_id: int, update_data: dict) -> TaskResponse:
        """Update an existing task"""
        task = TaskService.get_task(db, user_id, task_id)

        # Update fields
        for key, value in update_data.items():
            if hasattr(task, key):
                setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def delete_task(db: Session, user_id: int, task_id: int) -> bool:
        """Delete a task"""
        task = TaskService.get_task(db, user_id, task_id)

        db.delete(task)
        db.commit()

        return True

    @staticmethod
    def mark_task_complete(db: Session, user_id: int, task_id: int) -> TaskResponse:
        """Mark a task as complete"""
        return TaskService.update_task(db, user_id, task_id, {"status": TaskStatus.COMPLETED})

    @staticmethod
    def mark_task_in_progress(db: Session, user_id: int, task_id: int) -> TaskResponse:
        """Mark a task as in progress"""
        return TaskService.update_task(db, user_id, task_id, {"status": TaskStatus.IN_PROGRESS})

    @staticmethod
    def mark_task_pending(db: Session, user_id: int, task_id: int) -> TaskResponse:
        """Mark a task as pending"""
        return TaskService.update_task(db, user_id, task_id, {"status": TaskStatus.PENDING})
