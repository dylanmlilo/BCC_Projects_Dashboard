from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, select, join
from models.projects import ProjectsData, ProjectManagers
from models.gis import Output, Activity, ResponsiblePerson, Task
from models.strategic import StrategicTask
from dotenv import load_dotenv
import os

load_dotenv()

db_connection_string = os.getenv("db_connection_string")

engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)

session = Session()


def project_managers_to_dict_list():
    """
    Convert SQLAlchemy query results into a list of dictionaries.
    Exclude the _sa_instance_state attribute.
    
    Returns:
        list: A list of dictionaries containing project managers.
    """
    try:
        project_managers = session.query(ProjectManagers).all()
    except:
        session.rollback()
    finally:
        session.close()
    result_list = []
    for row in project_managers:
        result_dict = {}
        for column in row.__table__.columns:
            result_dict[column.name] = getattr(row, column.name)
        result_list.append(result_dict)
    return result_list


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


def gis_data_to_dict_list():
    """
    Returns a list of dictionaries containing GIS data.
    
    This function queries the database to retrieve GIS data, including output information, 
    activity details, responsible person information, and task descriptions. It then 
    constructs a list of dictionaries, where each dictionary represents a single GIS data 
    point. The function handles potential database errors and ensures that the session is 
    properly closed.
    
    Returns:
        A list of dictionaries for GIS Data
    """
    try:
        query = select(
            Output.id,
            Output.name,
            Activity.activity,
            ResponsiblePerson.name,
            ResponsiblePerson.designation,
            Task.description,
            Task.percentage_of_activity
        ).select_from(
            Output
        ).outerjoin(
            Activity, Output.id == Activity.output_id
        ).outerjoin(
            ResponsiblePerson, Activity.responsible_person_id == ResponsiblePerson.id
        ).outerjoin(
            Task, Activity.id == Task.activity_id
        )
    except:
        session.rollback()
    finally:
        session.close()

    try:
        results = session.execute(query).fetchall()
    except:
        session.rollback()
    finally:
        session.close()

    gis_data = []
    for row in results:
        gis_dict = {
            "output_id": row[0],
            "output_name": row[1],
            "activity": row[2],
            "responsible_person": row[3],
            "designation": row[4],
            "task_description": row[5],
            "percentage_of_activity": row[6]
        }
        gis_data.append(gis_dict)

    return gis_data

def gis_data_to_responsible_person():
    gis_data = gis_data_to_dict_list()
    responsible_person_dict = {}

    for data in gis_data:
        person_name = data['responsible_person']
        if person_name not in responsible_person_dict:
            responsible_person_dict[person_name] = []
        responsible_person_dict[person_name].append(data)
    
    return responsible_person_dict

# test = gis_data_to_responsible_person()
# print(test)


def gis_output_data_to_dict_list():
    output_list = []
    try:
        query = session.query(Output.id, Output.name).all()
    except:
        session.rollback()
    finally:
        session.close()

    for row in query:
        output_dict = {
            "output_id": row[0],
            "output_name": row[1]
        }
        output_list.append(output_dict)

    return output_list

def gis_activity_data_to_dict_list():
    activity_list = []
    try:
        query = session.query(Activity.id, Activity.activity, Activity.output_id, Activity.responsible_person_id).all()
    except:
        session.rollback()
    finally:
        session.close()

    for row in query:
        activity_dict = {
            "activity_id": row[0],
            "activity_name": row[1],
            "output_id": row[2],
            "responsible_person_id": row[3]
        }
        activity_list.append(activity_dict)

    return activity_list

def gis_responsible_person_data_to_dict_list():
    responsible_person_list = []
    try:
        query = session.query(ResponsiblePerson.id, ResponsiblePerson.name, ResponsiblePerson.designation).all()
    except:
        session.rollback()
    finally:
        session.close()

    for row in query:
        responsible_person_dict = {
            "responsible_person_id": row[0],
            "responsible_person_name": row[1],
            "designation": row[2]
        }
        responsible_person_list.append(responsible_person_dict)

    return responsible_person_list

def gis_task_data_to_dict_list():
    task_list = []
    try:
        query = session.query(Task.id, Task.description, Task.percentage_of_activity, Task.activity_id).all()
    except:
        session.rollback()
    finally:
        session.close()

    for row in query:
        task_dict = {
            "task_id": row[0],
            "task_description": row[1],
            "percentage_of_activity": row[2],
            "activity_id": row[3]
        }
        task_list.append(task_dict)

    return task_list

def strategic_tasks_to_dict_list():
    # Perform a join between StrategicTask and ProjectManagers on the assigned_to column
    try:
        query = session.query(StrategicTask, ProjectManagers.name).join(ProjectManagers, StrategicTask.assigned_to == ProjectManagers.id)
    except:
        session.rollback()
    finally:
        session.close()

    # Execute the query and fetch all results
    results = query.all()
    
    # Create a list of dictionaries with the task details and project manager names
    task_list = [
    {
        'task_id': task.task_id,
        'status': task.status,
        'priority': task.priority,
        'deadline': task.deadline,
        'task': task.task,
        'description': task.description,
        'assigned_to': task.assigned_to,
        'project_manager': project_manager_name,
        'deliverables': task.deliverables,
        'percentage_done': task.percentage_done,
        'fixed_cost': task.fixed_cost,
        'estimated_hours': task.estimated_hours,
        'actual_hours': task.actual_hours
    }
    for task, project_manager_name in results
    ]
    
    return task_list