import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import threading
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from data_generator import RetailDataGenerator
from analytics_engine import AnalyticsEngine
from anomaly_detector import AnomalyDetector
from customer_segmentation import CustomerSegmentation
from predictive_analytics import PredictiveAnalytics
from report_generator import ReportGenerator
from image_generator import ImageGenerator

# Configure page
st.set_page_config(
    page_title="Advanced Retail Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with blue-green-black theme and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
    
    .main {
        background: linear-gradient(135deg, #0a0f1c 0%, #1a2332 50%, #2c3e50 100%);
        min-height: 100vh;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .main-header {
        background: linear-gradient(135deg, #00d4ff 0%, #090979 50%, #020024 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.3);
        animation: fadeInUp 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
        transform: rotate(45deg);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 50%, #00c9ff 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        color: #1a2332;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 201, 255, 0.3);
        animation: fadeInUp 1.2s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s infinite;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(0, 212, 255, 0.2);
        color: #00d4ff;
        animation: slideInRight 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.8s;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.4);
        border-color: #00d4ff;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border-left: 5px solid #00d4ff;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        color: white;
        animation: slideInRight 0.6s ease-out;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 3s infinite;
    }
    
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .nav-pills {
        display: flex;
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 0.8rem;
        border-radius: 25px;
        margin: 1rem 0;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.3);
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%) !important;
        color: #1a2332 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 201, 255, 0.4) !important;
        background: linear-gradient(135deg, #92fe9d 0%, #00c9ff 100%) !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a2332 0%, #2c3e50 100%);
        color: #00d4ff;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #00d4ff !important;
    }
    
    .stMultiSelect > div > div {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #00d4ff !important;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(0, 212, 255, 0.2);
        color: white;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
        animation: pulse 2s infinite;
    }
    
    .status-active {
        background: linear-gradient(135deg, #00d4ff, #92fe9d);
        color: #1a2332;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .status-inactive {
        background: linear-gradient(135deg, #2c3e50, #1a2332);
        color: #00d4ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stMetric > div {
        color: #00d4ff !important;
    }
    
    .stMetric label {
        color: #92fe9d !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    .glowing-text {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        animation: pulse 2s infinite;
    }
    
    .animated-bg {
        background: linear-gradient(270deg, #00d4ff, #92fe9d, #00c9ff);
        background-size: 600% 600%;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_generator' not in st.session_state:
    st.session_state.data_generator = RetailDataGenerator()
    st.session_state.analytics_engine = AnalyticsEngine()
    st.session_state.anomaly_detector = AnomalyDetector()
    st.session_state.customer_segmentation = CustomerSegmentation()
    st.session_state.predictive_analytics = PredictiveAnalytics()
    st.session_state.report_generator = ReportGenerator()
    st.session_state.image_generator = ImageGenerator()
    st.session_state.sales_data = pd.DataFrame()
    st.session_state.is_streaming = False
    st.session_state.last_update = datetime.now()
    st.session_state.current_page = "Home"
    st.session_state.generated_report = ""

def generate_data_batch():
    """Generate a batch of new sales data"""
    batch_data = st.session_state.data_generator.generate_batch(batch_size=10)
    
    # Append to existing data
    if not st.session_state.sales_data.empty:
        st.session_state.sales_data = pd.concat([st.session_state.sales_data, batch_data], ignore_index=True)
    else:
        st.session_state.sales_data = batch_data
    
    # Keep only last 1000 records for performance
    if len(st.session_state.sales_data) > 1000:
        st.session_state.sales_data = st.session_state.sales_data.tail(1000).reset_index(drop=True)
    
    st.session_state.last_update = datetime.now()

def stream_data():
    """Simulate real-time data streaming"""
    import streamlit as st
    try:
        while getattr(st.session_state, 'is_streaming', False):
            generate_data_batch()
            time.sleep(2)
    except Exception:
        # Handle session state access issues in threading
        pass

def show_homepage():
    """Display the attractive homepage"""
    # Hero Section with animations
    st.markdown("""
    <div class="hero-section animated-bg">
        <h1 class="glowing-text floating-element">🚀 Advanced Retail Analytics Platform</h1>
        <h3>Unlock the Power of Data-Driven Retail Intelligence</h3>
        <p>Transform your retail operations with AI-powered analytics, real-time insights, and predictive intelligence</p>
        <div style="margin-top: 2rem;">
            <span class="status-badge status-active">✨ Next-Gen Analytics</span>
            <span class="status-badge status-active">🤖 AI-Powered</span>
            <span class="status-badge status-active">📊 Real-Time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate and display hero image
    hero_image = st.session_state.image_generator.create_dashboard_hero_image()
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="data:image/png;base64,{hero_image}" style="max-width: 100%; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    st.markdown("## 🎯 Platform Capabilities")
    
    # Generate feature icons
    icons = st.session_state.image_generator.create_feature_icons()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card floating-element">
            <img src="data:image/png;base64,{icons['analytics']}" style="width: 60px; height: 60px; margin-bottom: 1rem; animation: pulse 3s infinite;">
            <h4 class="glowing-text">📊 Real-Time Analytics</h4>
            <p>Live sales tracking, performance metrics, and instant insights with interactive dashboards</p>
            <ul style="text-align: left; margin-top: 1rem; color: #92fe9d;">
                <li>• Live sales monitoring</li>
                <li>• Performance KPIs</li>
                <li>• Interactive visualizations</li>
                <li>• Trend analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <img src="data:image/png;base64,{icons['customers']}" style="width: 60px; height: 60px; margin-bottom: 1rem;">
            <h4>👥 Customer Intelligence</h4>
            <p>Advanced customer segmentation, lifetime value analysis, and behavior insights</p>
            <ul style="text-align: left; margin-top: 1rem;">
                <li>RFM segmentation</li>
                <li>Customer lifetime value</li>
                <li>Churn risk analysis</li>
                <li>Journey mapping</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <img src="data:image/png;base64,{icons['predictions']}" style="width: 60px; height: 60px; margin-bottom: 1rem;">
            <h4>🔮 Predictive Analytics</h4>
            <p>AI-powered forecasting, demand prediction, and inventory optimization</p>
            <ul style="text-align: left; margin-top: 1rem;">
                <li>Sales forecasting</li>
                <li>Demand prediction</li>
                <li>Inventory optimization</li>
                <li>Seasonal analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Features Row
    st.markdown("## 🔧 Advanced Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🚨 Anomaly Detection</h4>
            <p>ML-powered anomaly detection using Isolation Forest and statistical methods</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Trend Analysis</h4>
            <p>Comprehensive trend analysis across products, categories, and time periods</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📋 Smart Reports</h4>
            <p>Automated report generation with actionable insights and recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Modern UI</h4>
            <p>Beautiful, responsive interface with interactive charts and visualizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start Section
    st.markdown("## 🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Generate Sample Data", key="home_sample", help="Create sample retail data to explore"):
            generate_data_batch()
            st.success("✅ Sample data generated! Check the Dashboard tab.")
    
    with col2:
        if st.button("📊 View Dashboard", key="home_dashboard", help="Go to the main analytics dashboard"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
    
    with col3:
        if st.button("🔄 Start Live Demo", key="home_stream", help="Start real-time data streaming"):
            try:
                st.session_state.is_streaming = True
                # Use a more robust threading approach
                if not hasattr(st.session_state, 'streaming_thread') or not st.session_state.streaming_thread.is_alive():
                    st.session_state.streaming_thread = threading.Thread(target=stream_data, daemon=True)
                    st.session_state.streaming_thread.start()
                st.success("🟢 Live demo started! Data is streaming...")
            except Exception as e:
                st.error(f"Error starting stream: {str(e)}")
    
    # Platform Statistics
    st.markdown("## 📊 Platform Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📈 Data Points", f"{len(st.session_state.sales_data):,}", 
                 delta="Real-time" if st.session_state.is_streaming else "Static")
    
    with col2:
        st.metric("🏪 Store Locations", "20", delta="Multi-location")
    
    with col3:
        st.metric("📦 Product Categories", "6", delta="Diverse portfolio")
    
    with col4:
        st.metric("👥 Customer Segments", "8+", delta="AI-powered")
    
    with col5:
        st.metric("🤖 ML Models", "5", delta="Advanced algorithms")

def show_dashboard():
    """Display the main analytics dashboard"""
    # Generate sample data if empty
    if st.session_state.sales_data.empty:
        st.info("📊 No data available. Generate some sample data to start exploring!")
        if st.button("🎲 Generate Sample Data"):
            for _ in range(3):  # Generate multiple batches for better analysis
                generate_data_batch()
            st.success("✅ Sample data generated!")
            st.rerun()
        return
    
    filtered_data = st.session_state.sales_data
    
    # Data filtering options in sidebar
    with st.sidebar:
        st.header("🎛️ Dashboard Controls")
        
        # Data streaming controls
        st.subheader("🔄 Data Streaming")
        
        streaming_col1, streaming_col2 = st.columns(2)
        with streaming_col1:
            if st.button("▶️ Start", disabled=st.session_state.is_streaming):
                try:
                    st.session_state.is_streaming = True
                    if not hasattr(st.session_state, 'streaming_thread') or not st.session_state.streaming_thread.is_alive():
                        st.session_state.streaming_thread = threading.Thread(target=stream_data, daemon=True)
                        st.session_state.streaming_thread.start()
                    st.success("Started!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with streaming_col2:
            if st.button("⏹️ Stop", disabled=not st.session_state.is_streaming):
                st.session_state.is_streaming = False
                st.success("Stopped!")
        
        if st.button("🎲 Generate Batch"):
            generate_data_batch()
            st.success("Data generated!")
        
        # Status indicators
        st.markdown(f"""
        <div class="status-badge {'status-active' if st.session_state.is_streaming else 'status-inactive'}">
            {'🟢 Streaming Active' if st.session_state.is_streaming else '🔴 Streaming Inactive'}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Filters
        st.subheader("🔍 Filters")
        
        if not filtered_data.empty:
            # Time range filter
            min_time = filtered_data['timestamp'].min()
            max_time = filtered_data['timestamp'].max()
            
            time_range = st.slider(
                "⏱️ Time Range",
                min_value=min_time.to_pydatetime(),
                max_value=max_time.to_pydatetime(),
                value=(min_time.to_pydatetime(), max_time.to_pydatetime()),
                format="HH:mm:ss"
            )
            
            # Category filter
            categories = filtered_data['category'].unique()
            selected_categories = st.multiselect(
                "📦 Product Categories",
                categories,
                default=categories
            )
            
            # Store filter
            stores = filtered_data['store_id'].unique()
            selected_stores = st.multiselect(
                "🏪 Store IDs",
                stores,
                default=stores
            )
            
            # Apply filters
            filtered_data = filtered_data[
                (filtered_data['timestamp'] >= time_range[0]) &
                (filtered_data['timestamp'] <= time_range[1]) &
                (filtered_data['category'].isin(selected_categories)) &
                (filtered_data['store_id'].isin(selected_stores))
            ]
    
    if filtered_data.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your criteria.")
        return
    
    # Main Dashboard Header with animations
    st.markdown("""
    <div class="main-header">
        <h1 class="glowing-text">📊 Real-Time Retail Analytics Dashboard</h1>
        <p>Comprehensive insights into your retail operations</p>
        <div style="margin-top: 1rem;">
            <span class="status-badge status-active floating-element">🔄 Live Analytics</span>
            <span class="status-badge status-active">📈 Smart Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Section
    analytics_results = st.session_state.analytics_engine.calculate_metrics(filtered_data)
    
    st.markdown("## 📈 Key Performance Indicators")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        total_revenue = filtered_data['total_amount'].sum()
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    
    with kpi_col2:
        total_transactions = len(filtered_data)
        st.metric("🛒 Transactions", f"{total_transactions:,}")
    
    with kpi_col3:
        avg_transaction = filtered_data['total_amount'].mean()
        st.metric("📊 Avg. Transaction", f"${avg_transaction:.2f}")
    
    with kpi_col4:
        unique_customers = filtered_data['customer_id'].nunique()
        st.metric("👥 Unique Customers", f"{unique_customers:,}")
    
    with kpi_col5:
        unique_products = filtered_data['product_name'].nunique()
        st.metric("📦 Products Sold", f"{unique_products}")
    
    st.markdown("---")
    
    # Charts Section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### 📈 Sales Trend Over Time")
        
        # Group by minute for trend analysis
        trend_data = filtered_data.copy()
        trend_data['minute'] = trend_data['timestamp'].dt.floor('T')
        minute_sales = trend_data.groupby('minute')['total_amount'].sum().reset_index()
        
        if len(minute_sales) > 0:
            fig_trend = px.line(
                minute_sales, 
                x='minute', 
                y='total_amount',
                title="Revenue Trend (Per Minute)",
                labels={'total_amount': 'Revenue ($)', 'minute': 'Time'}
            )
            fig_trend.update_traces(line_color='#667eea', line_width=3)
            fig_trend.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    
    with chart_col2:
        st.markdown("### 🏪 Sales by Category")
        category_sales = analytics_results['category_performance']
        if not category_sales.empty:
            fig_category = px.bar(
                category_sales,
                x='category',
                y='revenue',
                title="Revenue by Product Category",
                labels={'revenue': 'Revenue ($)', 'category': 'Category'},
                color='revenue',
                color_continuous_scale='viridis'
            )
            fig_category.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_category, use_container_width=True)
    
    # Additional Analytics
    st.markdown("---")
    st.markdown("## 🔍 Detailed Analytics")
    
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        st.markdown("### 🏬 Store Performance")
        store_sales = analytics_results['store_performance']
        if not store_sales.empty:
            top_stores = store_sales.head(10)
            fig_store = px.bar(
                top_stores,
                x='store_id',
                y='revenue',
                title="Top 10 Stores by Revenue",
                labels={'revenue': 'Revenue ($)', 'store_id': 'Store ID'},
                color='revenue',
                color_continuous_scale='plasma'
            )
            fig_store.update_layout(height=400)
            st.plotly_chart(fig_store, use_container_width=True)
    
    with analytics_col2:
        st.markdown("### 🛍️ Product Performance")
        product_performance = analytics_results['product_performance'].head(10)
        
        if not product_performance.empty:
            fig_products = px.bar(
                product_performance,
                y='product_name',
                x='quantity_sold',
                orientation='h',
                title="Top 10 Products by Quantity Sold",
                labels={'quantity_sold': 'Quantity Sold', 'product_name': 'Product'},
                color='revenue',
                color_continuous_scale='cividis'
            )
            fig_products.update_layout(height=400)
            st.plotly_chart(fig_products, use_container_width=True)
    
    # Anomaly Detection Section
    st.markdown("---")
    st.markdown("## 🚨 Anomaly Detection")
    
    if len(filtered_data) > 10:
        anomalies = st.session_state.anomaly_detector.detect_anomalies(filtered_data)
        
        if not anomalies.empty:
            st.warning(f"⚠️ {len(anomalies)} anomalies detected in recent transactions!")
            
            # Anomaly visualization
            fig_anomalies = go.Figure()
            
            # Normal transactions
            normal_data = filtered_data[~filtered_data.index.isin(anomalies.index)]
            fig_anomalies.add_trace(go.Scatter(
                x=normal_data['timestamp'],
                y=normal_data['total_amount'],
                mode='markers',
                name='Normal Transactions',
                marker=dict(color='#3498db', size=6, opacity=0.7)
            ))
            
            # Anomalous transactions
            fig_anomalies.add_trace(go.Scatter(
                x=anomalies['timestamp'],
                y=anomalies['total_amount'],
                mode='markers',
                name='Anomalies',
                marker=dict(color='#e74c3c', size=12, symbol='x', line=dict(color='white', width=1))
            ))
            
            fig_anomalies.update_layout(
                title="Transaction Anomalies Detection",
                xaxis_title="Time",
                yaxis_title="Transaction Amount ($)",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_anomalies, use_container_width=True)
            
            # Anomaly details
            with st.expander("📋 Anomaly Details"):
                st.dataframe(
                    anomalies[['timestamp', 'product_name', 'total_amount', 'anomaly_score']].round(3),
                    use_container_width=True
                )
        else:
            st.success("✅ No anomalies detected in current data.")
    else:
        st.info("🔄 Generate more data to enable anomaly detection.")

def show_customer_analytics():
    """Display customer analytics and segmentation"""
    if st.session_state.sales_data.empty:
        st.info("📊 No data available for customer analysis. Generate some data first!")
        if st.button("🎲 Generate Sample Data"):
            for _ in range(5):
                generate_data_batch()
            st.rerun()
        return
    
    st.markdown("""
    <div class="main-header">
        <h1>👥 Customer Intelligence & Segmentation</h1>
        <p>Deep insights into customer behavior and segmentation analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Customer Segmentation
    with st.spinner("🔄 Analyzing customer segments..."):
        rfm_data, segment_stats = st.session_state.customer_segmentation.segment_customers(
            st.session_state.sales_data, n_clusters=5
        )
    
    if not rfm_data.empty:
        st.markdown("## 🎯 Customer Segments")
        
        # Segment overview
        segment_col1, segment_col2, segment_col3 = st.columns(3)
        
        with segment_col1:
            st.metric("📊 Total Segments", len(segment_stats))
        
        with segment_col2:
            largest_segment = max(segment_stats.items(), key=lambda x: x[1]['customer_count'])
            st.metric("👑 Largest Segment", largest_segment[0])
        
        with segment_col3:
            most_valuable = max(segment_stats.items(), key=lambda x: x[1]['total_revenue'])
            st.metric("💎 Most Valuable", most_valuable[0])
        
        # Segment details
        for segment_name, stats in segment_stats.items():
            with st.expander(f"📋 {segment_name} Segment Details"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👥 Customers", stats['customer_count'])
                
                with col2:
                    st.metric("💰 Total Revenue", f"${stats['total_revenue']:,.2f}")
                
                with col3:
                    st.metric("🛒 Avg. Transaction", f"${stats['avg_transaction_value']:.2f}")
                
                with col4:
                    st.metric("📈 Frequency", f"{stats['avg_frequency']:.1f}")
                
                # Preferred categories
                if stats['preferred_categories']:
                    st.markdown("**🏷️ Preferred Categories:**")
                    for category, revenue in list(stats['preferred_categories'].items())[:3]:
                        st.write(f"• {category}: ${revenue:,.2f}")
        
        # RFM Analysis Visualization
        st.markdown("## 📊 RFM Analysis")
        
        fig_rfm = px.scatter_3d(
            rfm_data,
            x='recency',
            y='frequency',
            z='monetary',
            color='segment_name',
            title="3D RFM Customer Segmentation",
            labels={
                'recency': 'Recency (Days)',
                'frequency': 'Frequency (Transactions)',
                'monetary': 'Monetary Value ($)'
            }
        )
        fig_rfm.update_layout(height=600)
        st.plotly_chart(fig_rfm, use_container_width=True)
    
    # Customer Lifetime Value
    st.markdown("## 💎 Customer Lifetime Value")
    
    clv_data = st.session_state.customer_segmentation.get_customer_lifetime_value(st.session_state.sales_data)
    
    if not clv_data.empty:
        clv_col1, clv_col2 = st.columns(2)
        
        with clv_col1:
            # CLV Distribution
            fig_clv = px.histogram(
                clv_data,
                x='predicted_clv',
                title="Customer Lifetime Value Distribution",
                labels={'predicted_clv': 'Predicted CLV ($)'},
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig_clv, use_container_width=True)
        
        with clv_col2:
            # CLV by Quartile
            clv_quartile_counts = clv_data['clv_quartile'].value_counts()
            fig_quartile = px.pie(
                values=clv_quartile_counts.values,
                names=clv_quartile_counts.index,
                title="CLV Quartile Distribution",
                color_discrete_sequence=['#ff6b9d', '#feca57', '#ff6b35', '#0abde3']
            )
            st.plotly_chart(fig_quartile, use_container_width=True)
        
        # Top CLV customers
        st.markdown("### 🌟 Top Value Customers")
        top_clv = clv_data.nlargest(10, 'predicted_clv')[['customer_id', 'total_spent', 'avg_order_value', 'predicted_clv']].round(2)
        st.dataframe(top_clv, use_container_width=True)

def show_predictive_analytics():
    """Display predictive analytics and forecasting"""
    if st.session_state.sales_data.empty:
        st.info("📊 No data available for predictions. Generate some data first!")
        return
    
    st.markdown("""
    <div class="main-header">
        <h1>🔮 Predictive Analytics & Forecasting</h1>
        <p>AI-powered predictions and future insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sales Forecasting
    st.markdown("## 📈 Sales Forecasting")
    
    forecast_days = st.slider("📅 Forecast Period (Days)", 1, 14, 7)
    
    with st.spinner("🤖 Generating sales forecast..."):
        forecast_df, forecast_metrics = st.session_state.predictive_analytics.forecast_sales(
            st.session_state.sales_data, forecast_days=forecast_days
        )
    
    if not forecast_df.empty:
        # Display forecast metrics
        forecast_col1, forecast_col2, forecast_col3, forecast_col4 = st.columns(4)
        
        with forecast_col1:
            st.metric("🎯 Model Accuracy", f"{forecast_metrics.get('model_score', 0)*100:.1f}%")
        
        with forecast_col2:
            st.metric("📊 Forecast Total", f"${forecast_metrics.get('forecast_total', 0):,.2f}")
        
        with forecast_col3:
            st.metric("📉 MAE", f"{forecast_metrics.get('mae', 0):.2f}")
        
        with forecast_col4:
            st.metric("📊 RMSE", f"{forecast_metrics.get('rmse', 0):.2f}")
        
        # Forecast visualization
        fig_forecast = go.Figure()
        
        # Historical data
        historical = st.session_state.sales_data.copy()
        historical['timestamp'] = pd.to_datetime(historical['timestamp'])
        historical_hourly = historical.groupby(historical['timestamp'].dt.floor('H'))['total_amount'].sum().reset_index()
        
        fig_forecast.add_trace(go.Scatter(
            x=historical_hourly['timestamp'],
            y=historical_hourly['total_amount'],
            mode='lines',
            name='Historical Sales',
            line=dict(color='#3498db', width=2)
        ))
        
        # Forecast
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['predicted_revenue'],
            mode='lines',
            name='Forecast',
            line=dict(color='#e74c3c', width=3, dash='dash')
        ))
        
        # Confidence intervals
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['confidence_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['confidence_lower'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(231, 76, 60, 0.2)',
            name='Confidence Interval',
            hoverinfo='skip'
        ))
        
        fig_forecast.update_layout(
            title=f"Sales Forecast for Next {forecast_days} Days",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            height=500
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Demand Forecasting
    st.markdown("## 📦 Product Demand Forecasting")
    
    with st.spinner("🔄 Analyzing product demand..."):
        demand_df, demand_metrics = st.session_state.predictive_analytics.demand_forecasting(st.session_state.sales_data)
    
    if not demand_df.empty:
        demand_col1, demand_col2 = st.columns(2)
        
        with demand_col1:
            # Demand trend visualization
            fig_demand = px.bar(
                demand_df.head(10),
                y='product_name',
                x='predicted_7d_total',
                orientation='h',
                title="Top 10 Products - 7-Day Demand Forecast",
                labels={'predicted_7d_total': 'Predicted Demand', 'product_name': 'Product'},
                color='trend_slope',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_demand, use_container_width=True)
        
        with demand_col2:
            # Trend direction analysis
            trend_counts = demand_df['trend_direction'].value_counts()
            fig_trend = px.pie(
                values=trend_counts.values,
                names=trend_counts.index,
                title="Product Demand Trends",
                color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c']
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # Seasonal Analysis
    st.markdown("## 📅 Seasonal Analysis")
    
    seasonal_data = st.session_state.predictive_analytics.seasonal_analysis(st.session_state.sales_data)
    
    if seasonal_data and 'hourly_patterns' in seasonal_data:
        seasonal_col1, seasonal_col2 = st.columns(2)
        
        with seasonal_col1:
            # Hourly patterns
            hourly_df = pd.DataFrame.from_dict(seasonal_data['hourly_patterns'], orient='index')
            if 'total_amount' in hourly_df.columns:
                hourly_df = hourly_df.reset_index()
                hourly_df.columns = ['Hour', 'Avg_Revenue', 'Transaction_Count']
                
                fig_hourly = px.bar(
                    hourly_df,
                    x='Hour',
                    y='Avg_Revenue',
                    title="Average Revenue by Hour of Day",
                    labels={'Avg_Revenue': 'Average Revenue ($)', 'Hour': 'Hour of Day'}
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
        
        with seasonal_col2:
            # Category peak hours
            if 'category_peaks' in seasonal_data:
                peak_data = []
                for category, data in seasonal_data['category_peaks'].items():
                    peak_data.append({
                        'Category': category,
                        'Peak Hour': data['peak_hour'],
                        'Peak Revenue': data['peak_revenue']
                    })
                
                if peak_data:
                    peak_df = pd.DataFrame(peak_data)
                    fig_peaks = px.scatter(
                        peak_df,
                        x='Peak Hour',
                        y='Peak Revenue',
                        color='Category',
                        size='Peak Revenue',
                        title="Category Peak Hours",
                        labels={'Peak Hour': 'Hour of Day', 'Peak Revenue': 'Peak Revenue ($)'}
                    )
                    st.plotly_chart(fig_peaks, use_container_width=True)

def show_reports():
    """Display reports and export functionality"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Smart Reports & Analytics</h1>
        <p>Comprehensive reports with actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.sales_data.empty:
        st.info("📊 No data available for reports. Generate some data first!")
        return
    
    # Report generation options
    st.markdown("## 📊 Report Options")
    
    report_col1, report_col2, report_col3 = st.columns(3)
    
    with report_col1:
        if st.button("📈 Generate Executive Summary"):
            with st.spinner("📝 Generating executive report..."):
                analytics_results = st.session_state.analytics_engine.calculate_metrics(st.session_state.sales_data)
                report = st.session_state.report_generator.generate_comprehensive_report(
                    st.session_state.sales_data, analytics_results
                )
                st.session_state.generated_report = report
    
    with report_col2:
        if st.button("👥 Customer Analysis Report"):
            with st.spinner("👥 Generating customer report..."):
                analytics_results = st.session_state.analytics_engine.calculate_metrics(st.session_state.sales_data)
                rfm_data, segment_stats = st.session_state.customer_segmentation.segment_customers(st.session_state.sales_data)
                customer_segments = {'segment_stats': segment_stats}
                report = st.session_state.report_generator.generate_comprehensive_report(
                    st.session_state.sales_data, analytics_results, customer_segments
                )
                st.session_state.generated_report = report
    
    with report_col3:
        if st.button("🔮 Predictive Insights Report"):
            with st.spinner("🔮 Generating predictive report..."):
                analytics_results = st.session_state.analytics_engine.calculate_metrics(st.session_state.sales_data)
                forecast_df, forecast_metrics = st.session_state.predictive_analytics.forecast_sales(st.session_state.sales_data)
                demand_df, demand_metrics = st.session_state.predictive_analytics.demand_forecasting(st.session_state.sales_data)
                predictions = {'sales_forecast': forecast_metrics, 'demand_forecast': demand_metrics}
                report = st.session_state.report_generator.generate_comprehensive_report(
                    st.session_state.sales_data, analytics_results, predictions=predictions
                )
                st.session_state.generated_report = report
    
    # Display generated report
    if st.session_state.generated_report:
        st.markdown("## 📄 Generated Report")
        st.markdown(st.session_state.generated_report)
        
        # Export options
        st.markdown("## 📤 Export Options")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # Export data to CSV
            csv_content, filename = st.session_state.report_generator.export_to_csv(st.session_state.sales_data)
            st.download_button(
                label="📊 Download Data (CSV)",
                data=csv_content,
                file_name=filename,
                mime="text/csv"
            )
        
        with export_col2:
            # Export report as text
            st.download_button(
                label="📋 Download Report (TXT)",
                data=st.session_state.generated_report,
                file_name=f"retail_analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# Main navigation
def main():
    # Navigation
    st.markdown("""
    <div class="nav-pills">
    """, unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    
    with nav_col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.current_page = "Home"
    
    with nav_col2:
        if st.button("📊 Dashboard", key="nav_dashboard"):
            st.session_state.current_page = "Dashboard"
    
    with nav_col3:
        if st.button("👥 Customers", key="nav_customers"):
            st.session_state.current_page = "Customers"
    
    with nav_col4:
        if st.button("🔮 Predictions", key="nav_predictions"):
            st.session_state.current_page = "Predictions"
    
    with nav_col5:
        if st.button("📋 Reports", key="nav_reports"):
            st.session_state.current_page = "Reports"
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == "Home":
        show_homepage()
    elif st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Customers":
        show_customer_analytics()
    elif st.session_state.current_page == "Predictions":
        show_predictive_analytics()
    elif st.session_state.current_page == "Reports":
        show_reports()
    
    # Sidebar status
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.write(f"**🔄 Streaming:** {'🟢 Active' if st.session_state.is_streaming else '🔴 Inactive'}")
        st.write(f"**📈 Records:** {len(st.session_state.sales_data):,}")
        st.write(f"**⏰ Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
        st.write(f"**📱 Current Page:** {st.session_state.current_page}")

if __name__ == "__main__":
    main()