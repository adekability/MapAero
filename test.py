import plotly.graph_objects as go

tile_server = "http://127.0.0.1:5000/tiles/{z}/{x}/{y}.png"
lat = 54.629341
lon = 21.396067
import plotly.graph_objects as go

# Define the layout of your map
layout = go.Layout(
    mapbox=dict(
        layers=[
            dict(
                sourcetype = 'raster',
                source = [
                    tile_server  # Replace with your tile server URL
                ]
            )
        ],
        style="open-street-map",
        center=dict(lat=lat, lon=lon),
        zoom=10
    )
)

# Define the data for your map
data = [
    go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode="markers",
        marker=go.scattermapbox.Marker(size=14),
        text=["San Francisco"],
    )
]

# Create the figure
fig = go.Figure(data=data, layout=layout)

# Show the figure
fig.show()
