from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime



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
    availability_grid = []
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
    date = [          '2024-01-01 00:00:00',
               '2024-01-01 22:18:10.909090909',
               '2024-01-02 20:36:21.818181818',
               '2024-01-03 18:54:32.727272727',
               '2024-01-04 17:12:43.636363636',
               '2024-01-05 15:30:54.545454545',
               '2024-01-06 13:49:05.454545454',
               '2024-01-07 12:07:16.363636363',
               '2024-01-08 10:25:27.272727272',
               '2024-01-09 08:43:38.181818181',
               '2024-01-10 07:01:49.090909091',
                         '2024-01-11 05:20:00',
               '2024-01-12 03:38:10.909090909',
               '2024-01-13 01:56:21.818181818',
               '2024-01-14 00:14:32.727272727',
               '2024-01-14 22:32:43.636363636',
               '2024-01-15 20:50:54.545454545',
               '2024-01-16 19:09:05.454545454',
               '2024-01-17 17:27:16.363636363',
               '2024-01-18 15:45:27.272727272',
               '2024-01-19 14:03:38.181818182',
               '2024-01-20 12:21:49.090909091',
                         '2024-01-21 10:40:00',
               '2024-01-22 08:58:10.909090909',
               '2024-01-23 07:16:21.818181818',
               '2024-01-24 05:34:32.727272727',
               '2024-01-25 03:52:43.636363636',
               '2024-01-26 02:10:54.545454545',
               '2024-01-27 00:29:05.454545454',
               '2024-01-27 22:47:16.363636363',
               '2024-01-28 21:05:27.272727273',
               '2024-01-29 19:23:38.181818182',
               '2024-01-30 17:41:49.090909091',
                         '2024-01-31 16:00:00',
               '2024-02-01 14:18:10.909090909',
               '2024-02-02 12:36:21.818181818',
               '2024-02-03 10:54:32.727272727',
               '2024-02-04 09:12:43.636363636',
               '2024-02-05 07:30:54.545454545',
               '2024-02-06 05:49:05.454545454',
               '2024-02-07 04:07:16.363636364',
               '2024-02-08 02:25:27.272727273',
               '2024-02-09 00:43:38.181818182',
               '2024-02-09 23:01:49.090909091',
                         '2024-02-10 21:20:00',
               '2024-02-11 19:38:10.909090909',
               '2024-02-12 17:56:21.818181818',
               '2024-02-13 16:14:32.727272727',
               '2024-02-14 14:32:43.636363636',
               '2024-02-15 12:50:54.545454545',
               '2024-02-16 11:09:05.454545454',
               '2024-02-17 09:27:16.363636364',
               '2024-02-18 07:45:27.272727273',
               '2024-02-19 06:03:38.181818182',
               '2024-02-20 04:21:49.090909091',
                         '2024-02-21 02:40:00',
               '2024-02-22 00:58:10.909090909',
               '2024-02-22 23:16:21.818181818',
               '2024-02-23 21:34:32.727272727',
               '2024-02-24 19:52:43.636363637',
               '2024-02-25 18:10:54.545454546',
               '2024-02-26 16:29:05.454545455',
               '2024-02-27 14:47:16.363636364',
               '2024-02-28 13:05:27.272727273',
               '2024-02-29 11:23:38.181818182',
               '2024-03-01 09:41:49.090909091',
                         '2024-03-02 08:00:00',
               '2024-03-03 06:18:10.909090909',
               '2024-03-04 04:36:21.818181818',
               '2024-03-05 02:54:32.727272727',
               '2024-03-06 01:12:43.636363637',
               '2024-03-06 23:30:54.545454546',
               '2024-03-07 21:49:05.454545455',
               '2024-03-08 20:07:16.363636364',
               '2024-03-09 18:25:27.272727273',
               '2024-03-10 16:43:38.181818182',
               '2024-03-11 15:01:49.090909091',
                         '2024-03-12 13:20:00',
               '2024-03-13 11:38:10.909090909',
               '2024-03-14 09:56:21.818181818',
               '2024-03-15 08:14:32.727272728',
               '2024-03-16 06:32:43.636363637',
               '2024-03-17 04:50:54.545454546',
               '2024-03-18 03:09:05.454545455',
               '2024-03-19 01:27:16.363636364',
               '2024-03-19 23:45:27.272727273',
               '2024-03-20 22:03:38.181818182',
               '2024-03-21 20:21:49.090909091',
                         '2024-03-22 18:40:00',
               '2024-03-23 16:58:10.909090909',
               '2024-03-24 15:16:21.818181818',
               '2024-03-25 13:34:32.727272728',
               '2024-03-26 11:52:43.636363637',
               '2024-03-27 10:10:54.545454546',
               '2024-03-28 08:29:05.454545455',
               '2024-03-29 06:47:16.363636364',
               '2024-03-30 05:05:27.272727273',
               '2024-03-31 03:23:38.181818182',
               '2024-04-01 01:41:49.090909091',
                         '2024-04-02 00:00:00']
    procedure_trends = [64, 111, 88, 107, 107, 101, 115,
                         60, 141, 101, 106, 50, 54, 96, 121,
                            59, 99, 78, 51, 50, 104, 142, 108,
                             100, 89, 114, 122, 136, 108, 63, 103,
                               50, 117, 101, 59, 106, 87, 103, 149, 125,
                                 133, 112, 62, 94, 102, 139, 58, 90, 57, 54,
                                   134, 126, 94, 130, 129, 77, 135, 79, 70, 98,
                                     148, 131, 66, 78, 132, 74, 94, 107, 71, 53, 149,
                                       71, 97, 101, 146, 56, 115, 86, 103, 100, 68, 129, 149,
                                         60, 145, 147, 119, 147, 84, 83, 122, 68, 111, 68, 74,
                                           76, 128, 61, 109, 54]

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
    html = '''
    <div class="container  dash">
    '''
    html += reasonforvisit()
    # html += docavailability()
    html += proceduresovertime()
    html += '''
    </div>
    '''
    
    return html
