import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Family Travel Cost & Comparison Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .stApp {
        background-color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧳 Family Travel Cost & Comparison Dashboard")
st.markdown("An interactive platform to explore, filter, compare, and calculate family travel budgets globally.")

# --- DATA LOADING (25 Destinations) ---
@st.cache_data
def load_data():
    full_data = {
        "Destination": [
            # Domestic (12)
            "Goa", "Manali", "Jaipur", "Kerala", "Udaipur", "Shimla", 
            "Andaman", "Leh Ladakh", "Srinagar", "Varanasi", "Munnar", "Coorg",
            # International (13)
            "Maldives", "Valencia", "Lisbon", "Paris", "Copenhagen", "Bali", 
            "Tokyo", "Dubai", "Singapore", "Bangkok", "London", "Rome", "Istanbul"
        ],
        "Type": [
            "Domestic", "Domestic", "Domestic", "Domestic", "Domestic", "Domestic",
            "Domestic", "Domestic", "Domestic", "Domestic", "Domestic", "Domestic",
            "International", "International", "International", "International", "International", "International",
            "International", "International", "International", "International", "International", "International", "International"
        ],
        "Latitude": [
            15.2993, 32.2432, 26.9124, 10.8505, 24.5854, 31.1048,
            11.7401, 34.1526, 34.0837, 25.3176, 10.0889, 12.3375,
            3.2028, 39.4699, 38.7223, 48.8566, 55.6761, -8.4095,
            35.6762, 25.2048, 1.3521, 13.7563, 51.5074, 41.9028, 41.0082
        ],
        "Longitude": [
            74.1240, 77.1892, 75.7873, 76.2711, 73.7125, 77.1734,
            92.6586, 77.5771, 74.7973, 82.9739, 77.0595, 75.8069,
            73.2207, -0.3763, -9.1393, 2.3522, 12.5683, 115.1889,
            139.6503, 55.2708, 103.8198, 100.5018, -0.1278, 12.4964, 28.9784
        ],
        "Flight_Cost_Per_Person": [
            4000, 4500, 3500, 4000, 3800, 3000,
            9000, 7000, 6000, 3000, 3500, 3200,
            25000, 38000, 36000, 42000, 45000, 22000,
            48000, 20000, 24000, 16000, 52000, 40000, 30000
        ],
        "Hotel_Cost_Per_Night": [
            3500, 3200, 3000, 3200, 4000, 2800,
            4500, 3500, 3800, 2200, 2800, 3000,
            18000, 9500, 9000, 14000, 16000, 6000,
            13000, 11000, 15000, 5000, 18000, 12500, 8000
        ],
        "Daily_Expenses_Per_Person": [
            1500, 1100, 1200, 1200, 1500, 1000,
            1800, 1400, 1300, 800, 1000, 1100,
            6000, 3800, 3500, 5500, 6000, 2200,
            5000, 5000, 5500, 2500, 6500, 4800, 3200
        ],
        "Image_URL": [
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=500",
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=500",
            "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=500",
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=500",
            "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=500",
            "https://images.unsplash.com/photo-1562670108-a5b6c28f9d0c?w=500",
            "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=500",
            "https://images.unsplash.com/photo-1593181629936-11c609b8db9b?w=500",
            "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?w=500",
            "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=500",
            "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=500",
            "https://images.unsplash.com/photo-1598970434795-0c54fe7c0648?w=500",
            "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=500",
            "https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=500",
            "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=500",
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500",
            "https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=500",
            "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=500",
            "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=500",
            "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=500",
            "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=500",
            "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=500",
            "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=500",
            "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=500",
            "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=500"
        ]
    }
    
    try:
        df_file = pd.read_csv("travel_data.csv")
        df_file.columns = df_file.columns.str.strip().str.replace('"', '').str.replace("'", "")
        
        rename_map = {}
        for col in df_file.columns:
            c_clean = col.lower()
            if c_clean in ["destination", "destinations", "place", "city"]:
                rename_map[col] = "Destination"
            elif c_clean in ["type", "category", "scope"]:
                rename_map[col] = "Type"
            elif "flight" in c_clean:
                rename_map[col] = "Flight_Cost_Per_Person"
            elif "hotel" in c_clean:
                rename_map[col] = "Hotel_Cost_Per_Night"
            elif "daily" in c_clean or "expense" in c_clean:
                rename_map[col] = "Daily_Expenses_Per_Person"

        df_file = df_file.rename(columns=rename_map)

        if "Latitude" not in df_file.columns or "Image_URL" not in df_file.columns:
            coords = pd.DataFrame({
                "Destination": full_data["Destination"],
                "Latitude": full_data["Latitude"],
                "Longitude": full_data["Longitude"],
                "Image_URL": full_data["Image_URL"]
            })
            df_file = pd.merge(df_file, coords, on="Destination", how="left")
            
        data_to_use = df_file
    except Exception:
        data_to_use = pd.DataFrame(full_data)

    data_to_use["Total_Cost_4P_5D"] = (
        (data_to_use["Flight_Cost_Per_Person"] * 4) + 
        (data_to_use["Hotel_Cost_Per_Night"] * 5) + 
        (data_to_use["Daily_Expenses_Per_Person"] * 4 * 5)
    )
    
    return data_to_use

df = load_data()

# --- HIGH-CONTRAST COLOR PALETTE ---
COLOR_MAP = {
    "Domestic": "#2563EB",       # Vibrant Blue
    "International": "#FF0055"   # Bright Neon Pink/Magenta
}

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎯 Filter Options")

travel_scope = st.sidebar.multiselect(
    "Select Travel Scope:", 
    options=df["Type"].unique(), 
    default=df["Type"].unique()
)

max_budget_limit = int(df["Total_Cost_4P_5D"].max())
min_budget_limit = int(df["Total_Cost_4P_5D"].min())

selected_max_budget = st.sidebar.slider(
    "Filter by Max Budget (4 People / 5 Days):",
    min_value=min_budget_limit,
    max_value=max_budget_limit,
    value=max_budget_limit,
    step=5000
)

filtered_df = df[
    (df["Type"].isin(travel_scope)) & 
    (df["Total_Cost_4P_5D"] <= selected_max_budget)
]

# --- MAIN TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📊 Cost Comparison & Data", "🗺️ Interactive Map Explorer", "🧮 Custom Trip Calculator & Exporter"])

# TAB 1
with tab1:
    st.subheader("Overview & Cost Breakdown")
    
    if filtered_df.empty:
        st.warning("No destinations match your filter criteria. Adjust the budget slider or scope on the sidebar!")
    else:
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f'<div class="metric-card"><h4>Total Destinations</h4><h2>{len(filtered_df)}</h2></div>', unsafe_allow_html=True)
        with col_m2:
            cheapest = filtered_df.loc[filtered_df["Total_Cost_4P_5D"].idxmin()]["Destination"]
            st.markdown(f'<div class="metric-card"><h4>Most Affordable</h4><h2>{cheapest}</h2></div>', unsafe_allow_html=True)
        with col_m3:
            priciest = filtered_df.loc[filtered_df["Total_Cost_4P_5D"].idxmax()]["Destination"]
            st.markdown(f'<div class="metric-card"><h4>Most Premium</h4><h2>{priciest}</h2></div>', unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("Total Estimated Cost (4-Person Family, 5-Day Stay)")
        fig_bar = px.bar(
            filtered_df,
            x="Destination",
            y="Total_Cost_4P_5D",
            color="Type",
            color_discrete_map=COLOR_MAP,
            text_auto='.2s',
            title="Comparison of Total Expenses per Destination (₹)",
            labels={"Total_Cost_4P_5D": "Total Cost (₹)"},
            barmode="group"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Cost Component Breakdown Per Person / Night")
        melted_df = filtered_df.melt(
            id_vars=["Destination", "Type"], 
            value_vars=["Flight_Cost_Per_Person", "Hotel_Cost_Per_Night", "Daily_Expenses_Per_Person"],
            var_name="Cost_Type", 
            value_name="Cost_Amount"
        )
        fig_grouped = px.bar(
            melted_df,
            x="Destination",
            y="Cost_Amount",
            color="Cost_Type",
            color_discrete_sequence=["#3B82F6", "#10B981", "#F59E0B"],
            barmode="stack",
            title="Flight vs. Hotel vs. Daily Expense Share"
        )
        st.plotly_chart(fig_grouped, use_container_width=True)

        st.subheader("📋 Destination Raw Data")
        st.dataframe(filtered_df.drop(columns=["Image_URL"], errors="ignore"), use_container_width=True)

# TAB 2
with tab2:
    st.subheader("🗺️ Global Destination Pin Map")
    st.write("Hover over any pin on the map to compare prices across Europe, Asia, and India.")
    
    if not filtered_df.empty:
        try:
            fig_map = px.scatter_map(
                filtered_df,
                lat="Latitude",
                lon="Longitude",
                hover_name="Destination",
                hover_data=["Type", "Flight_Cost_Per_Person", "Hotel_Cost_Per_Night", "Daily_Expenses_Per_Person"],
                color="Type",
                color_discrete_map=COLOR_MAP,
                size="Total_Cost_4P_5D",
                zoom=1.2,
                height=550
            )
            fig_map.update_layout(map_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        except AttributeError:
            fig_map = px.scatter_mapbox(
                filtered_df,
                lat="Latitude",
                lon="Longitude",
                hover_name="Destination",
                hover_data=["Type", "Flight_Cost_Per_Person", "Hotel_Cost_Per_Night", "Daily_Expenses_Per_Person"],
                color="Type",
                color_discrete_map=COLOR_MAP,
                size="Total_Cost_4P_5D",
                zoom=1.2,
                height=550
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

# TAB 3
with tab3:
    st.subheader("🧮 Interactive Custom Budget Builder")
    st.write("Customize family size, duration, and travel style for any destination.")
    
    calc_col1, calc_col2 = st.columns([1, 1])
    
    with calc_col1:
        selected_dest = st.selectbox("Choose Destination:", filtered_df["Destination"].unique() if not filtered_df.empty else df["Destination"].unique())
        num_family = st.number_input("Number of Family Members:", min_value=1, max_value=15, value=4)
        num_days = st.number_input("Number of Travel Days:", min_value=1, max_value=60, value=5)
        travel_style = st.select_slider("Travel Style / Tier:", options=["Budget", "Standard", "Luxury"], value="Standard")
    
    style_multiplier = 0.8 if travel_style == "Budget" else (1.5 if travel_style == "Luxury" else 1.0)
    
    dest_row = df[df["Destination"] == selected_dest].iloc[0]
    
    custom_flight = dest_row["Flight_Cost_Per_Person"] * num_family
    custom_hotel = dest_row["Hotel_Cost_Per_Night"] * num_days * style_multiplier
    custom_expenses = dest_row["Daily_Expenses_Per_Person"] * num_family * num_days * style_multiplier
    custom_total = custom_flight + custom_hotel + custom_expenses
    
    with calc_col2:
        if "Image_URL" in dest_row and pd.notna(dest_row["Image_URL"]):
            st.image(dest_row["Image_URL"], caption=f"Destination View: {selected_dest}", use_container_width=True)
            
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #10B981;">
            <h3>Calculated Budget for {selected_dest}</h3>
            <h2>₹{custom_total:,.2f}</h2>
            <p><b>Tier:</b> {travel_style} | <b>Travelers:</b> {num_family} | <b>Duration:</b> {num_days} Days</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"- ✈️ **Flight Costs Total:** ₹{custom_flight:,.2f}")
        st.write(f"- 🏨 **Hotel Costs ({num_days} nights):** ₹{custom_hotel:,.2f}")
        st.write(f"- 🍽️ **Daily Expenses Total:** ₹{custom_expenses:,.2f}")
        
        export_df = pd.DataFrame([{
            "Destination": selected_dest,
            "Scope": dest_row["Type"],
            "Travelers": num_family,
            "Days": num_days,
            "Style": travel_style,
            "Flight_Total": custom_flight,
            "Hotel_Total": custom_hotel,
            "Expenses_Total": custom_expenses,
            "Grand_Total": custom_total
        }])
        
        st.download_button(
            label="📄 Export Custom Budget as CSV",
            data=export_df.to_csv(index=False).encode('utf-8'),
            file_name=f"{selected_dest}_Custom_Travel_Plan.csv",
            mime="text/csv"
        )