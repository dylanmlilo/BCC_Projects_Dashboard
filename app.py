from flask import Flask, render_template, jsonify, request
from models.plot_functions import today_date, plot_home_page_charts, plot_servicing_page_charts, progress_bar
from models.engine.database import projects_data_to_dict_list, gis_data_to_dict_list, gis_data_to_responsible_person, strategic_tasks_to_dict_list
import os
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
    
    
# @app.route('/get_project_managers', methods=['GET'])
# def get_project_managers():
#     # Query the database to get the list of project managers
#     project_managers = ['Alice', 'Bob', 'Charlie']  # Example list of project managers

#     return jsonify(project_managers)
    

@app.route("/Servicing", strict_slashes=False)
def servicing():
    projects_data = projects_data_to_dict_list(1)
    servicing_data_JSON = plot_servicing_page_charts()
    formatted_date = today_date()
    return render_template("servicing.html", projects_data=projects_data,
                           today_date=formatted_date,
                           servicing_data_JSON=servicing_data_JSON)

@app.route("/Goods", strict_slashes=True)
def goods():
    projects_data = projects_data_to_dict_list(3)
    formatted_date = today_date()
    return render_template("goods.html", today_date=formatted_date, 
                           projects_data=projects_data)

@app.route("/Works", strict_slashes=False)
def works():
    projects_data = projects_data_to_dict_list(4)
    formatted_date = today_date()
    return render_template("works.html", today_date=formatted_date,
                           projects_data=projects_data)

@app.route("/Services", strict_slashes=False)
def services():
    projects_data = projects_data_to_dict_list(2)
    formatted_date = today_date()
    return render_template("services.html", today_date=formatted_date,
                           projects_data=projects_data)
    
@app.route("/GIS", strict_slashes=False)
def gis():
    gis_data = gis_data_to_dict_list()
    responsible_persons= gis_data_to_responsible_person()
    progress_data = progress_bar()
    formatted_date = today_date()
    return render_template("gis.html", today_date=formatted_date,
                           gis_data=gis_data, progress_data=progress_data,
                           responsible_persons=responsible_persons)
    
@app.route("/StrategicPlanning", strict_slashes=False)
def strategic_planning():
    strategic_data_list = strategic_tasks_to_dict_list()
    formatted_date = today_date()
    return render_template("strategic_planning.html", today_date=formatted_date, 
                           strategic_data_list=strategic_data_list)


if __name__ == "__main__":
    app.run(debug=True, port=3000)