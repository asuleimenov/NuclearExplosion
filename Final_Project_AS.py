import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import plotly.express as px
import os
import seaborn as sns

# Name: Askarbek Suleimenov
# CS230: Section 4
# Data: Nuclear_Explosions.csv
# URL:

# Description:

# This project is an interactive Streamlit application designed to explore nuclear bomb detonations that occurred worldwide before the year 2000.
# It uses a detailed dataset to present information about these detonations, including their locations, yields, source countries, and purposes.
# The app provides a user-friendly interface with multiple tabs that allow users to interact with the data in various ways.
# Users can view a global map of detonation sites, analyze trends over time, and examine statistics like explosion yields and detonation reasons.
# The application integrates visualizations such as maps, pie charts, and bar charts to make the data more engaging and insightful.
# By combining filters and dynamic tools, the project offers an accessible way to investigate patterns and details behind nuclear detonations historically.

data = "nuclear_explosions.csv"
df = pd.read_csv(data)

df.rename(columns = {"WEAPON SOURCE COUNTRY":"Source Country",           # Rename the columns for the better understanding and readability [DA1]
                        "WEAPON DEPLOYMENT LOCATION":"Deployment Location",
                       "Location.Cordinates.Latitude": "Latitude",
                       "Location.Cordinates.Longitude":"Longitude",
                       "Location.Cordinates.Depth":"Depth",
                       "Data.Source":"Source",
                       "Data.Magnitude.Body":"Body Wave Magnitude",
                       "Data.Magnitude.Surface":"Surface Wave Magnitude",
                       "Data.Yeild.Lower":"Explosion Yield L",
                       "Data.Yeild.Upper":"Explosion Yield U",
                       "Data.Purpose":"Detonation Reason",
                       "Data.Name":"Name",
                       "Data.Type":"Detonation Method",
                       "Date.Day":"Day",
                       "Date.Month":"Month",
                       "Date.Year":"Year"}, inplace=True)

st.title("All Nuclear Explosions Prior to 2000")

#Making tabs based onb the information that I will provide with this site
tab1, tab2, tab3 , tab4 , tab5, tab6 , tab7 = st.tabs(["Main Page","Data Dictionary", "Filter by Year", "Map", "Weapon Source", "Detonation Reasons", "Explosion Statistics"]) #[ST1]

with tab1:
    st.title("🌍 Nuclear Bomb Detonations Explorer") #[ST2]
    st.markdown("""
        Welcome to the **Nuclear Bomb Detonation Explorer**, an interactive platform that tells the story of nuclear bomb detonations worldwide before the year 2000.
    """)

    # Display image and key metric
    bomb_pic = "bomb.png"
    col1, col2 = st.columns([2, 3])
    with col1:
        st.image(bomb_pic, use_container_width=True) #[ST4]
    with col2:
        st.metric("Total Nuclear Bombs Detonated", len(df))
        st.markdown("""
        This project helps you explore data interactively through:
        - Visualizations of global detonation locations
        - Filterable statistics by year, source, and purpose
        - In-depth analysis of explosion yields, magnitudes, and more
        """)

    # Description of tabs
    st.markdown("---")
    st.subheader("📋 Explore the Tabs")
    st.markdown("""
        - **Main Page**: Overview of the site and dataset.
        - **Data Dictionary**: Detailed breakdown of the dataset fields.
        - **Filter by Year**: View nuclear detonations from specific years.
        - **Map**: A global view of detonation locations.
        - **Weapon Source**: Analyze detonations by source countries.
        - **Detonation Reasons**: Explore the purposes behind the detonations.
        - **Explosion Statistics**: Gain insights into yields, counts, and patterns.
    """)
    st.markdown(" ")
    st.markdown("---")
    st.info("""Use the navigation tabs above to dive into the data and discover fascinating patterns and insights! """)


with tab2:
    # Title for the Data Dictionary tab
    st.title("📚 Data Dictionary")
    st.markdown("""
        Below is the cleaned and formatted dataset showing all nuclear detonations before 2000. 
        Each column represents specific details about each detonation:

        - **Source**: Source that reported the explosion event.
        - **Source Country**: Country deploying the nuclear device.
        - **Deployment Location**: Region where the nuclear device was deployed.
        - **Latitude**: Latitude position.
        - **Longitude**: Longitude position.
        - **Body Wave Magnitude**: Body wave magnitude of explosion (mb).
        - **Surface Wave Magnitude**: Surface wave magnitude of explosion (Ms).
        - **Depth**: Depth at detonation in Km (could be underground or above ground):
          - Positive = depth (below ground).
          - Negative = height (above ground).
        - **Explosion Yield L**: Explosion yield lower estimate in kilotons of TNT.
        - **Explosion Yield U**: Explosion yield upper estimate in kilotons of TNT.
        - **Detonation Reason**: Purpose of detonation (e.g., COMBAT, FMS, PNE, etc.).
        - **Name**: Name of the event or bomb.
        - **Detonation Method**: Type/method of deployment (e.g., Tower, Atmospheric).
        - **Day**: Day of detonation.
        - **Month**: Month of detonation.
        - **Year**: Year of detonation.
    """)

    # Dataframe widget [VIZ1] [ST1]
    st.subheader("Cleaned Dataset Preview")
    st.dataframe(df)

