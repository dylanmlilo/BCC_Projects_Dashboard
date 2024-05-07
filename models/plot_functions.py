from flask import abort
import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go
from models.engine.database import session, projects_data_to_dict_list
from models.projects import ProjectsData, ContractType, Section, ProjectManagers
from datetime import datetime, timedelta


def plot_home_page_charts(selected_project_manager=None):
    """
    Generates and returns JSON representations of various plots for projects data
    
    Returns:
    graph1JSON (str): JSON representation of the physical progress plot.
    graph2JSON (str): JSON representation of the reservoir levels plot.
    """
    projects_data = projects_data_to_dict_list()
    df = pd.DataFrame(projects_data)
    
    if selected_project_manager:
        filtered_data = [project for project in projects_data if project['project_manager'] == selected_project_manager]
    else:
        filtered_data = projects_data

    df = pd.DataFrame(filtered_data)
    
    fig1 = px.bar(df, x = 'contract_number', y = 'physical_progress_percentage',
                  color='project_manager', title = "Physical Progress of Works")
    fig1.update_layout(
    legend_title_text='Project Managers',
    title={
        'x': 0.5,
        'y': 0.9,
        'font': {
            'size': 25,
            'family': 'Arial'
        }
    },
    xaxis_title_text="Contract Number",
    yaxis_title_text="Physical Progress (%)",
    xaxis_title_font_size=17,
    yaxis_title_font_size=17,
    legend_title_font={'size': 16}
    )
    
    fig2 = px.bar(df, x = 'contract_number', y = 'financial_progress_percentage',
                  color='contract_type', title = "Financial Progress of Works")
    fig2.update_layout(
    legend_title_text='Contract Type',
    title={
        'x': 0.5,
        'y': 0.9,
        'font': {
            'size': 25,
            'family': 'Arial'
        }
    },
    xaxis_title_text="Contract Number",
    yaxis_title_text="Financial Progress (%)",
    xaxis_title_font_size=17,
    yaxis_title_font_size=17,
    legend_title_font={'size': 16}
    )
    
    # Group the projects by year and count the number of projects in each year
    projects_by_year = df.groupby('year').size().reset_index(name='num_projects')

    # Create a pie chart using Plotly Express with the number of projects as values
    fig3 = px.pie(projects_by_year, values='num_projects', names='year',
             title='Distribution of Projects by Year')
    
    # Group the projects by status and count the number of projects in each status
    projects_by_status = df.groupby('project_status').size().reset_index(name='num_projects')

    # Create a Treemap Chart using Plotly Express
    fig4 = px.treemap(projects_by_status, path=['project_status'], values='num_projects', 
                      title='Distribution of Projects by Status')
    
    # Group the projects by project manager and 
    # count the number of projects for each manager
    projects_by_manager = df['project_manager'].value_counts().reset_index()
    projects_by_manager.columns = ['project_manager', 'num_projects']

    # Create a Sunburst Chart using Plotly Express
    fig5 = px.sunburst(projects_by_manager, path=['project_manager'], values='num_projects',
                  title='Distribution of Projects by Project Managers')


    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON