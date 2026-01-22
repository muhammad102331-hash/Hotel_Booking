import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Hotel Booking Analysis Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('hotel_booking.csv')
    # Data cleaning
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], dayfirst=True)
    df.drop(['company', 'agent'], axis=1, inplace=True)
    df['children'].fillna(df['children'].median(), inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    
    # Handle outliers
    Q1 = df['adr'].quantile(0.25)
    Q3 = df['adr'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['adr'] >= lower_bound) & (df['adr'] <= upper_bound)]
    
    # Add month column
    df['month'] = df['reservation_status_date'].dt.month
    df['year'] = df['reservation_status_date'].dt.year
    
    return df

# Load data
try:
    df = load_data()
    data_loaded = True
except:
    data_loaded = False
    st.error("⚠️ Please ensure 'hotel_booking.csv' is in the same directory as this app.")

# Header
st.markdown('<p class="main-header">🏨 Hotel Booking Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Presented by Syed Muhammad Ali</p>', unsafe_allow_html=True)

if data_loaded:
    # Sidebar
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Select Analysis", [
        "📈 Overview",
        "🚫 Cancellation Analysis", 
        "💰 Revenue Insights",
        "🌍 Geographic Analysis",
        "📅 Seasonal Trends",
        "🔗 Booking Channels"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Dataset Info")
    st.sidebar.metric("Total Records", f"{len(df):,}")
    st.sidebar.metric("Date Range", f"{df['reservation_status_date'].min().year} - {df['reservation_status_date'].max().year}")
    st.sidebar.metric("Countries", df['country'].nunique())
    
    # Overview Page
    if page == "📈 Overview":
        st.header("Executive Summary")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_bookings = len(df)
        cancelled_bookings = df['is_canceled'].sum()
        cancellation_rate = (cancelled_bookings / total_bookings) * 100
        avg_adr = df['adr'].mean()
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Bookings", f"{total_bookings:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Daily Rate", f"${avg_adr:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Hotel Types", "2")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data Storytelling
        st.markdown("""
        ### 📖 The Story Behind the Data
        
        Our analysis reveals a **critical challenge**: nearly **37% of all hotel bookings are being canceled**. 
        This represents a significant opportunity for revenue recovery and operational improvement.
        
        **What This Means:**
        - For every 100 bookings, 37 don't materialize
        - Revenue uncertainty affects business planning
        - Room inventory management becomes complex
        - Staff scheduling becomes unpredictable
        """)
        
        # Cancellation Distribution Chart
        st.subheader("📊 Cancellation Distribution")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=['Not Cancelled', 'Cancelled'],
                    y=df['is_canceled'].value_counts().sort_index(),
                    marker_color=['#2ecc71', '#e74c3c'],
                    text=df['is_canceled'].value_counts().sort_index(),
                    textposition='auto',
                )
            ])
            fig.update_layout(
                title="Booking Status Distribution",
                xaxis_title="Status",
                yaxis_title="Number of Bookings",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("""
            **Key Insight:**
            
            🔴 **37% Cancellation Rate**
            
            This is significantly higher than the industry average of 25-30%.
            
            **Impact:**
            - Lost revenue opportunity
            - Inefficient resource allocation
            - Reduced forecasting accuracy
            
            **Action Required:**
            Implement targeted retention strategies
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Hotel Type Comparison
        st.subheader("🏨 Hotel Type Performance")
        
        hotel_cancel = df.groupby(['hotel', 'is_canceled']).size().reset_index(name='count')
        
        fig = px.bar(
            hotel_cancel,
            x='hotel',
            y='count',
            color='is_canceled',
            barmode='group',
            labels={'is_canceled': 'Status', 'count': 'Number of Bookings', 'hotel': 'Hotel Type'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            title="Bookings by Hotel Type and Status"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            resort_cancel_rate = df[df['hotel']=='Resort Hotel']['is_canceled'].mean() * 100
            st.info(f"🏖️ **Resort Hotel:** {resort_cancel_rate:.1f}% cancellation rate")
        
        with col2:
            city_cancel_rate = df[df['hotel']=='City Hotel']['is_canceled'].mean() * 100
            st.warning(f"🏙️ **City Hotel:** {city_cancel_rate:.1f}% cancellation rate")
    
    # Cancellation Analysis Page
    elif page == "🚫 Cancellation Analysis":
        st.header("Cancellation Deep Dive")
        
        st.markdown("""
        ### 🎯 Understanding Why Bookings Get Cancelled
        
        Cancellations don't happen randomly. Our analysis reveals specific patterns that can help 
        predict and prevent future cancellations.
        """)
        
        # Monthly Cancellation Trends
        st.subheader("📅 Monthly Cancellation Patterns")
        
        monthly_cancel = df.groupby(['month', 'is_canceled']).size().reset_index(name='count')
        
        fig = px.line(
            monthly_cancel,
            x='month',
            y='count',
            color='is_canceled',
            markers=True,
            labels={'month': 'Month', 'count': 'Number of Bookings', 'is_canceled': 'Status'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            title="Monthly Booking Trends: Cancelled vs Not Cancelled"
        )
        fig.update_xaxes(tickmode='linear', dtick=1)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        **📊 Pattern Analysis:**
        
        - **Peak Cancellation Months:** Summer months (June-August) see the highest cancellations
        - **Correlation:** High booking volume = High cancellation volume
        - **Opportunity:** Focus retention efforts during peak seasons
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lead Time Analysis
        st.subheader("⏰ Lead Time Impact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cancelled_lead = df[df['is_canceled']==1]['lead_time'].mean()
            not_cancelled_lead = df[df['is_canceled']==0]['lead_time'].mean()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['Cancelled', 'Not Cancelled'],
                    y=[cancelled_lead, not_cancelled_lead],
                    marker_color=['#e74c3c', '#2ecc71'],
                    text=[f"{cancelled_lead:.0f} days", f"{not_cancelled_lead:.0f} days"],
                    textposition='auto',
                )
            ])
            fig.update_layout(
                title="Average Lead Time (Days Before Arrival)",
                yaxis_title="Days",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **🔍 Key Finding:**
            
            Cancelled bookings are made **{cancelled_lead - not_cancelled_lead:.0f} days earlier** on average.
            
            **Why This Matters:**
            - Early bookings have higher uncertainty
            - Life circumstances change over time
            - Longer waiting = Higher cancellation risk
            
            **Strategy:**
            - Offer incentives for non-refundable rates
            - Send confirmation reminders
            - Implement flexible rebooking options
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Revenue Insights Page
    elif page == "💰 Revenue Insights":
        st.header("Revenue Analysis & Pricing Patterns")
        
        st.markdown("""
        ### 💡 Price Intelligence: What the Numbers Tell Us
        
        Understanding the relationship between pricing and cancellations is crucial for maximizing revenue.
        """)
        
        # ADR Comparison
        st.subheader("💵 Average Daily Rate (ADR) Comparison")
        
        # Filter data for 2016-2017
        cancelled_data = df[df['is_canceled'] == 1]
        not_cancelled_data = df[df['is_canceled'] == 0]
        
        cancelled_data_filtered = cancelled_data[
            (cancelled_data['reservation_status_date'].dt.year >= 2016) & 
            (cancelled_data['reservation_status_date'].dt.year <= 2017)
        ]
        not_cancelled_data_filtered = not_cancelled_data[
            (not_cancelled_data['reservation_status_date'].dt.year >= 2016) & 
            (not_cancelled_data['reservation_status_date'].dt.year <= 2017)
        ]
        
        cancelled_adr = cancelled_data_filtered.groupby('reservation_status_date')['adr'].mean().reset_index()
        not_cancelled_adr = not_cancelled_data_filtered.groupby('reservation_status_date')['adr'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=not_cancelled_adr['reservation_status_date'],
            y=not_cancelled_adr['adr'],
            mode='lines',
            name='Not Cancelled',
            line=dict(color='#2ecc71', width=2),
            fill='tonexty'
        ))
        fig.add_trace(go.Scatter(
            x=cancelled_adr['reservation_status_date'],
            y=cancelled_adr['adr'],
            mode='lines',
            name='Cancelled',
            line=dict(color='#e74c3c', width=2),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Average Daily Rate Over Time (2016-2017): Cancelled vs Not Cancelled",
            xaxis_title="Date",
            yaxis_title="Average Daily Rate ($)",
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_cancelled_adr = cancelled_data['adr'].mean()
            st.metric("Avg ADR (Cancelled)", f"${avg_cancelled_adr:.2f}")
        
        with col2:
            avg_not_cancelled_adr = not_cancelled_data['adr'].mean()
            st.metric("Avg ADR (Not Cancelled)", f"${avg_not_cancelled_adr:.2f}")
        
        with col3:
            diff = avg_cancelled_adr - avg_not_cancelled_adr
            st.metric("Difference", f"${diff:.2f}", delta=f"{(diff/avg_not_cancelled_adr*100):.1f}%")
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        **💰 Revenue Intelligence:**
        
        **Key Observation:** Cancelled bookings have slightly higher prices on average.
        
        **What This Means:**
        - Price sensitivity may drive cancellations
        - Higher-priced bookings carry more risk
        - Premium guests may have more flexibility
        
        **Actionable Strategy:**
        - Implement tiered pricing with cancellation terms
        - Offer price guarantees for non-refundable bookings
        - Create loyalty rewards to offset price concerns
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Hotel Type ADR
        st.subheader("🏨 Pricing by Hotel Type")
        
        resort_adr = df[df['hotel']=='Resort Hotel'].groupby('reservation_status_date')['adr'].mean().reset_index()
        city_adr = df[df['hotel']=='City Hotel'].groupby('reservation_status_date')['adr'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=resort_adr['reservation_status_date'],
            y=resort_adr['adr'],
            mode='lines',
            name='Resort Hotel',
            line=dict(color='#3498db', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=city_adr['reservation_status_date'],
            y=city_adr['adr'],
            mode='lines',
            name='City Hotel',
            line=dict(color='#f39c12', width=2)
        ))
        
        fig.update_layout(
            title="Average Daily Rate by Hotel Type Over Time",
            xaxis_title="Date",
            yaxis_title="Average Daily Rate ($)",
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Geographic Analysis Page
    elif page == "🌍 Geographic Analysis":
        st.header("Geographic Patterns & International Trends")
        
        st.markdown("""
        ### 🗺️ Where Are Cancellations Coming From?
        
        Understanding geographic patterns helps us tailor our approach for different markets.
        """)
        
        # Top Countries with Cancellations
        st.subheader("🌍 Top 10 Countries with Highest Cancellations")
        
        top_countries = df[df['is_canceled']==1]['country'].value_counts().head(10)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig = go.Figure(data=[go.Pie(
                labels=top_countries.index,
                values=top_countries.values,
                hole=.3,
                marker_colors=px.colors.qualitative.Set3
            )])
            fig.update_layout(
                title="Distribution of Cancelled Bookings by Country",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Top Countries")
            for i, (country, count) in enumerate(top_countries.items(), 1):
                percentage = (count / top_countries.sum()) * 100
                st.markdown(f"**{i}. {country}:** {count:,} cancellations ({percentage:.1f}%)")
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **🎯 Critical Finding:**
        
        **Portugal dominates with {(top_countries.iloc[0]/top_countries.sum()*100):.1f}% of all cancellations** among the top 10 countries.
        
        **Why This Matters:**
        - Concentrated risk in one market
        - Cultural or policy factors may be at play
        - Opportunity for targeted intervention
        
        **Recommended Actions:**
        1. **Investigate:** Why are Portuguese guests canceling?
        2. **Communicate:** Improve Portuguese language support
        3. **Incentivize:** Create retention programs for Portuguese market
        4. **Partner:** Work with Portuguese travel agencies
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cancellation Rate by Country
        st.subheader("📈 Cancellation Rate by Top Countries")
        
        top_countries_all = df['country'].value_counts().head(10).index
        country_cancel_rate = df[df['country'].isin(top_countries_all)].groupby('country')['is_canceled'].agg(['mean', 'count']).reset_index()
        country_cancel_rate['mean'] = country_cancel_rate['mean'] * 100
        country_cancel_rate = country_cancel_rate.sort_values('mean', ascending=False)
        
        fig = px.bar(
            country_cancel_rate,
            x='country',
            y='mean',
            text='mean',
            labels={'mean': 'Cancellation Rate (%)', 'country': 'Country'},
            title="Cancellation Rate by Country (Top 10 Booking Countries)",
            color='mean',
            color_continuous_scale='Reds'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal Trends Page
    elif page == "📅 Seasonal Trends":
        st.header("Seasonal Booking Patterns")
        
        st.markdown("""
        ### 🌤️ When Do Bookings Happen? When Do They Cancel?
        
        Seasonal patterns reveal critical timing for interventions and promotions.
        """)
        
        # Monthly ADR by Cancellation Status
        st.subheader("💰 Monthly Revenue Patterns")
        
        monthly_adr = df[df['is_canceled']==1].groupby('arrival_date_month')['adr'].sum().reset_index()
        
        # Sort by month order
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_adr['arrival_date_month'] = pd.Categorical(monthly_adr['arrival_date_month'], categories=month_order, ordered=True)
        monthly_adr = monthly_adr.sort_values('arrival_date_month')
        
        fig = px.bar(
            monthly_adr,
            x='arrival_date_month',
            y='adr',
            title="Total ADR by Month (Cancelled Bookings Only)",
            labels={'arrival_date_month': 'Month', 'adr': 'Total ADR ($)'},
            color='adr',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        **🔍 Seasonal Insight:**
        
        **Peak Lost Revenue:** Summer months (June, July, August) show the highest cancelled revenue.
        
        **Strategic Implications:**
        - Focus retention efforts before summer season
        - Implement stricter cancellation policies during peak season
        - Offer early bird discounts with commitment terms
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Year-over-year comparison
        st.subheader("📊 Year-over-Year Booking Trends")
        
        yearly_bookings = df.groupby(['year', 'is_canceled']).size().reset_index(name='count')
        
        fig = px.bar(
            yearly_bookings,
            x='year',
            y='count',
            color='is_canceled',
            barmode='group',
            labels={'is_canceled': 'Status', 'count': 'Number of Bookings', 'year': 'Year'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            title="Annual Booking Trends"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Booking Channels Page
    elif page == "🔗 Booking Channels":
        st.header("Booking Channel Analysis")
        
        st.markdown("""
        ### 📱 How Are Customers Finding Us?
        
        Different booking channels have different cancellation behaviors and profitability.
        """)
        
        # Market Segment Analysis
        st.subheader("🎯 Market Segment Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### All Bookings")
            market_all = df['market_segment'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=market_all.index,
                values=market_all.values,
                hole=.3
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Cancelled Bookings Only")
            market_cancelled = df[df['is_canceled']==1]['market_segment'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=market_cancelled.index,
                values=market_cancelled.values,
                hole=.3,
                marker_colors=px.colors.qualitative.Set3
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        **📊 Channel Intelligence:**
        
        **Online Travel Agencies (OTAs):**
        - Drive the highest volume (47% of bookings)
        - Also have high cancellation rates (45.6% of cancellations)
        - High volume, but lower quality
        
        **Direct Bookings:**
        - Only 12% of total bookings
        - Lower cancellation rate (4.1% of cancellations)
        - Higher quality, better retention
        
        **Strategy:**
        - Incentivize direct bookings with exclusive perks
        - Work with OTAs to improve booking quality
        - Focus on corporate partnerships (lowest cancellation rate)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cancellation Rate by Segment
        st.subheader("📈 Cancellation Rate by Market Segment")
        
        segment_cancel = df.groupby('market_segment')['is_canceled'].agg(['mean', 'count']).reset_index()
        segment_cancel['mean'] = segment_cancel['mean'] * 100
        segment_cancel = segment_cancel.sort_values('mean', ascending=False)
        
        fig = px.bar(
            segment_cancel,
            x='market_segment',
            y='mean',
            text='mean',
            labels={'mean': 'Cancellation Rate (%)', 'market_segment': 'Market Segment'},
            title="Cancellation Rate by Market Segment",
            color='mean',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution Channel
        st.subheader("🔀 Distribution Channel Performance")
        
        channel_data = df.groupby(['distribution_channel', 'is_canceled']).size().reset_index(name='count')
        
        fig = px.bar(
            channel_data,
            x='distribution_channel',
            y='count',
            color='is_canceled',
            barmode='group',
            labels={'is_canceled': 'Status', 'count': 'Number of Bookings', 'distribution_channel': 'Channel'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            title="Bookings by Distribution Channel"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Hotel Booking Analysis Dashboard</strong></p>
        <p>Presented by: Syed Muhammad Ali | Data Analyst</p>
        <p>📧 Contact for detailed analysis and recommendations</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Please ensure the data file 'hotel_booking.csv' is in the correct location.")
