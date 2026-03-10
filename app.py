"""
✈️ Flight Delay Analysis Dashboard
Interactive Streamlit app for exploring flight delays across US airlines in 2015
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Flight Delay Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .title-section {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING & CACHING
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    """Load and preprocess data"""
    try:
        airlines = pd.read_csv('airlines.csv')
        airports = pd.read_csv('airports.csv')
        data = pd.read_csv('flights.csv')
        
        # Convert to datetime
        data['MONTH'] = data['MONTH'].astype(int)
        
        return airlines, airports, data
    except FileNotFoundError as e:
        st.error(f"❌ Error: {e}")
        st.warning("Make sure airlines.csv, airports.csv, and flights.csv are in the project directory")
        st.stop()

airlines_df, airports_df, data_df = load_data()

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - FILTERS
# ═══════════════════════════════════════════════════════════════════════════

st.sidebar.markdown("## 📊 Filters & Settings")
st.sidebar.markdown("---")

# Airline filter
selected_airlines = st.sidebar.multiselect(
    "Select Airlines:",
    sorted(data_df['AIRLINE'].unique()),
    default=sorted(data_df['AIRLINE'].unique())[:3]
)

# Date filter
months = st.sidebar.slider(
    "Select Month Range:",
    min_value=1,
    max_value=12,
    value=(1, 12),
    help="Select range from 1 (Jan) to 12 (Dec)"
)

# Delay threshold
delay_threshold = st.sidebar.select_slider(
    "Delay Threshold (minutes):",
    options=[5, 10, 15, 20, 30, 45, 60],
    value=15,
    help="FAA definition: ≥15 minutes is considered delayed"
)

st.sidebar.markdown("---")

# Apply filters
filtered_data = data_df[
    (data_df['AIRLINE'].isin(selected_airlines)) &
    (data_df['MONTH'] >= months[0]) &
    (data_df['MONTH'] <= months[1])
]

# ═══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT - TITLE & DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
    <div class="title-section">
        <h1>✈️ Flight Delay Analysis Dashboard</h1>
        <p>Exploring patterns in flight delays across major US airlines (2015)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
This interactive dashboard analyzes **flight delay patterns** across 14 major US airlines in 2015.
Use the filters on the left to customize your analysis.
""")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# KEY METRICS
# ═══════════════════════════════════════════════════════════════════════════

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_flights = len(filtered_data)
    st.metric(
        "Total Flights",
        f"{total_flights:,}",
        help="Total number of flights in selected filters"
    )

with col2:
    delayed_flights = len(filtered_data[filtered_data['ARRIVAL_DELAY'] >= delay_threshold])
    st.metric(
        f"Delayed Flights (≥{delay_threshold}min)",
        f"{delayed_flights:,}",
        f"{(delayed_flights/total_flights*100):.1f}%" if total_flights > 0 else "0%"
    )

with col3:
    avg_delay = filtered_data['ARRIVAL_DELAY'].mean()
    st.metric(
        "Average Delay",
        f"{avg_delay:.1f} min",
        help="Mean arrival delay in minutes"
    )

with col4:
    on_time = len(filtered_data[filtered_data['ARRIVAL_DELAY'] < delay_threshold])
    on_time_pct = (on_time / total_flights * 100) if total_flights > 0 else 0
    st.metric(
        "On-Time %",
        f"{on_time_pct:.1f}%",
        help=f"Percentage of flights arriving before {delay_threshold} min delay"
    )

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CHARTS - TAB LAYOUT
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Airline Comparison",
    "📅 Weekly Pattern",
    "🗓️ Monthly Trend",
    "🌍 Top Routes",
    "📊 Data Table"
])

# ─────────────────────────────────────────────────────────────────────────
# TAB 1: AIRLINE COMPARISON
# ─────────────────────────────────────────────────────────────────────────

