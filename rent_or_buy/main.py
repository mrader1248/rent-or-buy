import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

blue1 = "#7890cd"
blue2 = "#3949ab"
blue3 = "#2a3990"
blue4 = "#212d74"
red1 = "#f06292"
red2 = "#d23369"
red3 = "#9c254d"


app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])
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
                                        dbc.Label("Eigenkapital"),
                                        dbc.Input(
                                            id="equity",
                                            type="number",
                                            value=400000,
                                            step=10000,
                                        ),
                                        html.Br(),
                                    ],
                                    title="Mieter/Eigentümer",
                                ),
                                dbc.AccordionItem(
                                    [
                                        dbc.Label("Preis der Immobilie"),
                                        dbc.Input(
                                            id="property-price",
                                            type="number",
                                            value=800000,
                                            step=10000,
                                        ),
                                        html.Br(),
                                        dbc.Label("Neben- und Adaptierungskosten"),
                                        dbc.Input(
                                            id="additional-costs",
                                            type="number",
                                            value=40000,
                                            step=1000,
                                        ),
                                        html.Br(),
                                        dbc.Label(
                                            "Reale jährliche Wertsteigerung in Prozent"
                                        ),
                                        dbc.Input(
                                            id="property-accretion-percent",
                                            type="number",
                                            value=0.5,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                        dbc.Label(
                                            "Jährliche Instandhaltungskosten in Prozent des Objektwerts"
                                        ),
                                        dbc.Input(
                                            id="maintenance-costs-percent",
                                            type="number",
                                            value=1,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                    ],
                                    title="Immobilie",
                                ),
                                dbc.AccordionItem(
                                    [
                                        dbc.Label("Kreditzins in Prozent"),
                                        dbc.Input(
                                            id="interest-rate-loan-percent",
                                            type="number",
                                            value=4.0,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                        dbc.Label("Laufzeit in Jahren"),
                                        dbc.Input(
                                            id="loan-period-years",
                                            type="number",
                                            value=30,
                                        ),
                                        html.Br(),
                                    ],
                                    title="Kredit",
                                ),
                                dbc.AccordionItem(
                                    [
                                        dbc.Label("Monatsmiete (ohne Betriebskosten)"),
                                        dbc.Input(
                                            id="rent-monthly",
                                            type="number",
                                            value=1800,
                                            step=10,
                                        ),
                                        html.Br(),
                                        dbc.Label(
                                            "Reale jährliche Mieterhöhung in Prozent"
                                        ),
                                        dbc.Input(
                                            id="rent-increase-percent",
                                            type="number",
                                            value=0.5,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                    ],
                                    title="Miete",
                                ),
                                dbc.AccordionItem(
                                    [
                                        dbc.Label("Inflationsrate in Prozent"),
                                        dbc.Input(
                                            id="inflation-percent",
                                            type="number",
                                            value=2,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                        dbc.Label(
                                            "Reale jährliche Wertsteigerung des Wertpapierdepots in Prozent"
                                        ),
                                        dbc.Input(
                                            id="depot-accretion-percent",
                                            type="number",
                                            value=3,
                                            step=0.1,
                                        ),
                                        html.Br(),
                                    ],
                                    title="Wirtschaftslage",
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Alert(
                            [
                                html.I(className="bi bi-info-circle-fill me-2"),
                                (
                                    "Die Entwicklung des Tools erfolgte nach bestem "
                                    "Wissen und Gewissen. Dennoch wird keine Haftung "
                                    "für die Korrektheit der Ergebnisse übernommen. "
                                    "Dieses Tool stellt keine Anlageberatung dar."
                                ),
                            ],
                            color="info",
                            dismissable=True,
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
        Input("rent-monthly", "value"),
        Input("rent-increase-percent", "value"),
        Input("depot-accretion-percent", "value"),
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
    rent_monthly,
    rent_increase_percent,
    depot_accretion_percent,
):
    if any(
        x is None
        for x in [
            equity,
            property_price,
            additional_costs,
            interest_rate_loan_percent,
            loan_period_years,
            maintenance_costs_percent,
            property_accretion_percent,
            inflation_percent,
            rent_monthly,
            rent_increase_percent,
            depot_accretion_percent,
        ]
    ):
        raise PreventUpdate

    interest_rate_loan = interest_rate_loan_percent / 100
    property_accretion = property_accretion_percent / 100
    inflation = inflation_percent / 100
    rent_increase = rent_increase_percent / 100
    depot_accretion = depot_accretion_percent / 100

    t = list(range(loan_period_years + 1))

    loan_nominal = [property_price + additional_costs - equity]

    loan_installment_nominal = (
        loan_nominal[0]
        * ((1 + interest_rate_loan) ** loan_period_years * interest_rate_loan)
        / ((1 + interest_rate_loan) ** loan_period_years - 1)
    )

    for j in range(1, len(t)):
        loan_nominal.append(
            loan_nominal[-1] * (1 + interest_rate_loan) - loan_installment_nominal
        )

    loan = [loan_nominal[j] / (1 + inflation) ** j for j in range(len(t))]
    loan_installment = [
        loan_installment_nominal / (1 + inflation) ** j for j in range(len(t))
    ]

    loan_interest_costs = [x * interest_rate_loan for x in loan]

    property_value = [property_price]
    for j in range(1, len(t)):
        property_value.append(property_value[-1] * (1 + property_accretion))

    maintenance_costs = [x * maintenance_costs_percent / 100 for x in property_value]

    buy_cashflow = [-loan_installment[j] - maintenance_costs[j] for j in range(len(t))]

    rent = [12 * rent_monthly * (1 + rent_increase) ** j for j in range(len(t))]

    depot_value = [equity]
    for j in range(1, len(t)):
        depot_value.append(
            depot_value[-1] * (1 + depot_accretion) + (-buy_cashflow[j] - rent[j])
        )
    depot_profit = [x * depot_accretion for x in depot_value]

    fig = make_subplots(rows=3, cols=1)

    fig.append_trace(
        go.Scatter(
            x=t,
            y=loan,
            name="Kredit",
            line=dict(color=red3),
        ),
        row=1,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=property_value,
            name="Immobilienwert",
            fill="tonexty",
            # fillcolor=red1,
            line=dict(color=red2),
        ),
        row=1,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=depot_value,
            name="Depot Mieter",
            line=dict(color=blue4, width=2.5),
        ),
        row=1,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=[depot_value[j] + loan[j] for j in range(len(t))],
            name="Depot Mieter vs. Kredit",
            line=dict(
                dash="dash",
                color=blue4,
                width=2.5,
            ),
        ),
        row=1,
        col=1,
    )
    fig.update_yaxes(title_text="Vermögen / Verbindlichkeiten", row=1, col=1)

    fig.append_trace(
        go.Scatter(
            x=t,
            y=loan_interest_costs,
            name="Kreditzinskosten",
            fill="tozeroy",
            # fillcolor=red1,
            line=dict(color=red3),
        ),
        row=2,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=[loan_interest_costs[j] + maintenance_costs[j] for j in range(len(t))],
            name="Instandhaltungskosten",
            fill="tonexty",
            # fillcolor=red2,
            line=dict(color=red2),
        ),
        row=2,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=depot_profit,
            name="Erträge aus Depot",
            line=dict(color=blue4, width=2.5),
        ),
        row=2,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=rent,
            name="Mietkosten",
            fill="tonexty",
            # fillcolor=blue1,
            line=dict(color=blue4),
        ),
        row=2,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=[rent[j] - depot_profit[j] for j in range(len(t))],
            name="Nettokosten Mieter",
            line=dict(color=blue4, dash="dash", width=2.5),
        ),
        row=2,
        col=1,
    )
    fig.update_yaxes(title_text="Kosten", row=2, col=1)

    fig.append_trace(
        go.Scatter(
            x=t,
            y=[-loan_installment[j] for j in range(len(t))],
            name="Kreditrate",
            fill="tozeroy",
            # fillcolor=red1,
            line=dict(color=red3),
        ),
        row=3,
        col=1,
    )
    fig.append_trace(
        go.Scatter(
            x=t,
            y=buy_cashflow,
            name="Instandhaltungskosten",
            fill="tonexty",
            # fillcolor=red2,
            line=dict(color=red2),
        ),
        row=3,
        col=1,
    )

    fig.append_trace(
        go.Scatter(
            x=t,
            y=[-rent[j] for j in range(len(t))],
            name="Miete",
            line=dict(color=blue4, width=2.5),
        ),
        row=3,
        col=1,
    )

    fig.update_yaxes(title_text="Cashflow", row=3, col=1)
    fig.update_xaxes(title_text="Jahre", row=3, col=1)

    fig.update_layout(showlegend=False)
    fig.update_layout(width=800, height=800)

    return fig


def main():
    app.run(debug=True)
