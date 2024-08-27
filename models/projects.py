from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Section(Base):
    __tablename__ = 'section'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Section({self.name})"

class ProjectManagers(Base):
    __tablename__ = 'project_managers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    section = Column(String(100))

    def __init__(self, name, section):
        self.name = name
        self.section = section

    def __repr__(self):
        return f"ProjectManagers({self.name}, {self.section})"

class ContractType(Base):
    __tablename__ = 'contract_type'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ContractType({self.name})"

class ProjectsData(Base):
    __tablename__ = 'projects_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_number = Column(String(50), nullable=False)
    contract_name = Column(Text)
    contract_type_id = Column(Integer, ForeignKey('contract_type.id'))
    project_manager_id = Column(Integer, ForeignKey('project_managers.id'))
    section_id = Column(Integer, ForeignKey('section.id'))
    contractor = Column(Text)
    year = Column(String(20))
    date_contract_signed = Column(Date)
    date_contract_signed_by_bcc = Column(Date)
    early_start_date = Column(Date)
    contract_duration_weeks = Column(DECIMAL(10, 2))
    contract_duration_months = Column(DECIMAL(10, 2))
    early_finish_date = Column(Date)
    extension_of_time = Column(Date)
    project_status = Column(String(50))
    contract_value_including_ten_percent_contingency = Column(DECIMAL(20, 2))
    performance_guarantee_value = Column(DECIMAL(20, 2))
    performance_guarantee_expiry_date = Column(Date)
    advance_payment_value = Column(DECIMAL(20, 2))
    advance_payment_guarantee_expiry_date = Column(Date)
    total_certified_interim_payments_to_date = Column(DECIMAL(20, 2))
    financial_progress_percentage = Column(DECIMAL(10, 2))
    roads_progress = Column(DECIMAL(10, 2))
    water_progress = Column(DECIMAL(10, 2))
    sewer_progress = Column(DECIMAL(10, 2))
    storm_drainage_progress = Column(DECIMAL(10, 2))
    public_lighting_progress = Column(DECIMAL(10, 2))
    physical_progress_percentage = Column(DECIMAL(10, 2))
    tax_clearance_validation = Column(String(50))
    link = Column(String(255))
    
    contract_type = relationship("ContractType")
    project_manager = relationship("ProjectManagers")
    section = relationship("Section")