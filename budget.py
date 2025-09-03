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

df_bar = df.head(30)

#########################################################################################################################################################

dose_1 = pn.widgets.Button(name="Budget & Financial", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
dose_1.on_click(lambda event: show_page("Page1"))

#########################################################################################################################################################

unique_abbreviation =  list(df['abbreviation'].unique())
select_abbreviation = pn.widgets.Select(name="Abbreviation", options=unique_abbreviation)


# --- Add a dropdown for Y-axis selection ---
select_amount_value = pn.widgets.Select(
    name='Amount Value',
    options=['outlay_amount', 'obligated_amount', 'budget_authority_amount'],  
    value='outlay_amount'
)

#########################################################################################################################################################

x = 900
y = 420

x_bar = 480
y_bar = 420


def details():
    return df.hvplot.table(width=x, height=y)


# --- Update your plotting function ---
@pn.depends(amount_value=select_amount_value)
def create_active_fy_scatter(amount_value):
    return (
        df.hvplot.scatter(
            x=amount_value,  # now dynamic
            y="percentage_of_total_budget_authority",
            width=x_bar,
            height=y_bar,
            title=f"Amount value by % of Total Budget Authority"
        )
    )

# --- Update your plotting function ---
@pn.depends(amount_value=select_amount_value)
def create_active_fy_bar(amount_value):
    return (
        df_bar.hvplot.barh(
            x="abbreviation",
            y=amount_value,  # now dynamic
            width=x_bar,
            height=y_bar,
            title=f"% Total Budget Authority by Abbreviation"
        )
    )

#########################################################################################################################################################

def show_page(page_key):
    main_area.clear()
    main_area.append(mapping[page_key])

#########################################################################################################################################################

def CreatePage1():
    return pn.Column(

            pn.Row(
                pn.Column(
                    pn.Row(select_amount_value),
                ),
            ),

            pn.Row(
                pn.Column(
                    pn.Row(create_active_fy_scatter),
                ),

                pn.Column(
                    pn.Row(create_active_fy_bar),
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
