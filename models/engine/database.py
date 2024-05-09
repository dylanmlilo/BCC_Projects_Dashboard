from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from models.projects import ProjectsData, ProjectManagers
from dotenv import load_dotenv
import os

load_dotenv()

db_connection_string = os.getenv("db_connection_string")

engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)

session = Session()

def projects_data_to_dict_list(contract_type_id=None):
    """
    Convert SQLAlchemy query results into a list of dictionaries.
    Exclude the _sa_instance_state attribute.
    
    Args:
        contract_type_id (str, optional): Filter results by contract_type_id.
        Defaults to None.
    
    Returns:
        list: A list of dictionaries containing projects data with related data
        from ContractType, ProjectManagers, and Section.
    """
    try:
        query = session.query(ProjectsData) \
        .join(ProjectsData.contract_type) \
        .join(ProjectsData.project_manager) \
        .join(ProjectsData.section)
    except:
        session.rollback()
    finally:
        session.close()
    
    if contract_type_id:
        query = query.filter(ProjectsData.contract_type_id == contract_type_id)
    
    projects_data = query.all()
    
    result_list = []
    for row in projects_data:
        result_dict = {}
        for column in row.__table__.columns:
            result_dict[column.name] = getattr(row, column.name)
        
        result_dict['contract_type'] = row.contract_type.name
        result_dict['project_manager'] = row.project_manager.name
        result_dict['section'] = row.section.name
        
        result_list.append(result_dict)
    
    sorted_result_list = sorted(result_list, key=lambda x: x["id"])
    return sorted_result_list


def contract_type_data_dict(contract_type_id):
    """
    Filters and returns project data for a specific contract type id.

    Args:
      contract_type_id (int): The contract type id to filter by.

    Returns:
      list: A list of dictionaries containing project data for the specified contract type,
        or an empty list if no data is found.
    """ 

    servicing_data = projects_data_to_dict_list()
    filtered_data = [row for row in servicing_data if 'contract_type_id' in row and row['contract_type_id'] == contract_type_id]
    return filtered_data

# print(servicing_data_dict(4))


# print(projects_data_to_dict_list())
# print(servicing_data_dict(1))

# def project_managers_to_dict():
#     project_managers = []
#     project_manager = session.query(ProjectManagers.name).all()
    
        

# result = projects_data_to_dict_list(1)
# print(result)