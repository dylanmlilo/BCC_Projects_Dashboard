from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.projects import ProjectManagers


Base = declarative_base()


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