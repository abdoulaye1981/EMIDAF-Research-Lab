from dash import html
import dash_bootstrap_components as dbc


class ProjectCard:

    @staticmethod
    def create(project):

        return dbc.Card(

            [

                dbc.CardHeader(

                    "📁 " + project.name

                ),

                dbc.CardBody(

                    [

                        html.P(

                            f"Auteur : {project.author}"

                        ),

                        html.P(

                            project.description

                        )

                    ]

                )

            ],

            className="mb-3"

        )