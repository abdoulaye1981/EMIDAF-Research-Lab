import dash_bootstrap_components as dbc


class Toolbar:

    @staticmethod
    def projects():

        return dbc.ButtonGroup(

            [

                dbc.Button(

                    "➕ Nouveau",

                    id="btn-new-project",

                    color="primary"

                ),

                dbc.Button(

                    "📂 Ouvrir",

                    id="btn-open-project"

                ),

                dbc.Button(

                    "🗑 Supprimer",

                    id="btn-delete-project",

                    color="danger"

                )

            ]

        )