import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def format_lap_time(seconds):

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{remaining_seconds:02}.{milliseconds:03}"

def format_seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes:02}:{remaining_seconds:02}"

def plot_lap_times(lap_time_df: pd.DataFrame, driver_color_map: dict):
    if lap_time_df.empty:
        st.warning("No lap data available to plot.")
        return

    lap_time_df["formatted_lap_time"] = lap_time_df["lap_duration"].apply(format_lap_time)
    lap_time_df["is_pit_out_lap"] = lap_time_df["is_pit_out_lap"].fillna(False).astype(bool)

    fig = go.Figure()

    for driver in lap_time_df["name_acronym"].unique():
        driver_data = lap_time_df[lap_time_df["name_acronym"] == driver].copy()
        driver_data = driver_data.sort_values("lap_number")

        hover_texts = [
            f"<b> {driver}: {row['driver_number']} </b><br>"
            f"Lap: {row['lap_number']}<br>"
            f"Lap Time : {row['formatted_lap_time']}"
            + ("<br> PIT" if row["is_pit_out_lap"] else "")
            for _, row in driver_data.iterrows()
        ]

        fig.add_trace(
            go.Scatter(
                x=driver_data["lap_number"],
                y=driver_data["lap_duration"],
                mode="lines+markers",
                name=driver,
                marker=dict(color=driver_color_map.get(driver, "gray"), size=8),
                line=dict(color=driver_color_map.get(driver, "gray")),
                hoverinfo="text",
                hovertext=hover_texts,
            )
        )

    fig.update_layout(
        title="Lap Times by Driver",
        xaxis_title="Lap",
        yaxis_title="Lap Time (MM:SS)",
        hovermode="closest",
        height=600,
    )

    tick_vals = sorted(lap_time_df["lap_duration"].dropna().unique())
    tick_vals = [round(val, 0) for val in tick_vals if 60 <= val <= 180]
    tick_vals = sorted(set(tick_vals))[::5]

    fig.update_yaxes(
        
        tickvals=tick_vals,
        ticktext=[format_seconds_to_mmss(val) for val in tick_vals],
    )

    return fig

COMPOUND_COLORS = {
    "SOFT": "red",
    "MEDIUM": "yellow",
    "HARD": "white",
    "INTERMEDIATE": "green",
    "WET": "blue",
    "Unknown": "gray"
}

def plot_tire_strategy(stints_df, color_map: dict):
    if stints_df.empty:
        st.warning("No stint data available to plot.")
        return
    
    fig = go.Figure()

    for _, row in stints_df.itterrows():
        compound = row["compound"].upper()
        acronym = row["name_acronym"]

        fig.add_trace(
            go.Bar(
                x=[row["lap_count"]],
                y=[acronym],
                base=row["lap_start"],
                orientation="h",
                marker=dict(color=COMPOUND_COLORS.get(compound, "gray")),
                hovertemplate=(
                    f"{acronym}: {row['driver_number']}<br>"
                    f"Compound: {compound}<br>"
                    f"Laps: {row["lap_count"]}<br>"
                    f"Start Lap: {row["lap_start"]}<br>"
                    f"End Lap: {row["lap_end"]}<br>"
                ),
                name = "",
                showlegend=False
                )
        )

        y_labels = stints_df["name_acronym"].unique()
        for acronym in y_labels:
            fig.add_annotation(
                x=-3,
                y=acronym,
                xref="x",
                yref="y",
                text=f"<b>{acronym}</b>",
                showarrow=False,
                font=dict(
                    color=color_map.get(acronym, "#AAA"),
                    size=12
                ),
                align="right",
            )
        fig.update_layout(
            title="Tire Strategy by Driver",
            xaxis_title="Lap Number",
            yaxis_title="",
            barmode="stack",
            height=600,
            margin=dict(l=120)
            
        )

        fig.update_yaxes(showticklabels=False)
    

    return fig

def plot_pit_stop(pit_stop_df: pd.DataFrame, color_map: dict):

    if pit_stop_df.empty:
        st.warning("No pit stop data available for this session.")
        return None

    pit_stop_df["driver_number"] = pit_stop_df["driver_number"].astype(str)

    
    pit_stop_df["driver_label"] = pit_stop_df["name_acronym"] + ": " + pit_stop_df["driver_number"]

    fig = px.bar(
        pit_stop_df,
        x="lap_number",
        y="pit_duration",
        color="name_acronym",
        color_discrete_map=color_map,
        hover_data={
            "driver_label": False,
            "lap_number": False, 
            "pit_duration": False,
            "name_acronym": False, 
            "driver_number": False,  
        },
        custom_data=["name_acronym", "driver_number", "lap_number", "pit_duration"],
        labels={
            "lap_number": "Lap",
            "pit_duration": "Time in pit lane (s)",
        }
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}: %{customdata[1]}</b><br>" +
                      "Lap: %{customdata[2]}<br>" +
                      "Time in pit lane (s): %{customdata[3]:.1f}<br>" +
                      "<extra></extra>"  # Removes the trace box
    )
    fig.update_layout(
        title="Pit Stop Times by Driver",
        hovermode="closest",
        barmode="group",
        height=600)
    return fig


