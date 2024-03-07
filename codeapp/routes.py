# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io
from typing import Text

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Dummy
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[Dummy] = get_data_list()

    counter: dict[int | str, int] = calculate_statistics(dataset)

    return render_template("home.html", counter=counter)


@bp.get("/image")
def image() -> Response:
    dataset: list[Dummy] = get_data_list()

    counter: dict[int | str, int] = calculate_statistics(dataset)
    fig = Figure()
    sorted_keys = sorted(counter.keys(), key=lambda k: counter[k], reverse=True)
    fig.gca().bar(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted_keys],
        color="#e0218a",
        alpha=0.8,
        zorder=3,
    )
    keys_as_str: list[str | Text] = []
    for key in counter:
        new_key: str = str(key)
        keys_as_str.append(new_key)
    fig.gca().set_xticks(list(range(0, 20)))
    fig.gca().set_xticklabels(keys_as_str, rotation="vertical")
    fig.gca().grid(ls=":", zorder=1)
    fig.gca().set_xlabel("Genre")
    fig.gca().set_ylabel("Number of games")
    fig.tight_layout()

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:
    dataset: list[Dummy] = get_data_list()
    return jsonify(dataset)


@bp.get("/json-stats")
def get_json_stats() -> Response:
    dataset: list[Dummy] = get_data_list()
    counter: dict[int | str, int] = calculate_statistics(dataset)
    return jsonify(counter)