with tab3:
    st.title("📊 Filter by Year")

    st.text("Use the slider below to select a range of years. The bar chart will show the total number of nuclear bombs detonated in each year within the selected range. ")

    # Year range slider [ST2]
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    year_range = st.slider("Select Year Range:",min_year,max_year, (1945,1998), step=1)

    # [DA4] Filter data by one condition, based on the selected range
    filtered_data = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    year_counts = filtered_data["Year"].value_counts().sort_index()

    # Check if there are empty data points (years with no detonated bombs)
    if year_counts.empty: #[PY4]
        st.warning("No data available for the selected range. Please adjust the slider.")
    else:
        # Plot the bar chart using seaborn package - place that took me a lot of time
        fig, ax = plt.subplots(figsize=(10, 6)) # Initiates the chart
        sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis", ax=ax) # seaborn

        # Customizing
        ax.set_title(f"Nuclear Bombs Detonated (Years {year_range[0]} - {year_range[1]})", fontsize=16)
        ax.set_xlabel("Year", fontsize=14)
        ax.set_ylabel("Number of Bombs", fontsize=14)

        ax.tick_params(axis='x', rotation=90)  # Rotate the x-axis labels for better readability
        plt.xticks(ticks=range(0, len(year_counts), 5), labels=year_counts.index[::5])  # Show every 5th year

        ax.grid(axis='y', linestyle="--", alpha=0.7) # Adds the gridlines, and customizes them
        st.pyplot(fig)

        # Display raw data summary
        st.subheader("Data Summary")
        st.write(year_counts)

with tab4:
    st.title("🌍 Global Map of Nuclear Detonations")

    st.markdown("""
        Select a map type from the sidebar to explore nuclear detonation locations worldwide:

        - **Simple Map**: Basic map showing detonation points.
        - **Scatterplot Map**: Layered map with denser points showing darker colors.
        - **Custom Tooltip Map**: Points with country flags shown on hover.
    """)

    # [ST2] Sidebar widget for map selection
    selected_map = st.sidebar.radio("Please select the map", ["", "Simple", "Scatterplot", "Custom Tooltip"])

    map_data = df[["Latitude", "Longitude", "Source Country"]].dropna()  # Drop rows with missing values [DA1]
    map_data.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)  # Rename columns for PyDeck compatibility [DA4]

    if selected_map == "Simple":
        st.title("🗺️ Simple Map")
        # The most basic map, st.map(df)
        st.map(map_data)

    elif selected_map == "Scatterplot":
        st.title("📍 Scatterplot Map")

        view_state = pdk.ViewState(
            latitude=map_data["lat"].mean(),  # The latitude of the view center [PY2]
            longitude=map_data["lon"].mean(),  # The longitude of the view center [PY2]
            zoom=1,
            pitch=0
        )

        # Create a map layer with the given coordinates
        layer1 = pdk.Layer(
            type='ScatterplotLayer',  # Layer type [VIZ3]
            data=map_data,
            get_position='[lon, lat]',
            get_radius=20000,
            get_color=[0, 200, 0],
            pickable=True  # Enable tooltips [ST3]
        )

        layer2 = pdk.Layer(
            type='ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_radius=10000,
            get_color=[0, 0, 255],
            pickable=True
        )

        tool_tip = {
            "html": "<b>Country:</b> {Source Country}",
            "style": {"backgroundColor": "orange", "color": "white"}
        }

        scatter_map = pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v12',
            initial_view_state=view_state,
            layers=[layer1, layer2],  # The following layer would be on top of the previous layers [VIZ4]
            tooltip=tool_tip
        )

        st.pydeck_chart(scatter_map)

    elif selected_map == "Custom Tooltip":
        st.title("🖼️ Custom Tooltip Map")

        view_state = pdk.ViewState(
            latitude=map_data["lat"].mean(),
            longitude=map_data["lon"].mean(),
            zoom=1,
            pitch=0
        )

        # Updated dictionary mapping countries to their flag URLs
        # This took me the longest time to match every country, as it worked for some countries, but not all. [PY5]
        flag_urls = {
            "usa": "https://flagcdn.com/us.svg",
            "ussr": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_of_the_Soviet_Union.svg",
            "uk": "https://flagcdn.com/gb.svg",
            "france": "https://flagcdn.com/fr.svg",
            "china": "https://flagcdn.com/cn.svg",
            "pakist": "https://flagcdn.com/pk.svg",
            "india": "https://flagcdn.com/in.svg",
        }

        # Normalize the Source Country column and map to flag URLs
        # That's the problem that I had, and some flags didn't show up [DA1]
        map_data["Source Country"] = map_data["Source Country"].str.strip().str.lower()  # [PY1]
        map_data["Flag"] = map_data["Source Country"].map(flag_urls)  # Map flags to countries [DA4]

        icon_layer = pdk.Layer(
            type="ScatterplotLayer",
            data=map_data,
            get_position='[lon, lat]',
            get_radius=20000,
            get_color=[0, 100, 255, 180],  # Blue color
            pickable=True  # Enable interaction [ST3]
        )

        # Tooltip that displays the country name and flag
        tool_tip = {
            "html": """
                <b>Country:</b> {Source Country}<br>
                <img src='{Flag}' width='80' height='50'>
            """,
            "style": {"backgroundColor": "black", "color": "white"}
        }

        # Create the map
        tooltip_map = pdk.Deck(
            map_style='mapbox://styles/mapbox/navigation-day-v1',
            layers=[icon_layer],
            initial_view_state=view_state,
            tooltip=tool_tip  # Enhanced tooltips for better user experience [ST3]
        )

        st.pydeck_chart(tooltip_map)

