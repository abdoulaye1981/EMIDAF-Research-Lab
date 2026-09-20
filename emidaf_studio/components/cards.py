from dash import html
import dash_bootstrap_components as dbc


class ProjectCard:

    @staticmethod
    def create(project):

        description = (
            project.description
            if project.description
            else "Aucune description renseignée."
        )

        return dbc.Card(
            [
                # ==========================================
                # En-tête
                # ==========================================

                html.Div(
                    [
                        html.Div(
                            html.I(
                                className=(
                                    "bi bi-folder2-open "
                                    "project-card-v2-icon"
                                )
                            ),
                            className="project-card-v2-icon-box",
                        ),

                        html.Div(
                            [
                                html.Div(
                                    "PROJET",
                                    className=(
                                        "project-card-v2-kicker"
                                    ),
                                ),

                                html.H3(
                                    project.name,
                                    className=(
                                        "project-card-v2-title"
                                    ),
                                ),
                            ],
                            className="project-card-v2-heading",
                        ),

                        html.Div(
                            f"#{project.id}",
                            className="project-card-v2-id",
                        ),
                    ],
                    className="project-card-v2-header",
                ),

                # ==========================================
                # Corps
                # ==========================================

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(
                                            className=(
                                                "bi bi-grid-1x2 "
                                                "me-2"
                                            )
                                        ),
                                        html.Span(
                                            "Workspace",
                                        ),
                                    ],
                                    className=(
                                        "project-card-v2-meta-label"
                                    ),
                                ),

                                html.Div(
                                    str(project.workspace_id),
                                    className=(
                                        "project-card-v2-meta-value"
                                    ),
                                ),
                            ],
                            className="project-card-v2-meta",
                        ),

                        html.P(
                            description,
                            className=(
                                "project-card-v2-description"
                            ),
                        ),
                    ],
                    className="project-card-v2-body",
                ),

                # ==========================================
                # Action
                # ==========================================

                html.Div(
                    dbc.Button(
                        [
                            html.Span("Ouvrir le projet"),
                            html.I(
                                className=(
                                    "bi bi-arrow-up-right "
                                    "ms-2"
                                )
                            ),
                        ],
                        id={
                            "type": "select-project",
                            "index": project.id,
                        },
                        color="link",
                        className="project-card-v2-button",
                    ),
                    className="project-card-v2-footer",
                ),
            ],
            className="project-card-v2",
        )
