from flask import Flask, abort, render_template, jsonify
from models.plot_functions import today_date, plot_home_page_charts, plot_servicing_page_charts, progress_bar
from models.engine.database import session, projects_data_to_dict_list, gis_data_to_dict_list, gis_data_to_responsible_person, strategic_tasks_to_dict_list
from models.projects import ContractType
import os
import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", strict_slashes=False)
def index():
    projects_data = projects_data_to_dict_list()
    active_projects = [project for project in projects_data if project['project_status'] == "In Progress"]

    # Get unique project names for dropdown
    project_names = [project['contract_name'] for project in active_projects]
    
    graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON = plot_home_page_charts()
    formatted_date = today_date()
    return render_template("home.html", graph1JSON=graph1JSON, today_date=formatted_date,
                           graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                           graph4JSON=graph4JSON, projects_data=projects_data,
                           graph5JSON=graph5JSON, project_names=project_names)

    
@app.route("/Servicing", strict_slashes=False)
def servicing():
    """
    Renders the 'servicing.html' template with project data for servicing contracts.

    This function fetches project data for servicing contracts, generates a bar chart,
    and renders the 'servicing.html' template with the necessary data.

    Returns:
        Flask.Response: The rendered template.
    """
    projects_data = projects_data_to_dict_list(1)
    servicing_data_JSON = plot_servicing_page_charts()
    formatted_date = today_date()
    return render_template("servicing.html", projects_data=projects_data,
                           today_date=formatted_date,
                           servicing_data_JSON=servicing_data_JSON)


@app.route("/Goods", strict_slashes=True)
def goods():
    """
    Function to handle /Goods route.

    Retrieves projects data and today's date, then renders the goods.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "goods.html" with today's date and projects data.

    """
    projects_data = projects_data_to_dict_list(3)
    formatted_date = today_date()
    return render_template("goods.html", today_date=formatted_date, 
                           projects_data=projects_data)


@app.route("/Works", strict_slashes=False)
def works():
    """
    Function to handle works data retrieval and rendering.

    Retrieves projects data and today's date, then renders the works.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "works.html" with today's date and projects data.

    """
    projects_data = projects_data_to_dict_list(4)
    formatted_date = today_date()
    return render_template("works.html", today_date=formatted_date,
                           projects_data=projects_data)


@app.route("/Services", strict_slashes=False)
def services():
    """
    Function to handle Services route.

    Retrieves projects data and today's date, then renders the services.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "services.html" with today's date and projects data.

    """
    projects_data = projects_data_to_dict_list(2)
    formatted_date = today_date()
    return render_template("services.html", today_date=formatted_date,
                           projects_data=projects_data)
    
@app.route("/GIS", strict_slashes=False)
def gis():
    """
    Function to handle GIS route.

    Retrieves GIS data, responsible persons, progress data, and today's date, then renders the gis.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "gis.html" with today's date, GIS data, progress data, and responsible persons.

    """
    gis_data = gis_data_to_dict_list()
    responsible_persons= gis_data_to_responsible_person()
    progress_data = progress_bar()
    formatted_date = today_date()
    return render_template("gis.html", today_date=formatted_date,
                           gis_data=gis_data, progress_data=progress_data,
                           responsible_persons=responsible_persons)
    
@app.route("/StrategicPlanning", strict_slashes=False)
def strategic_planning():
    """
    Function to handle Strategic Planning route.

    Retrieves strategic data list and today's date, then renders the strategic_planning.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "strategic_planning.html" with today's date and strategic data list.

    """
    strategic_data_list = strategic_tasks_to_dict_list()
    formatted_date = today_date()
    return render_template("strategic_planning.html", today_date=formatted_date, 
                           strategic_data_list=strategic_data_list)


@app.route("/api/projects_data", strict_slashes=False)
def projects_data_api():
    """
    Function to handle projects data API endpoint.

    Retrieves projects data and returns it in JSON format.

    Parameters:
    - None

    Returns:
    - JSON response containing projects data.

    """
    projects_data = projects_data_to_dict_list()
    return jsonify(projects_data)

# @app.route("/get_data_from_my_api", strict_slashes=False)
# def get_data_from_my_api():
#     response = requests.get("http://127.0.0.1:3000/api/projects_data")
#     return response.json()

# response = requests.get("http://127.0.0.1:3000/api/projects_data")
# print(response.json())


if __name__ == "__main__":
    app.run(debug=True, port=3000)