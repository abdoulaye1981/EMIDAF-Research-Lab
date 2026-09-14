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
                            f"Workspace ID : {project.workspace_id}"
                        ),

                        html.P(
                            project.description
                        ),

                        dbc.Button(
                            "Sélectionner",
                            id={
                                "type": "select-project",
                                "index": project.id
                            },
                            color="secondary",
                            size="sm",
                            outline=True
                        )
                    ]
                )
            ],

            className="mb-3"
        )
