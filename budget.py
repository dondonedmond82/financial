import warnings
import os
import pandas as pd
import panel as pn
import hvplot.pandas

warnings.filterwarnings("ignore")
pn.extension('tabulator', 'echarts')

# --------------------------------------------------
# Load Data
# --------------------------------------------------
FILE_PATH = "./data/output.csv"
df = pd.read_csv(FILE_PATH)
df['active_fy'] = df['active_fy'].astype(str)

# --------------------------------------------------
# Widgets (Filters)
# --------------------------------------------------
select_amount_value = pn.widgets.Select(
    name="Amount Value",
    options=["outlay_amount", "obligated_amount", "budget_authority_amount"],
    value="outlay_amount"
)

select_abbreviation = pn.widgets.Select(
    name="Abbreviation",
    options=["All"] + sorted(df["abbreviation"].unique())
)

# --------------------------------------------------
# KPIs
# --------------------------------------------------
def kpi_cards():
    total_outlay = df["outlay_amount"].sum()
    total_obligated = df["obligated_amount"].sum()
    total_budget_auth = df["budget_authority_amount"].sum()

    utilization = (total_obligated / total_budget_auth * 100) if total_budget_auth else 0

    return pn.Row(
        pn.indicators.Number(name="Total Outlay", value=total_outlay, format="{value:,.0f}"),
        pn.indicators.Number(name="Total Obligated", value=total_obligated, format="{value:,.0f}"),
        pn.indicators.Number(name="Budget Authority", value=total_budget_auth, format="{value:,.0f}"),
        pn.indicators.Number(name="Utilization (%)", value=utilization, format="{value:.1f}%"),
    )

# --------------------------------------------------
# Filtered Data
# --------------------------------------------------
def get_filtered_data():
    data = df.copy()
    if select_abbreviation.value != "All":
        data = data[data["abbreviation"] == select_abbreviation.value]
    return data

# --------------------------------------------------
# Plots
# --------------------------------------------------
@pn.depends(select_amount_value, select_abbreviation)
def scatter_plot(amount_value, abbreviation):
    data = get_filtered_data()
    return data.hvplot.scatter(
        x=amount_value, 
        y="percentage_of_total_budget_authority",
        title=f"{amount_value} vs % of Budget Authority",
        width=500, height=400
    )

@pn.depends(select_amount_value, select_abbreviation)
def bar_plot(amount_value, abbreviation):
    top = df.groupby("abbreviation")[[amount_value]].sum().sort_values(amount_value, ascending=False).head(10)
    return top.hvplot.barh(
        y=amount_value,
        title=f"Top 10 Agencies by {amount_value}",
        width=500, height=400
    )

def table_view():
    return df.head(50).hvplot.table(width=900, height=400)

# --------------------------------------------------
# Export
# --------------------------------------------------
def exporting(event=None):
    filename = "BudgetData_filtered.xlsx"
    get_filtered_data().to_excel(filename, index=False)
    os.system(filename)

export_button = pn.widgets.Button(name="Export Data", button_type="primary")
export_button.on_click(exporting)

# --------------------------------------------------
# Tabs
# --------------------------------------------------
summary_tab = pn.Column(
    "## 📊 Budget Summary",
    # kpi_cards,
    pn.Row(scatter_plot, bar_plot)
)

details_tab = pn.Column(
    "## 📋 Data Preview",
    table_view,
    export_button
)

# --------------------------------------------------
# Template
# --------------------------------------------------
template = pn.template.FastListTemplate(
    title="Budget & Financial Dashboard",
    sidebar=[pn.pane.Markdown("## Filters"), select_amount_value, select_abbreviation, export_button],
    main=[pn.Tabs(("Summary", summary_tab), ("Details", details_tab))],
    header_background="#f5b907",
    accent_base_color="#f5b907",
    site="Budget and Financial Forecast",
    logo="logo.png",
)

template.servable()
