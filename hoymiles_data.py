import sys
import argparse
from ipaddress import ip_address
import asyncio
from flask import Flask, render_template_string
from hoymiles_wifi.dtu import DTU
import plotly.graph_objects as go
from jinja2 import Template

parser = argparse.ArgumentParser(
    prog = 'hoymiles_data.py',
    description = 'Get data from Hoymiles inverter'
    )
parser.add_argument('--dtu_ip_address', default = '', type=ip_address, required=True, help = "where DTU-IP-ADDRESS has the format aaa.bbb.ccc.ddd")
parser.add_argument('--debug', action = "store_true", default=False, required=False, help = "turn on debugging")
parser.add_argument('--test', action = "store_true", default=False, required=False, help = "use a test dataset")

args = parser.parse_args()
if args.dtu_ip_address:
    dtuIpAddress = args.dtu_ip_address
else:
    dtuIpAddress = ''

app = Flask(__name__)

async def get_dtu_data():
    if args.test:
        response = open("response_test_data.txt", "r")
    else:
        dtu = DTU(dtuIpAddress)
        response = await dtu.async_get_real_data_new()

    # Print the response to the console
    print(f"DTU Response: {response}")

    if response:
        # Assuming you want to process the first pv_data entry
        pv_data = response.pv_data[0]
        power = pv_data.power / 10.0
        energy_total = pv_data.energy_total
        energy_daily = pv_data.energy_daily
        current = pv_data.current / 10
    else:
        # Unable to get response!
        pv_data = 0
        power = 0
        energy_total = 0
        energy_daily = 0
        current = 0
    
    # Create gauge graphic
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=power,
        title={'text': "Power (W)", 'font': {'color': 'white', 'size': 15}},
        number={'valueformat': '.1f', 'font': {'size': 24}},  # Format the number to one decimal place
        gauge={'axis': {'range': [0, 420], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
               'bar': {'color': 'white'},
               'bgcolor': 'black',
               'borderwidth': 2,
               'bordercolor': 'white'},
        domain={'x': [0, 1], 'y': [0.8, 1]}  # Adjust vertical positioning
    ))

    # Add additional trace for energy daily
    fig.add_trace(go.Indicator(
        mode="number",
        value=energy_daily,
        title={'text': "Heute", 'font': {'color': 'white', 'size': 15}},
        number={'suffix': " Wh", 'font': {'size': 12}},
        domain={'x': [0, 1], 'y': [0.6, 0.7]}  # Adjust vertical positioning
    ))

    # Add additional trace for energy total
    fig.add_trace(go.Indicator(
        mode="number",
        value=energy_total,
        title={'text': "Gesamt", 'font': {'color': 'white', 'size': 15}},
        number={'suffix': " Wh", 'font': {'size': 12}},
        domain={'x': [0, 1], 'y': [0.5, 0.6]}  # Adjust vertical positioning
    ))

    # Update layout
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        margin=dict(t=50, b=0, l=0, r=0)  # Small margins around the plot
    )

    # Save the gauge graphic as an HTML div
    gauge_html = fig.to_html(full_html=False)

    # HTML template
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DTU Data</title>
        <style>
          
        </style>
    </head>
    <body>
        <div>
            {{ gauge_html | safe }} 
        </div>
    </body>
    </html>
    """)

    # Render the HTML with the gauge graphic and energy total
    html_content = template.render(gauge_html=gauge_html, energy_total=energy_total, energy_daily=energy_daily)

    return html_content

@app.route('/')
def index():
    html_content = asyncio.run(get_dtu_data())
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=args.debug)
