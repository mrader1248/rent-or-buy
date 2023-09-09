import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.subplots import make_subplots

# blue1 = "#7890cd"
# blue2 = "#3949ab"
# blue3 = "#2a3990"
# blue4 = "#212d74"
# red1 = "#f06292"
# red2 = "#d23369"
# red3 = "#9c254d"

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        html.Label("Eigenkapital"),
                                        dbc.Input(
                                            id="equity",
                                            type="number",
                                            value=400000,
                                            step=10000,
                                        ),
                                    ],
                                    title="Mieter/Eigentümer",
                                ),
                                dbc.AccordionItem(
                                    [
                                        html.Label("Preis der Immobilie"),
                                        dbc.Input(
                                            id="property-price",
                                            type="number",
                                            value=800000,
                                            step=10000,
                                        ),
                                        html.Br(),
                                        html.Label("Neben- und Adaptierungskosten"),
                                        dbc.Input(
                                            id="additional-costs",
                                            type="number",
                                            value=40000,
                                            step=1000,
                                        ),
                                        html.Br(),
                                        html.Label(
                                            "Reale jährliche Wertsteigerung in Prozent"
                                        ),
                                        dbc.Input(
                                            id="property-accretion-percent",
                                            type="number",
                                            value=0.5,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                        html.Label(
                                            "Jährliche Instandhaltungskosten in Prozent des Objektwerts"
                                        ),
                                        dbc.Input(
                                            id="maintenance-costs-percent",
                                            type="number",
                                            value=1,
                                            step=0.1,
                                        ),
                                    ],
                                    title="Immobilie",
                                ),
                                dbc.AccordionItem(
                                    [
                                        html.Label("Kreditzins in Prozent"),
                                        dbc.Input(
                                            id="interest-rate-loan-percent",
                                            type="number",
                                            value=4.0,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                        html.Label("Laufzeit in Jahren"),
                                        dbc.Input(
                                            id="loan-period-years",
                                            type="number",
                                            value=30,
                                        ),
                                    ],
                                    title="Kredit",
                                ),
                                dbc.AccordionItem(
                                    [
                                        html.Label("Inflationsrate in Prozent"),
                                        dbc.Input(
                                            id="inflation-percent",
                                            type="number",
                                            value=2,
                                            step=0.1,
                                        ),
                                    ],
                                    title="Wirtschaftslage",
                                ),
                            ]
                        ),
                    ],
                    md=4,
                ),
                dbc.Col([dcc.Graph(id="graph-cost")], md=8),
            ],
            align="center",
        ),
    ],
)


@callback(
    Output("graph-cost", "figure"),
    [
        Input("equity", "value"),
        Input("property-price", "value"),
        Input("additional-costs", "value"),
        Input("interest-rate-loan-percent", "value"),
        Input("loan-period-years", "value"),
        Input("maintenance-costs-percent", "value"),
        Input("property-accretion-percent", "value"),
        Input("inflation-percent", "value"),
    ],
)
def update_graph_cost(
    equity,
    property_price,
    additional_costs,
    interest_rate_loan_percent,
    loan_period_years,
    maintenance_costs_percent,
    property_accretion_percent,
    inflation_percent,
):
    interest_rate_loan = interest_rate_loan_percent / 100
    property_accretion = property_accretion_percent / 100
    inflation = inflation_percent / 100

    t = list(range(loan_period_years + 1))

    loan_nominal = [property_price + additional_costs - equity]
    loan_installment = (
        loan_nominal[0]
        * ((1 + interest_rate_loan) ** loan_period_years * interest_rate_loan)
        / ((1 + interest_rate_loan) ** loan_period_years - 1)
    )
    for j in range(1, len(t)):
        loan_nominal.append(
            loan_nominal[-1] * (1 + interest_rate_loan) - loan_installment
        )

    loan = [loan_nominal[j] / (1 + inflation) ** j for j in range(len(t))]

    loan_interest_costs = [x * interest_rate_loan for x in loan]

    property_value = [property_price]
    for j in range(1, len(t)):
        property_value.append(property_value[-1] * (1 + property_accretion))

    maintenance_costs = [x * maintenance_costs_percent / 100 for x in property_value]

    fig = make_subplots(rows=2, cols=1)

    fig.append_trace(go.Scatter(x=t, y=loan_nominal, name="Kredit"), row=1, col=1)
    fig.append_trace(
        go.Scatter(x=t, y=property_value, name="Immobilienwert"), row=1, col=1
    )

    fig.append_trace(
        go.Scatter(
            x=t,
            y=loan_interest_costs,
            fill="tozeroy",
            name="Kreditzinskosten",
        ),
        row=2,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=[loan_interest_costs[j] + maintenance_costs[j] for j in range(len(t))],
            fill="tonexty",
            name="Instandhaltungskosten",
        ),
        row=2,
        col=1,
    )
    fig.update_yaxes(title_text="Kosten", row=2, col=1)

    fig.update_layout(width=800, height=800)

    return fig


def main():
    app.run(debug=True)
