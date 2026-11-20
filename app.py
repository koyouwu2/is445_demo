
# IS 445 Streamlit Assignment - ID40477
# Run locally using: streamlit run app.py

import streamlit as st
import altair as alt
from vega_datasets import data

# 1. Updated Streamlit app title
st.title("Streamlit App for IS445: ID40477")

# 2. Replace this placeholder with your deployed Streamlit URL
st.text("The URL for this app is: https://is445demo-jbpyssjtfnachpjp8tsaon.streamlit.app/")

# Load Seattle weather dataset
source = data.seattle_weather()

# Weather color scale
scale = alt.Scale(
    domain=["sun", "fog", "drizzle", "rain", "snow"],
    range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"],
)

color = alt.Color("weather:N", scale=scale)

# Interactive selections
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_point(encodings=["color"])

# Top panel: Scatter plot of temperature vs. date
points = (
    alt.Chart()
    .mark_point()
    .encode(
        alt.X(
            "monthdate(date):T",
            title="Date (Month Year)"
        ),
        alt.Y(
            "temp_max:Q",
            title="Maximum Daily Temperature (C)",
            scale=alt.Scale(domain=[-5, 40]),
        ),
        color=alt.condition(
            brush, color, alt.value("lightgray")
        ),
        size=alt.Size(
            "precipitation:Q",
            scale=alt.Scale(range=[5, 200])
        ),
    )
    .properties(width=550, height=300)
    .add_params(brush)
    .transform_filter(click)
)

# Bottom panel: Bar chart of weather types
bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="weather:N",
        color=alt.condition(
            click, color, alt.value("lightgray")
        ),
    )
    .transform_filter(brush)
    .properties(width=550)
    .add_params(click)
)

# 3. Updated chart title
chart = alt.vconcat(
    points,
    bars,
    data=source,
    title="Seattle Weather - 2011 to 2013"
)

# Display charts using two themes
tab1, tab2 = st.tabs([
    "Streamlit theme (default)",
    "Altair native theme"
])

with tab1:
    st.altair_chart(
        chart,
        theme="streamlit",
        use_container_width=True
    )

with tab2:
    st.altair_chart(
        chart,
        theme=None,
        use_container_width=True
    )
