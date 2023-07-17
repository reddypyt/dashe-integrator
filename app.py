from dash import Dash, dcc, html, page_container, page_registry, DiskcacheManager
import dash_design_kit as ddk


app = Dash(
    __name__,
    suppress_callback_exceptions=False,
    use_pages=True,
)
server = app.server  # Needed to attach vscode Flask debugger

app.layout = ddk.App(show_editor=True, children=[
    ddk.Header([
        ddk.Logo(src=app.get_relative_path('/assets/infosource_log.svg')),
        ddk.Title('Data Integrator'),
        ddk.Menu([
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in page_registry.values()
        ])
    ]),
    html.Div(page_container)
],
    theme={
        "accent": "#2BFEBE",
        "accent_positive": "#33ffe6",
        "accent_negative": "#ff2c6d",
        "background_content": "#1D262F",
        "background_page": "#242e3f",
        "body_text": "#87B4E5",
        "border": "#5C8CBE",
        "border_style": {
            "name": "underlined",
            "borderWidth": "0px 0px 1px 0px",
            "borderStyle": "solid",
            "borderRadius": 0
        },
        "button_border": {
            "width": "1px",
            "color": "#2BFEBE",
            "radius": "0px"
        },
        "button_capitalization": "uppercase",
        "button_text": "#2BFEBE",
        "button_background_color": "#1D262F",
        "control_border": {
            "width": "0px 0px 1px 0px",
            "color": "#5C8CBE",
            "radius": "0px"
        },
        "control_background_color": "#1D262F",
        "control_text": "#87B4E5",
        "card_margin": "15px",
        "card_padding": "5px",
        "card_border": {
            "width": "0px 0px 0px 0px",
            "style": "solid",
            "color": "#5C8CBE",
            "radius": "0px"
        },
        "card_background_color": "#1D262F",
        "card_box_shadow": "0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24)",
        "card_outline": {
            "width": "0px",
            "style": "solid",
            "color": "#5C8CBE"
        },
        "card_header_margin": "0px",
        "card_header_padding": "10px",
        "card_header_border": {
            "width": "0px 0px 1px 0px",
            "style": "solid",
            "color": "#5C8CBE",
            "radius": "0px"
        },
        "card_header_background_color": "#1D262F",
        "card_header_box_shadow": "0px 0px 0px rgba(0,0,0,0)",
        "breakpoint_font": "1200px",
        "breakpoint_stack_blocks": "700px",
        "colorway": [
            "#2bfebe",
            "#4c78a8",
            "#f58518",
            "#e45756",
            "#54a24b",
            "#eeca3b",
            "#b279a2",
            "#ff9da6",
            "#9d755d",
            "#bab0ac"
        ],
        "colorscale": [
            "#2bfebe",
            "#27e8aa",
            "#22d396",
            "#1ebd83",
            "#19a971",
            "#14945f",
            "#0f814d",
            "#096e3c",
            "#045b2b",
            "#00491b"
        ],
        "dbc_primary": "#2BFEBE",
        "dbc_secondary": "#dce6f1",
        "dbc_info": "#00A4D9",
        "dbc_gray": "#adb5bd",
        "dbc_success": "#00D9C1",
        "dbc_warning": "#e9e086",
        "dbc_danger": "#ff5e7b",
        "font_family": "Noto Sans",
        "font_family_header": "Playfair",
        "font_family_headings": "Playfair",
        "font_size": "17px",
        "font_size_smaller_screen": "15px",
        "font_size_header": "24px",
        "title_capitalization": "uppercase",
        "header_content_alignment": "spread",
        "header_margin": "0px 0px 15px 0px",
        "header_padding": "0px",
        "header_border": {
            "width": "0px 0px 0px 0px",
            "style": "solid",
            "color": "#5C8CBE",
            "radius": "0px"
        },
        "header_background_color": "#1D262F",
        "header_box_shadow": "0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24)",
        "header_text": "#87B4E5",
        "heading_text": "#87B4E5",
        "text": "#87B4E5",
        "report_background_content": "#FAFBFC",
        "report_background_page": "white",
        "report_text": "black",
        "report_font_family": "Computer Modern",
        "report_font_size": "12px"
}
)


if __name__ == '__main__':
    app.run(debug=True)
