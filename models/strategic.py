from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.projects import ProjectManagers
from models.base import Base


class StrategicTask(Base):
    __tablename__ = 'strategic_tasks'
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255))
    priority = Column(String(255))
    deadline = Column(String(255))
    task = Column(Text)
    description = Column(Text)
    assigned_to = Column(Integer, ForeignKey('project_managers.id'))
    deliverables = Column(Text)
    percentage_done = Column(DECIMAL(10,2))
    fixed_cost = Column(DECIMAL(10,2))
    estimated_hours = Column(DECIMAL(10,2))
    actual_hours = Column(DECIMAL(10,2))

    def __init__(self, status, priority, deadline, task, description, assigned_to, deliverables, percentage_done, fixed_cost, estimated_hours, actual_hours):
        self.status = status
        self.priority = priority
        self.deadline = deadline
        self.task = task
        self.description = description
        self.assigned_to = assigned_to
        self.deliverables = deliverables
        self.percentage_done = percentage_done
        self.fixed_cost = fixed_cost
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours

    def __repr__(self):
        return f"<StrategicTask(task='{self.task}', description='{self.description}', assigned_to='{self.assigned_to}')>"