with tab5:
    st.title("🔎 Weapon Source Analysis")

    st.markdown("""
        This section explores the contribution of each country to nuclear detonations.

        - The chart below shows the percentage of detonations by source country.
        - Smaller contributors (China, India, Pakistan, and UK) are combined into "Other Countries".
    """)

    # [DA2] Group data by Source Country and count occurrences, to count total detonations
    detonations_by_country = map_data.groupby("Source Country").size().reset_index(name="Detonation Count")

    # [DA7] Normalize country names for consistent matching
    detonations_by_country["Source Country"] = detonations_by_country["Source Country"].str.strip().str.lower()

    # [DA9] Use a lambda function to combine smaller contributors into "Other Countries"
    other_countries = ["china", "india", "pakist", "uk"]
    detonations_by_country["Source Country"] = detonations_by_country["Source Country"].apply(
        lambda x: "Other Countries" if x in other_countries else x
    ) # [DA1] Updates the "Source Country" column so that smaller contributors are grouped together

    # Regroup to merge "Other Countries" counts
    detonations_by_country = detonations_by_country.groupby("Source Country", as_index=False).sum()

    # [DA3] Sort the results by Detonation Count in descending order
    detonations_by_country = detonations_by_country.sort_values(by="Detonation Count", ascending=False)

    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        detonations_by_country["Detonation Count"],
        labels=detonations_by_country["Source Country"].str.title(),  # Capitalize labels for better display
        autopct='%1.1f%%',  # Show percentage values
        startangle=140  # Rotate the pie chart for better readability
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # [ST4] Custom legend placement for a better readability
    ax.legend(
        wedges,
        detonations_by_country["Source Country"].str.title(),
        title="Countries",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1) # Anchors the legend box outside of pie chart, on the right side.
    )

    # [VIZ5] Pie chart visualization with percentages
    st.pyplot(fig)

    st.markdown("""
        **Key Insights:**
        - The pie chart highlights the proportion of detonations conducted by major countries.
        - "Other Countries" includes smaller contributors like China, India, Pakistan, and UK.
    """) # Add the context

