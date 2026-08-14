from dash import Input
from dash import Output
from dash import State
from dash import callback


@callback(

    Output("project-modal", "is_open"),

    Input("btn-new-project", "n_clicks"),

    Input("btn-close-project", "n_clicks"),

    State("project-modal", "is_open")

)

def toggle_modal(

    open_click,

    close_click,

    is_open

):

    if open_click or close_click:

        return not is_open

    return is_open