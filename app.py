import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Family Travel Planner", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# 1. Safe Data Loading
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "travel_data.csv")
    return pd.read_csv(csv_path)

df = load_data()

st.title("✈️ Family Travel Cost & Comparison Dashboard")
st.caption("Plan your next family vacation by comparing real-time cost breakdowns in INR (₹).")
st.divider()

# 2. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Trip Parameters")
    
    # NEW: Domestic vs International Filter
    travel_type = st.radio("🌍 Travel Scope", ["All", "Domestic", "International"])
    
    family_size = st.number_input("👨‍👩‍👧‍👦 Family Members", min_value=1, max_value=10, value=4)
    trip_days = st.slider("📅 Trip Duration (Days)", min_value=1, max_value=30, value=7)
    max_budget = st.number_input("💰 Max Budget (₹)", min_value=20000, max_value=2000000, value=400000, step=25000)

# Filter dataset based on Travel Scope
if travel_type != "All":
    filtered_type_df = df[df['type'] == travel_type]
else:
    filtered_type_df = df.copy()

# Dynamic Cost Calculations in INR
filtered_type_df['TotalFlight'] = filtered_type_df['flight_inr'] * family_size
filtered_type_df['TotalHotel'] = filtered_type_df['nightly_inr'] * trip_days
filtered_type_df['TotalDaily'] = filtered_type_df['daily_inr'] * family_size * trip_days
filtered_type_df['TotalFamilyCost'] = (
    filtered_type_df['TotalFlight'] + 
    filtered_type_df['TotalHotel'] + 
    filtered_type_df['TotalDaily']
)

# Apply Budget Filter
filtered_df = filtered_type_df[filtered_type_df['TotalFamilyCost'] <= max_budget].sort_values(by='TotalFamilyCost')

tab1, tab2 = st.tabs(["⚖️ Side-by-Side Comparison", "📊 Cost Analytics & Breakdown"])

# TAB 1: Side-by-Side Comparison
with tab1:
    st.subheader(f"Compare Locations ({travel_type} Destinations)")
    
    available_dests = filtered_type_df['name'].unique()
    
    if len(available_dests) >= 2:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            dest1 = st.selectbox("Destination 1", available_dests, index=0)
        with col_sel2:
            dest2 = st.selectbox("Destination 2", available_dests, index=1)
            
        data1 = filtered_type_df[filtered_type_df['name'] == dest1].iloc[0]
        data2 = filtered_type_df[filtered_type_df['name'] == dest2].iloc[0]
        
        col1, col2 = st.columns(2)
        
        # Card 1
        with col1:
            st.image(data1['image'], use_container_width=True)
            st.markdown(f"### 📍 {data1['name']}, {data1['country']}")
            st.caption(f"_{data1['tagline']}_ | **{data1['type']}**")
            st.metric(label="Total Family Trip Cost", value=f"₹{int(data1['TotalFamilyCost']):,}")
            
            with st.expander("🔍 View Detailed Expense Breakdown", expanded=True):
                st.write(f"✈️ **Flights ({family_size} passengers):** ₹{int(data1['TotalFlight']):,}")
                st.write(f"🏨 **Hotel ({trip_days} nights):** ₹{int(data1['TotalHotel']):,}")
                st.write(f"🍽️ **Daily Expenses:** ₹{int(data1['TotalDaily']):,}")
                st.write(f"⭐ **User Rating:** {data1['rating']} / 5.0")
            
        # Card 2
        with col2:
            st.image(data2['image'], use_container_width=True)
            st.markdown(f"### 📍 {data2['name']}, {data2['country']}")
            st.caption(f"_{data2['tagline']}_ | **{data2['type']}**")
            st.metric(label="Total Family Trip Cost", value=f"₹{int(data2['TotalFamilyCost']):,}")
            
            with st.expander("🔍 View Detailed Expense Breakdown", expanded=True):
                st.write(f"✈️ **Flights ({family_size} passengers):** ₹{int(data2['TotalFlight']):,}")
                st.write(f"🏨 **Hotel ({trip_days} nights):** ₹{int(data2['TotalHotel']):,}")
                st.write(f"🍽️ **Daily Expenses:** ₹{int(data2['TotalDaily']):,}")
                st.write(f"⭐ **User Rating:** {data2['rating']} / 5.0")
            
        st.divider()
        diff = abs(data1['TotalFamilyCost'] - data2['TotalFamilyCost'])
        if data1['TotalFamilyCost'] != data2['TotalFamilyCost']:
            cheaper = data1['name'] if data1['TotalFamilyCost'] < data2['TotalFamilyCost'] else data2['name']
            st.success(f"💡 **Budget Tip:** Choosing **{cheaper}** saves your family **₹{int(diff):,}** overall!")
        else:
            st.info("Both selected destinations cost the exact same amount for your parameters.")
    else:
        st.warning("Not enough destinations match the selected filter to perform a side-by-side comparison.")

# TAB 2: Visual Charts
with tab2:
    if not filtered_df.empty:
        st.subheader("Budget Breakdown Visuals")
        
        chart_data = filtered_df.melt(
            id_vars=['name', 'type'], 
            value_vars=['TotalFlight', 'TotalHotel', 'TotalDaily'],
            var_name='Cost Type', 
            value_name='Amount'
        )
        chart_data['Cost Type'] = chart_data['Cost Type'].replace({
            'TotalFlight': 'Flights',
            'TotalHotel': 'Hotel/Stay',
            'TotalDaily': 'Daily Expenses'
        })
        
        fig_stacked = px.bar(
            chart_data,
            x="name",
            y="Amount",
            color="Cost Type",
            title="Cost Composition by Destination",
            text_auto="₹,.0f",
            labels={"Amount": "Total Cost (₹)", "name": "Destination"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        st.subheader("Filtered Destinations Table")
        st.dataframe(
            filtered_df[['name', 'country', 'type', 'tagline', 'TotalFamilyCost', 'rating']], 
            use_container_width=True
        )
    else:
        st.warning("No destinations fit inside your selected budget limit. Try adjusting your max budget in the sidebar.")