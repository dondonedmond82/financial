import warnings

import panel as pn
import hvplot.pandas
import json
import datetime as dt
import os

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, NumberFormatter, TableColumn, Button
from bokeh.layouts import column,row

import pandas as pd
import numpy as np

import xlsxwriter

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Button, CustomJS
import pandas as pd
import io
import base64

warnings.filterwarnings("ignore")
pn.extension()

#########################################################################################################################################################

df = pd.read_csv("./data/output.csv")

df['active_fy'] = df['active_fy'].astype("str")

#########################################################################################################################################################

dose_1 = pn.widgets.Button(name="Budget & Financial", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
dose_1.on_click(lambda event: show_page("Page1"))

#########################################################################################################################################################

x = 900
y = 420

x_bar = 490
y_bar = 195


def details():
    return df.hvplot.table(width=x, height=y)


def show_page(page_key):
    main_area.clear()
    main_area.append(mapping[page_key])

#########################################################################################################################################################

def CreatePage1():
    return pn.Column(

            pn.Row(
                pn.Column(
                    pn.Row(details),

                ),
            ),
        )

#########################################################################################################################################################

mapping = { 
    "Page1": CreatePage1(),  
}

logout   =  pn.widgets.Button(name="Déconnexion", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
logout.js_on_click(code="""window.location.href = './logout'""")

sidebar = pn.Column(pn.pane.Markdown("## Menu"), dose_1, logout, styles={"width": "100%", "padding": "15px"})
main_area = pn.Column(mapping['Page1'], styles={"width":"100%"})


template = pn.template.BootstrapTemplate(
    title=f"""Bienvenue {pn.state.user}""",
    sidebar=[sidebar],
    main=[main_area],
    # footer=[sidebar],
    header_background="#f5b907",
    # accent_base_color='orange',
    site="Budget and Financial Forecast",  logo="logo.png",
    sidebar_width=250,
    busy_indicator=None,
)

template.servable()
