from dash import html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        html.H5("Navigation", className="mt-3"),

        dbc.Nav(
            [
                dbc.NavLink("🏠 Accueil", href="/"),
                dbc.NavLink("📁 Projets", href="/projects"),
                dbc.NavLink("📥 Importation", href="/import"),
                dbc.NavLink("🔍 Inspection", href="/inspection"),
                dbc.NavLink("🧹 EIDPP", href="/eidpp"),
                dbc.NavLink("📊 ELAE", href="/elae"),
                dbc.NavLink("🧠 EKDE", href="/ekde"),
                dbc.NavLink("🤖 EAIE", href="/eaie"),
                dbc.NavLink("💡 EXAIE", href="/exaie"),
                dbc.NavLink("🎯 EDSE", href="/edse"),
                dbc.NavLink("📄 Rapports", href="/reports"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "padding": "20px",
        "height": "100vh",
        "backgroundColor": "#F8F9FA",
    },
)