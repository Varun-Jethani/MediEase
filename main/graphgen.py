from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

password = "0VegOnJDwJeRKTiF"

uri = f"mongodb+srv://varunjethani2444:{password}@cluster0.biqo3x8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri, server_api=ServerApi('1'))


db = client['hospital_data']





def docavailability():
    doctors_availability = db.doctors.find({}, {'name': 1, 'availability': 1})

    doctors_availability = list(doctors_availability)

    # Initialize dictionaries to store availability counts
    availability_counts = {}

    # Aggregate availability data
    for doctor in doctors_availability:
        for availability in doctor['availability']:
            day = availability['day']
            for time_slot in availability['time_slots']:
                if (day, time_slot) in availability_counts:
                    availability_counts[(day, time_slot)] += 1
                else:
                    availability_counts[(day, time_slot)] = 1

    # Extract days of the week and time slots
    days_of_week = sorted(set(day for day, _ in availability_counts.keys()))
    time_slots = sorted(set(time_slot for _, time_slot in availability_counts.keys()))

    # Create a grid of availability counts
    availability_grid = np.zeros((len(time_slots), len(days_of_week)))
    for i, day in enumerate(days_of_week):
        for j, time_slot in enumerate(time_slots):
            availability_grid[j, i] = availability_counts.get((day, time_slot), 0)

    # Create traces for heatmap
    trace = go.Heatmap(
        z=availability_grid,
        x=days_of_week,
        y=time_slots,
        colorscale='Viridis'
    )

    # Create layout
    layout = go.Layout(
        title='Doctor Availability',
        xaxis=dict(title='Day of Week'),
        yaxis=dict(title='Time Slot')
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)

    # Output plot to HTML file
    #pio.write_html(fig, 'doctor_availability.html')
    return fig.to_html(full_html= False, include_plotlyjs='cdn', div_id = "heatmap")

def reasonforvisit():
    patients_collection = db["patients"]

    # Define a function to extract reasons for hospital visits
    def get_reasons_for_hospital_visits():
        reasons_count = {}
        for patient in patients_collection.find():
            for record in patient["health_records"]:
                reason = record["diagnosis"]
                if reason in reasons_count:
                    reasons_count[reason] += 1
                else:
                    reasons_count[reason] = 1
        return reasons_count

    # Get reasons for hospital visits
    reasons_data = get_reasons_for_hospital_visits()

    # Prepare data for Plotly pie chart
    reasons = list(reasons_data.keys())
    visits = list(reasons_data.values())

    # Create a pie chart for reasons for hospital visits
    fig = go.Figure(data=[go.Pie(labels=reasons, values=visits)])

    # Update layout
    fig.update_layout(
        title='Reasons for Hospital Visits'
    )

    # Update pie chart properties
    fig.update_traces(
        textinfo='percent+label',  # Display percentage and label
        insidetextfont=dict(size=20)  # Set font size for the percentage
    )

    # Save plot to HTML file
    #fig.write_html('reasons_for_hospital_visits_pie_chart_mng.html')
    return fig.to_html(full_html= False, include_plotlyjs='cdn', div_id = "piechrt" )#include_plotlyjs='cdn'


def proceduresovertime():
    date = pd.date_range(start='2024-01-01', periods=100, end=datetime.today().strftime('%Y-%m-%d'))
    procedure_trends = np.random.randint(50, 150, size=100)

    # Create line plot
    fig = go.Figure(data=go.Scatter(x=date, y=procedure_trends, mode='lines'))

    # Update layout
    fig.update_layout(
    title="Procedure Trends Over Time",
    xaxis_title="Date",
    yaxis_title="Total Procedures",
    # template="plotly_dark"
    )

    # Show plot
    return fig.to_html(full_html= False, include_plotlyjs='cdn', div_id = "linechrt")


def generate_graph():
    html = '''{% extends 'main/base.html' %}
    {% load static %}
    {% block title %}
    Doctor Availability
    {% endblock title %}
    
    {% block Styles %}<link rel='stylesheet', href = "{% static 'assets/css/sum.css' %}"/>{% endblock Styles %}

    {% block content %}
    <div class="container  dash">
    '''
    html += reasonforvisit()
    # html += docavailability()
    html += proceduresovertime()
    html += '''
    </div>
    {% endblock content %}'''
    
    f= open('main/templates/main/graph.html', 'w') 
    f.write(html)
    f.close()