with tab6:
    st.title("💥 Detonation Reasons")

    # Explanation, all found in the web
    st.markdown("""
        This section explores the reasons for nuclear detonations, such as testing, combat, and other purposes.

        ### Common Detonation Reasons:
        - **Wr**: Weapon-related tests conducted to assess the performance, reliability, and safety of nuclear weapons.
        - **We**: Weapon-effect tests to study the effects of nuclear detonations on structures and environments.
        - **Pne**: Peaceful nuclear explosions intended for non-military uses such as mining or excavation.
        - **Combat**: Actual use of nuclear weapons during wartime.
        - **Se**: Safety experiments to ensure that accidental detonation does not occur.
        - **Fms**: Fail-safe tests designed to assess the reliability of safety mechanisms.
        - **Sam**: Simulated armed missile tests.
        - **Plo**: Plutonium-based tests for research and development purposes.

        Use the interactive filters below to explore the data based on detonation reasons.
    """)

    # Count occurrences of each detonation reason
    detonation_counts = df.groupby("Detonation Reason").size().reset_index(name="Count")
    detonation_counts = detonation_counts.sort_values(by="Count", ascending=False)

    # Filter out single-digit reasons and keep top reasons, including "Combat", even though it's not a top reason
    filtered_reasons = detonation_counts[detonation_counts["Count"] >= 10]  # Threshold for significance, can be any number, but I did 10
    significant_reasons = filtered_reasons["Detonation Reason"].tolist()
    if "Combat" not in significant_reasons:
        significant_reasons.append("Combat")  # Ensure "Combat" is there

    # [ST3] Multiselect widget for user interaction
    selected_reasons = st.multiselect(
        "Select Detonation Reasons to Filter:",
        options=significant_reasons,
        default=significant_reasons  # Default to showing all significant reasons
    )

    # [DA5] Filter data by multiple conditions using .isin()
    filtered_data = df[df["Detonation Reason"].isin(selected_reasons)].dropna(subset=["Detonation Reason"])  # Clean NaN rows

    # Group Data by Detonation Reason and Count Occurrences
    reasons_summary = filtered_data.groupby("Detonation Reason").size().reset_index(name="Count")
    reasons_summary = reasons_summary.sort_values(by="Count", ascending=False)

    # [VIZ3] Display filtered data as a table
    st.markdown("### Filtered Detonation Data")
    st.dataframe(filtered_data)

    st.markdown("### Detonation Reason Summary")
    st.table(reasons_summary)

    st.markdown("""
        **Key Insights:**
        - The table above highlights the number of detonations for each selected reason.
        - Use the filter to narrow down results and explore specific reasons in depth.
    """)

with tab7:
    st.title("📈 Explosion Statistics")

    st.markdown("""
        This section analyzes nuclear detonations based on their explosion yield. 
        You can identify high-yield detonations and visualize them on an interactive scatterplot map.
    """)

    # Slider to adjust the yield threshold
    yield_threshold = st.slider(
        "Set the Explosion Yield Threshold (kilotons):",
        min_value=int(df["Explosion Yield L"].min()),
        max_value=int(df["Explosion Yield L"].max()),
        value=1000,
        step=10
    )

    # [DA8] Identify high-yield detonations using iterrows
    high_yield_rows = []
    for _, row in df.iterrows():
        if row["Explosion Yield L"] > yield_threshold:
            high_yield_rows.append(row)

    # Create a DataFrame for high-yield detonations
    high_yield_df = pd.DataFrame(high_yield_rows)

    # Display high-yield detonations DataFrame
    st.markdown(f"### Detonations with Yield Above {yield_threshold} Kilotons")
    if not high_yield_df.empty:
        st.dataframe(high_yield_df)
    else:
        st.info("No detonations found with yields above the specified threshold.")

    # Scatterplot Map for high-yield Detonations
    st.markdown("### Scatterplot Map of High-Yield Detonations")
    scatter_data = high_yield_df[["Latitude", "Longitude", "Explosion Yield L"]].dropna()
    scatter_data.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)

    if not scatter_data.empty:
        view_state = pdk.ViewState(
            latitude=scatter_data["lat"].mean(),
            longitude=scatter_data["lon"].mean(),
            zoom=1,
            pitch=0
        )

        # Adjust the radius dynamically based on the yield and scale
        scatter_data["scaled_radius"] = scatter_data["Explosion Yield L"] / 10  # Scale for better visibility, can be edited

        scatter_layer = pdk.Layer(
            type="ScatterplotLayer",
            data=scatter_data,
            get_position="[lon, lat]",
            get_radius="scaled_radius",
            radius_scale=100,  # Increased scaling factor for larger visibility
            get_color=[255, 0, 0, 160],  # Red color for high-yield detonations
            pickable=True
        )

        scatter_map = pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state=view_state,
            layers=[scatter_layer],
            tooltip={
                "html": "<b>Explosion Yield:</b> {Explosion Yield L} kilotons",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }
        )
        st.pydeck_chart(scatter_map)
    else:
        st.info("No detonations meet the criteria for the scatterplot map.")

    st.markdown("""
        **Key Insights:**
        - Use the slider above to adjust the explosion yield threshold and explore high-yield detonations.
        - The scatterplot map dynamically updates to reflect detonations exceeding the selected threshold.
        - Point size scales with the explosion yield for better visibility.
    """)
























