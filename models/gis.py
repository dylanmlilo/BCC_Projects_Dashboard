from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Output(Base):
    __tablename__ = "output"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Output(id={self.id}, name='{self.name}')"

class Activity(Base):
  __tablename__ = "activities"

  id = Column(Integer, primary_key=True)
  activity = Column(String(255), nullable=False)
  output_id = Column(Integer, ForeignKey("output.id"))
  responsible_person_id = Column(Integer, ForeignKey("responsiblepeople.id"))

  output = relationship("Output", backref="activities")
  responsible_person = relationship("ResponsiblePerson", backref="activities")

  def __init__(self, activity, output_id, responsible_person_id):
        self.activity = activity
        self.output_id = output_id
        self.responsible_person_id = responsible_person_id

  def __repr__(self):
    return f"Activity(id={self.id}, activity='{self.activity}', output_id={self.output_id}, responsible_person_id={self.responsible_person_id})"

class ResponsiblePerson(Base):
  __tablename__ = "responsiblepeople"

  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False)
  designation = Column(String(255), nullable=False)

  def __init__(self, name, designation):
        self.name = name
        self.designation = designation

  def __repr__(self):
    return f"ResponsiblePerson(id={self.id}, name='{self.name}', designation='{self.designation}')"

class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True)
  activity_id = Column(Integer, ForeignKey("activities.id"))
  description = Column(Text, nullable=False)
  percentage_of_activity = Column(DECIMAL(5, 2), nullable=True)

  activity = relationship("Activity", backref="tasks")

  def __init__(self, activity_id, description, percentage_of_activity=None):
        self.activity_id = activity_id
        self.description = description
        self.percentage_of_activity = percentage_of_activity

  def __repr__(self):
    return f"Task(id={self.id}, activity_id={self.activity_id}, description='{self.description}', percentage_of_activity={self.percentage_of_activity})"