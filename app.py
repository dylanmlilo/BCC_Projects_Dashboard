from flask import Flask, render_template
from models.plot_functions import plot_home_page_charts
from models.engine.database import projects_data_to_dict_list
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", strict_slashes=False)
def index():
    projects_data = projects_data_to_dict_list()
    graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON = plot_home_page_charts()
    return render_template("home.html", graph1JSON=graph1JSON,
                           graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                           graph4JSON=graph4JSON, projects_data=projects_data,
                           graph5JSON=graph5JSON)

@app.route("/Servicing", strict_slashes=False)
def servicing():
    projects_data = projects_data_to_dict_list(1)
    return render_template("servicing.html", projects_data=projects_data)

@app.route("/Goods", strict_slashes=True)
def goods():
    projects_data = projects_data_to_dict_list(3)
    return render_template("goods.html", projects_data=projects_data)

@app.route("/Works", strict_slashes=False)
def works():
    projects_data = projects_data_to_dict_list(4)
    return render_template("works.html", projects_data=projects_data)

@app.route("/Services", strict_slashes=False)
def services():
    projects_data = projects_data_to_dict_list(2)
    return render_template("services.html", projects_data=projects_data)


if __name__ == "__main__":
    app.run(debug=True, port=3000)