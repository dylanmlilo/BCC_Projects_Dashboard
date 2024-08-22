from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.plot_functions import today_date, plot_home_page_charts, plot_servicing_page_charts, progress_bar
from models.engine.database import session, projects_data_to_dict_list, gis_data_to_dict_list, gis_data_to_responsible_person, strategic_tasks_to_dict_list, gis_output_data_to_dict_list, gis_activity_data_to_dict_list, gis_responsible_person_data_to_dict_list, gis_task_data_to_dict_list
from models.users import Users
from models.login import LoginForm
from models.projects import ProjectsData
from models.gis import ResponsiblePerson, Activity, Task, Output
import os
import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user object from the database based on the user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Users or None: The user object if found, None otherwise.
    """
    try:
        user = session.query(Users).get(int(user_id))
    except:
        session.rollback()
    finally:
        session.close()
    return user


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = session.query(Users).filter_by(username=form.username.data).first()
        except:
            session.rollback()
        finally:
            session.close()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@app.route('/logout', strict_slashes=False)
def logout():
    """
    Logs out the current user and redirects to the login page.

    Returns:
        flask.Response: A redirect response to the login page.
    """
    logout_user()
    return redirect(url_for('login'))


@app.route("/admin_dashboard", strict_slashes=False)
@login_required
def admin_dashboard():
    """
    Renders the admin dashboard page.

    Returns:
        flask.Response: The rendered admin dashboard template.
    """
    return render_template("admin_dashboard.html")


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


@app.route("/projects_data", strict_slashes=False)
def projects_data():
    """
    Function to handle projects data retrieval and rendering.

    Retrieves projects data and today's date, then renders the projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "projects_data.html" with today's date and projects data.

    """
    projects_data = projects_data_to_dict_list()
    formatted_date = today_date()
    return render_template("projects_data.html", today_date=formatted_date,
                           projects_data=projects_data)


@app.route('/insert_projects_data', methods=['POST'])
def insert_projects_data():
    """
    Inserts the project data into the database and redirects to the projects page.

    Returns:
        flask.Response: A redirect response to the projects page or a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            # Get form data
            contract_number = request.form.get('contract_number')
            contract_name = request.form.get('contract_name')
            contract_type_id = request.form.get('contract_type_id')
            project_manager_id = request.form.get('project_manager_id')
            section_id = request.form.get('section_id')
            contractor = request.form.get('contractor')
            year = request.form.get('year')
            date_contract_signed_by_bcc = request.form.get('date_contract_signed_by_bcc')
            early_start_date = request.form.get('early_start_date')
            contract_duration_weeks = request.form.get('contract_duration_weeks')
            contract_duration_months = request.form.get('contract_duration_months')
            early_finish_date = request.form.get('early_finish_date')
            extension_of_time = request.form.get('extension_of_time')
            project_status = request.form.get('project_status')
            contract_value_including_ten_percent_contingency = request.form.get('contract_value_including_ten_percent_contingency')
            performance_guarantee_value = request.form.get('performance_guarantee_value')
            performance_guarantee_expiry_date = request.form.get('performance_guarantee_expiry_date')
            advance_payment_value = request.form.get('advance_payment_value')
            advance_payment_guarantee_expiry_date = request.form.get('advance_payment_guarantee_expiry_date')
            total_certified_interim_payments_to_date = request.form.get('total_certified_interim_payments_to_date')
            financial_progress_percentage = request.form.get('financial_progress_percentage')
            roads_progress = request.form.get('roads_progress')
            water_progress = request.form.get('water_progress')
            sewer_progress = request.form.get('sewer_progress')
            storm_drainage_progress = request.form.get('storm_drainage_progress')
            public_lighting_progress = request.form.get('public_lighting_progress')
            physical_progress_percentage = request.form.get('physical_progress_percentage')
            tax_clearance_validation = request.form.get('tax_clearance_validation')
            link = request.form.get('link')
        
            # Validation checks
            errors = []

            if errors:
                return jsonify({'errors': errors}), 400

            # Create new project record
            new_project_record = ProjectsData(
                contract_number=contract_number,
                contract_name=contract_name,
                contract_type_id=contract_type_id,
                project_manager_id=project_manager_id,
                section_id=section_id,
                contractor=contractor,
                year=year,
                date_contract_signed_by_bcc=date_contract_signed_by_bcc,
                early_start_date=early_start_date,
                contract_duration_weeks=contract_duration_weeks,
                contract_duration_months=contract_duration_months,
                early_finish_date=early_finish_date,
                extension_of_time=extension_of_time,
                project_status=project_status,
                contract_value_including_ten_percent_contingency=contract_value_including_ten_percent_contingency,
                performance_guarantee_value=performance_guarantee_value,
                performance_guarantee_expiry_date=performance_guarantee_expiry_date,
                advance_payment_value=advance_payment_value,
                advance_payment_guarantee_expiry_date=advance_payment_guarantee_expiry_date,
                total_certified_interim_payments_to_date=total_certified_interim_payments_to_date,
                financial_progress_percentage=financial_progress_percentage,
                roads_progress=roads_progress,
                water_progress=water_progress,
                sewer_progress=sewer_progress,
                storm_drainaige_progress=storm_drainage_progress,
                public_lighting_progress=public_lighting_progress,
                physical_progress_percentage=physical_progress_percentage,
                tax_clearance_validation=tax_clearance_validation,
                link=link)
            
            session.add(new_project_record)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('projects_data'))

        
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        
        finally:
            session.close()
    
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


@app.route("/GIS_data", strict_slashes=False)
def gis_data():
    """
    Function to handle GIS data retrieval and rendering.

    Retrieves GIS data and today's date, then renders the gis_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "gis_data.html" with today's date and GIS data.

    """
    gis_data = gis_data_to_dict_list()
    gis_output_data = gis_output_data_to_dict_list()
    gis_activity_data = gis_activity_data_to_dict_list()
    gis_responsible_person_data = gis_responsible_person_data_to_dict_list()
    gis_task_data = gis_task_data_to_dict_list()
    formatted_date = today_date()
    return render_template("gis_data.html", today_date=formatted_date,
                           gis_data=gis_data, gis_output_data=gis_output_data,
                           gis_activity_data=gis_activity_data,
                           gis_responsible_person_data=gis_responsible_person_data,
                           gis_task_data=gis_task_data)


@app.route("/insert_gis_resp_person_data", methods=['POST'])
def insert_gis_resp_person_data():
    """
    Inserts the gis data into the database and redirects to the gis data page.

    Returns:
        flask.Response: A redirect response to the  dagista page or a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            name = request.form.get('responsible_person_name')
            designation = request.form.get('designation')

            new_responsible_person = ResponsiblePerson(name=name, designation=designation)
            session.add(new_responsible_person)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('gis_data'))
        
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        
        finally:
            session.close()


@app.route("/insert_gis_output_data", methods=['POST'])
def insert_gis_output_data():
    """
    Inserts the gis data into the database and redirects to the gis data page.

    Returns:
        flask.Response: A redirect response to the  dagista page or a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            name = request.form.get('output_name')

            new_output = Output(name=name)
            session.add(new_output)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('gis_data'))

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

        finally:
            session.close()


@app.route("/insert_gis_activity_data", methods=['POST'])
def insert_gis_activity_data():
    """
    Inserts the gis data into the database and redirects to the gis data page.

    Returns:
        flask.Response: A redirect response to the  dagista page or a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            activity = request.form.get('activity_name')
            output_id = request.form.get('output_id')
            responsible_person_id = request.form.get('responsible_person_id')


            new_activity = Activity(activity=activity, output_id=output_id, responsible_person_id=responsible_person_id)
            session.add(new_activity)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('gis_data'))

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400

        finally:
            session.close()


@app.route("/insert_gis_task_data", methods=['POST'])
def insert_gis_task_data():

    if request.method == "POST":
        try:
            activity_id = request.form.get('activity_id')
            description = request.form.get('task_description')
            percentage_of_activity = request.form.get('percentage_of_activity')

            new_task = Task(activity_id=activity_id, description=description, percentage_of_activity=percentage_of_activity)
            session.add(new_task)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('gis_data'))

        except Exception as e:  
            session.rollback()
            return jsonify({'error': str(e)}), 400

        finally:
            session.close()

@app.route('/insert_gis_data', methods=['POST'])
def insert_gis_data():
    """
    Inserts the gis data into the database and redirects to the gis data page.

    Returns:
        flask.Response: A redirect response to the  dagista page or a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            activity = request.form.get('activity')
            output_id = request.form.get('output_id')
            responsible_person_id = request.form.get('responsible_person_id')
            dam_percentage = request.form.get('dam_percentage')
            dam_volume = request.form.get('dam_volume')
            daily_inflow = request.form.get('daily_inflow')

            # Validation checks
            errors = []

            if not daily_inflow:
                daily_inflow = None
            else:
                try:
                    daily_inflow = float(daily_inflow)
                except ValueError:
                    errors.append("daily_inflows must be a valid number")

            if errors:
                return jsonify({'errors': errors}), 400

            new_dam_record = DamData(dam_id=dam_id, date=date, dam_reading=dam_reading, dam_percentage=dam_percentage, dam_volume=dam_volume, daily_inflow=daily_inflow)
            session.add(new_dam_record)
            session.commit()
            flash('Data inserted successfully')
            return redirect(url_for('dam_data'))

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        
        finally:
            session.close()
    
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