with tab1:
    st.subheader("Delay Metrics by Airline")
    
    # Calculate airline statistics
    airline_stats = []
    for airline in selected_airlines:
        airline_data = filtered_data[filtered_data['AIRLINE'] == airline]
        if len(airline_data) > 0:
            delayed = len(airline_data[airline_data['ARRIVAL_DELAY'] >= delay_threshold])
            delay_pct = (delayed / len(airline_data)) * 100
            avg_arr_delay = airline_data['ARRIVAL_DELAY'].mean()
            total = len(airline_data)
            
            airline_stats.append({
                'Airline': airline,
                'Total Flights': total,
                'Delayed': delayed,
                'Delay %': delay_pct,
                'Avg Delay (min)': avg_arr_delay
            })
    
    airline_stats_df = pd.DataFrame(airline_stats)
    
    # 2 columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Delay percentage bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(airline_stats_df)))
        ax.barh(airline_stats_df['Airline'], airline_stats_df['Delay %'], color=colors)
        ax.set_xlabel('Delay Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Delay Percentage by Airline', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(airline_stats_df['Delay %']):
            ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        # Average delay bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(airline_stats_df['Airline'], airline_stats_df['Avg Delay (min)'], color='steelblue')
        ax.set_xlabel('Average Delay (minutes)', fontsize=12, fontweight='bold')
        ax.set_title('Average Arrival Delay by Airline', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(airline_stats_df['Avg Delay (min)']):
            ax.text(v + 0.5, i, f'{v:.1f}', va='center', fontweight='bold')
        st.pyplot(fig)
    
    # Statistics table
    st.subheader("Detailed Statistics")
    st.dataframe(
        airline_stats_df.sort_values('Delay %', ascending=False),
        use_container_width=True,
        hide_index=True
    )

# ─────────────────────────────────────────────────────────────────────────
# TAB 2: WEEKLY PATTERN
# ─────────────────────────────────────────────────────────────────────────

with tab2:
    st.subheader("Delay Patterns by Day of Week")
    
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # Calculate daily statistics
    daily_stats = []
    for day in range(1, 8):
        day_data = filtered_data[filtered_data['DAY_OF_WEEK'] == day]
        if len(day_data) > 0:
            delayed = len(day_data[day_data['ARRIVAL_DELAY'] >= delay_threshold])
            daily_stats.append({
                'Day': days[day-1],
                'Flights': len(day_data),
                'Delayed': delayed,
                'Delay %': (delayed / len(day_data)) * 100,
                'Avg Delay': day_data['ARRIVAL_DELAY'].mean()
            })
    
    daily_stats_df = pd.DataFrame(daily_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart - Delay percentage
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_stats_df['Day'], daily_stats_df['Delay %'], 
               marker='o', linewidth=2, markersize=8, color='#e74c3c')
        ax.fill_between(range(len(daily_stats_df)), daily_stats_df['Delay %'], alpha=0.3, color='#e74c3c')
        ax.set_ylabel('Delay Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Weekly Delay Patterns', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        # Bar chart - Number of flights
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(daily_stats_df['Day'], daily_stats_df['Flights'], color='skyblue', label='Total')
        ax.bar(daily_stats_df['Day'], daily_stats_df['Delayed'], color='coral', label='Delayed')
        ax.set_ylabel('Number of Flights', fontsize=12, fontweight='bold')
        ax.set_title('Flights by Day of Week', fontsize=14, fontweight='bold')
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    st.dataframe(daily_stats_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────
# TAB 3: MONTHLY TREND
# ─────────────────────────────────────────────────────────────────────────

with tab3:
    st.subheader("Delay Trends Throughout the Year")
    
    months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Calculate monthly statistics
    monthly_stats = []
    for month in range(1, 13):
        month_data = filtered_data[filtered_data['MONTH'] == month]
        if len(month_data) > 0:
            delayed = len(month_data[month_data['ARRIVAL_DELAY'] >= delay_threshold])
            monthly_stats.append({
                'Month': months_names[month-1],
                'Flights': len(month_data),
                'Delayed': delayed,
                'Delay %': (delayed / len(month_data)) * 100,
                'Avg Delay': month_data['ARRIVAL_DELAY'].mean()
            })
    
    monthly_stats_df = pd.DataFrame(monthly_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart - Delay trend
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_stats_df['Month'], monthly_stats_df['Delay %'], 
               marker='s', linewidth=2, markersize=8, color='#3498db')
        ax.fill_between(range(len(monthly_stats_df)), monthly_stats_df['Delay %'], 
                        alpha=0.3, color='#3498db')
        ax.set_ylabel('Delay Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Delay Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        # Area chart - Average delay
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.fill_between(range(len(monthly_stats_df)), monthly_stats_df['Avg Delay'], 
                        alpha=0.6, color='#2ecc71')
        ax.plot(monthly_stats_df['Month'], monthly_stats_df['Avg Delay'], 
               marker='o', linewidth=2, markersize=8, color='#27ae60')
        ax.set_ylabel('Average Delay (minutes)', fontsize=12, fontweight='bold')
        ax.set_title('Average Delay by Month', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    st.dataframe(monthly_stats_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────
# TAB 4: TOP ROUTES
# ─────────────────────────────────────────────────────────────────────────

with tab4:
    st.subheader("Top Routes with Most Delays")
    
    # Find top routes
    route_data = filtered_data.copy()
    route_data['Route'] = route_data['ORIGIN_AIRPORT'] + ' → ' + route_data['DESTINATION_AIRPORT']
    
    route_delays = route_data.groupby('Route').agg({
        'ARRIVAL_DELAY': ['count', 'mean', lambda x: len(x[x >= delay_threshold])]
    }).round(2)
    route_delays.columns = ['Total', 'Avg Delay', 'Delayed Count']
    route_delays['Delay %'] = (route_delays['Delayed Count'] / route_delays['Total'] * 100).round(2)
    route_delays = route_delays.sort_values('Delay %', ascending=False).head(10)
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Top routes by delay percentage
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(range(len(route_delays)), route_delays['Delay %'], color='#e74c3c')
        ax.set_yticks(range(len(route_delays)))
        ax.set_yticklabels(route_delays.index, fontsize=10)
        ax.set_xlabel('Delay Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Routes by Delay Percentage', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(route_delays['Delay %']):
            ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontweight='bold', fontsize=9)
        st.pyplot(fig)
    
    with col2:
        # Top routes by average delay
        route_delays_sorted = route_delays.sort_values('Avg Delay', ascending=False)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(range(len(route_delays_sorted)), route_delays_sorted['Avg Delay'], color='#3498db')
        ax.set_yticks(range(len(route_delays_sorted)))
        ax.set_yticklabels(route_delays_sorted.index, fontsize=10)
        ax.set_xlabel('Average Delay (minutes)', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Routes by Average Delay', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(route_delays_sorted['Avg Delay']):
            ax.text(v + 0.5, i, f'{v:.1f}', va='center', fontweight='bold', fontsize=9)
        st.pyplot(fig)
    
    st.subheader("Route Statistics")
    route_table = route_delays.reset_index()
    route_table.columns = ['Route', 'Total Flights', 'Avg Delay (min)', 'Delayed Count', 'Delay %']
    st.dataframe(route_table, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────
# TAB 5: DATA TABLE
# ─────────────────────────────────────────────────────────────────────────

with tab5:
    st.subheader("Raw Data Viewer")
    
    # Show sample size
    st.info(f"📊 Showing {len(filtered_data):,} flights out of {len(data_df):,} total")
    
    # Column selection
    columns_to_show = st.multiselect(
        "Select columns to display:",
        filtered_data.columns.tolist(),
        default=['YEAR', 'MONTH', 'DAY_OF_WEEK', 'AIRLINE', 'ORIGIN_AIRPORT', 
                'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'DISTANCE']
    )
    
    # Display dataframe
    st.dataframe(
        filtered_data[columns_to_show].head(100),
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = filtered_data[columns_to_show].to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="flight_delay_analysis.csv",
        mime="text/csv"
    )

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Data Source:** Kaggle - Department of Transportation")
    st.markdown("**Dataset:** 2015 Flight Data")

with col2:
    st.markdown("**Airlines Analyzed:** 14 Major US Carriers")
    st.markdown("**Total Records:** 100,000+ flights")

with col3:
    st.markdown("**Built with:** Streamlit")
    st.markdown("**Analysis:** [GitHub](https://github.com/your-username/Flight-Delay-Analysis)")

st.markdown("""
---
**About This Analysis:** This dashboard explores flight delay patterns across major US airlines in 2015. 
The analysis uses data cleaning, statistical analysis, and machine learning to uncover insights about what factors 
contribute to flight delays.
""")
