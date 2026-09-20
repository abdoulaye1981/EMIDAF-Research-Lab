from dash import (
    Input,
    Output,
    callback,
)


THEMES = {
    "scientific": {
        "background": "#E9EFF4",
        "sidebar": "#F2F5F7",
        "navbar": "#243B53",
        "text": "#1F2933",
    },

    "laboratory": {
        "background": "#DCECF7",
        "sidebar": "#E7F1F7",
        "navbar": "#244A68",
        "text": "#183247",
    },

    "deep_blue": {
        "background": "#D4E0EC",
        "sidebar": "#DFE8F1",
        "navbar": "#17324D",
        "text": "#162A3A",
    },

    "research": {
        "background": "#E2F1EC",
        "sidebar": "#ECF6F2",
        "navbar": "#245447",
        "text": "#20352F",
    },

    "deep_green": {
        "background": "#D8E8E0",
        "sidebar": "#E3EFE9",
        "navbar": "#173F35",
        "text": "#18372D",
    },

    "dark": {
        "background": "#17212B",
        "sidebar": "#1E2A35",
        "navbar": "#0F171E",
        "text": "#F5F7FA",
    },
}


@callback(
    Output(
        "theme-preference",
        "data",
    ),
    Input(
        "theme-selector",
        "value",
    ),
)
def save_theme(theme):

    if theme not in THEMES:
        return "scientific"

    return theme


@callback(
    Output(
        "emidaf-app-shell",
        "style",
    ),
    Output(
        "emidaf-main-content",
        "style",
    ),
    Output(
        "emidaf-sidebar-column",
        "style",
    ),
    Output(
        "emidaf-navbar",
        "style",
    ),
    Input(
        "theme-preference",
        "data",
    ),
)
def apply_theme(theme):

    palette = THEMES.get(
        theme,
        THEMES["scientific"],
    )

    shell_style = {
        "minHeight": "100vh",
        "backgroundColor": palette["background"],
        "color": palette["text"],
    }

    main_style = {
        "minHeight": "calc(100vh - 56px)",
        "backgroundColor": palette["background"],
        "color": palette["text"],
    }

    sidebar_style = {
        "minHeight": "calc(100vh - 56px)",
        "backgroundColor": palette["sidebar"],
        "borderRight": "1px solid rgba(0,0,0,0.08)",
    }

    navbar_style = {
        "backgroundColor": palette["navbar"],
        "borderBottom": "1px solid rgba(255,255,255,0.08)",
    }

    return (
        shell_style,
        main_style,
        sidebar_style,
        navbar_style,
    )
