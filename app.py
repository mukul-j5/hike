import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

from data_fetcher import DataFetcher
from project_data import get_web3_projects
from utils import (format_number, calculate_metrics, get_color_palette,
                   calculate_token_velocity, calculate_burn_rate_estimate,
                   calculate_market_cap_to_dau_ratio)

# Page configuration
st.set_page_config(page_title="Web3 Revenue Dashboard",
                   page_icon="📊",
                   layout="wide",
                   initial_sidebar_state="expanded")


# Initialize data fetcher
@st.cache_resource
def init_data_fetcher():
    return DataFetcher()


data_fetcher = init_data_fetcher()

# Main title
st.title("🚀 Web3 Revenue & Metrics Dashboard")
st.markdown("---")

# Sidebar for filters and controls
st.sidebar.header("🔧 Dashboard Controls")


# Category filter with counts
@st.cache_data(ttl=300)
def get_category_counts():
    projects = get_web3_projects()
    web3_count = len([p for p in projects if p['category'] == 'Web3'])
    gaming_count = len([p for p in projects if p['category'] == 'Web3 Gaming'])
    return web3_count, gaming_count


web3_count, gaming_count = get_category_counts()
category_options = [
    "All (100 projects)", f"Web3 ({web3_count} projects)",
    f"Web3 Gaming ({gaming_count} projects)"
]

category_filter = st.sidebar.selectbox("Select Category", category_options)

# Convert display format back to internal format
if "Web3 Gaming" in category_filter:
    category_filter = "Web3 Gaming"
elif "Web3" in category_filter and "Gaming" not in category_filter:
    category_filter = "Web3"
else:
    category_filter = "All"

# Refresh data button
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    st.cache_data.clear()
    st.rerun()

# Auto-refresh controls
st.sidebar.subheader("Auto-refresh Settings")
auto_refresh = st.sidebar.checkbox("Enable auto-refresh", value=False)
if auto_refresh:
    refresh_interval = st.sidebar.selectbox(
        "Refresh interval", [15, 30, 60],
        index=1,
        format_func=lambda x: f"{x} seconds")
else:
    refresh_interval = 30

# Search functionality with instant filtering
search_term = st.sidebar.text_input(
    "🔍 Search Projects",
    placeholder="Type project name or symbol...",
    help="Search supports partial matches")


# Load project data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_project_data():
    projects = get_web3_projects()
    market_data = data_fetcher.get_market_data([p['symbol'] for p in projects])

    # Combine project info with market data
    combined_data = []
    for project in projects:
        symbol = project['symbol']
        if symbol in market_data:
            market_info = market_data[symbol]
            project_data = {
                **project,
                **market_info, 'revenue_per_user':
                calculate_metrics(market_info),
                'token_velocity':
                calculate_token_velocity(market_info.get('volume_24h', 0),
                                         market_info.get('market_cap', 0)),
                'burn_rate_estimate':
                calculate_burn_rate_estimate(market_info),
                'mcap_dau_ratio':
                calculate_market_cap_to_dau_ratio(
                    market_info.get('market_cap', 0),
                    market_info.get('volume_24h', 0),
                    market_info.get('price', 0))
            }
            combined_data.append(project_data)

    return pd.DataFrame(combined_data)


# Load data
try:
    with st.spinner("Loading project data..."):
        df = load_project_data()

    if df.empty:
        st.error("No data available. Please check API connectivity.")
        st.stop()

    # Apply filters
    filtered_df = df.copy()

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]

    if search_term:
        filtered_df = filtered_df[filtered_df['name'].str.
                                  contains(search_term, case=False, na=False)
                                  | filtered_df['symbol'].str.
                                  contains(search_term, case=False, na=False)]

    # Key metrics overview
    st.header("📈 Strategic Business Metrics")

    col1, col2, col3, col4 = st.columns(4)

    # Calculate meaningful metrics
    high_velocity_projects = len(
        filtered_df[filtered_df['token_velocity'] > 0.1])
    total_projects = len(filtered_df)
    velocity_adoption_rate = (high_velocity_projects / total_projects *
                              100) if total_projects > 0 else 0

    profitable_projects = len(
        filtered_df[filtered_df['revenue_per_user'] > 1.0])
    profitability_rate = (profitable_projects / total_projects *
                          100) if total_projects > 0 else 0

    # Market efficiency: Volume/Market Cap ratio
    efficient_projects = len(filtered_df[filtered_df['token_velocity'] > 0.05])
    efficiency_rate = (efficient_projects / total_projects *
                       100) if total_projects > 0 else 0

    # Growth momentum: positive performers in last 7 days
    growth_projects = len(filtered_df[filtered_df['percent_change_7d'] > 0])
    growth_momentum = (growth_projects / total_projects *
                       100) if total_projects > 0 else 0

    with col1:
        st.metric(
            label="🔄 Token Utility Rate",
            value=f"{velocity_adoption_rate:.1f}%",
            delta=f"{high_velocity_projects}/{total_projects} active",
            help=
            "Projects with meaningful token velocity (>0.1x daily turnover)")

    with col2:
        st.metric(label="💰 Revenue Efficiency",
                  value=f"{profitability_rate:.1f}%",
                  delta=f"{profitable_projects} profitable",
                  help="Projects generating >$1 revenue per user")

    with col3:
        st.metric(
            label="⚡ Market Efficiency",
            value=f"{efficiency_rate:.1f}%",
            delta=f"{efficient_projects} liquid",
            help="Projects with healthy trading activity relative to valuation"
        )

    with col4:
        st.metric(
            label="📈 Growth Momentum",
            value=f"{growth_momentum:.1f}%",
            delta=f"7-day trend",
            help="Percentage of projects with positive 7-day performance")

    # Business Intelligence Section
    st.header("🧠 Business Intelligence Insights")

    # Create insight cards
    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        # Top performers by actual utility
        top_utility = filtered_df.nlargest(
            3, 'token_velocity')[['name', 'token_velocity']]
        st.subheader("🚀 Highest Utility Projects")
        for idx, row in top_utility.iterrows():
            st.write(
                f"**{row['name']}**: {row['token_velocity']:.3f}x daily turnover"
            )

    with insight_col2:
        # Most capital efficient
        capital_efficient = filtered_df[
            filtered_df['revenue_per_user'] > 0].nlargest(
                3, 'revenue_per_user')[['name', 'revenue_per_user']]
        st.subheader("💡 Most Capital Efficient")
        for idx, row in capital_efficient.iterrows():
            st.write(f"**{row['name']}**: ${row['revenue_per_user']:.2f}/user")

    with insight_col3:
        # Undervalued opportunities (high utility, lower market cap)
        filtered_df['utility_score'] = filtered_df['token_velocity'] / (
            filtered_df['market_cap'] / 1e9)  # Utility per $1B market cap
        undervalued = filtered_df[filtered_df['utility_score'] > 0].nlargest(
            3, 'utility_score')[['name', 'utility_score']]
        st.subheader("💎 Potential Value Plays")
        for idx, row in undervalued.iterrows():
            st.write(
                f"**{row['name']}**: {row['utility_score']:.4f} utility/cap ratio"
            )

    st.markdown("---")

    # Charts section
    st.header("📊 Interactive Analytics")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "Market Overview", "Revenue Metrics", "Token Analysis", "Performance"
    ])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Market cap vs volume scatter plot with enhanced tooltips
            fig_scatter = px.scatter(
                filtered_df,
                x="market_cap",
                y="volume_24h",
                size="circulating_supply",
                color="category",
                hover_name="name",
                hover_data={
                    "market_cap": ":$,.0f",
                    "volume_24h": ":$,.0f",
                    "price": ":$.4f",
                    "revenue_per_user": ":$.2f",
                    "token_velocity": ":.4f",
                    "circulating_supply": ":,.0f"
                },
                title="Market Cap vs 24h Volume (Log-Log Scale)",
                labels={
                    "market_cap": "Market Cap ($) - Log Scale",
                    "volume_24h": "24h Volume ($) - Log Scale",
                    "circulating_supply": "Bubble Size: Circulating Supply"
                },
                color_discrete_map={
                    "Web3": "#1f77b4",
                    "Web3 Gaming": "#ff7f0e"
                })
            fig_scatter.update_layout(xaxis_type="log",
                                      yaxis_type="log",
                                      legend=dict(orientation="h",
                                                  yanchor="bottom",
                                                  y=1.02,
                                                  xanchor="right",
                                                  x=1))
            # Add size legend annotation
            fig_scatter.add_annotation(text="Bubble Size = Circulating Supply",
                                       xref="paper",
                                       yref="paper",
                                       x=0.02,
                                       y=0.98,
                                       showarrow=False,
                                       font=dict(size=10, color="gray"))
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col2:
            # Enhanced category distribution with counts
            category_counts = filtered_df['category'].value_counts()
            total_projects = len(filtered_df)

            # Create labels with counts and percentages
            labels_with_counts = [
                f"{cat}: {count} projects ({count/total_projects*100:.1f}%)"
                for cat, count in category_counts.items()
            ]

            fig_pie = px.pie(
                values=category_counts.values,
                names=labels_with_counts,
                title="Projects by Category Distribution",
                color_discrete_map={
                    f"Web3: {category_counts.get('Web3', 0)} projects ({category_counts.get('Web3', 0)/total_projects*100:.1f}%)":
                    "#1f77b4",
                    f"Web3 Gaming: {category_counts.get('Web3 Gaming', 0)} projects ({category_counts.get('Web3 Gaming', 0)/total_projects*100:.1f}%)":
                    "#ff7f0e"
                })
            fig_pie.update_traces(textposition='inside',
                                  textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        # Revenue Metrics Section
        st.subheader("📊 Revenue & User Metrics")

        col1, col2 = st.columns(2)

        with col1:
            # Revenue per user with improved formatting
            revenue_data = filtered_df.nlargest(20, 'revenue_per_user')
            fig_revenue = px.bar(
                revenue_data,
                x="name",
                y="revenue_per_user",
                color="category",
                title="Revenue per User (Top 20 Projects)",
                labels={"revenue_per_user": "Revenue per User ($)"},
                color_discrete_map={
                    "Web3": "#1f77b4",
                    "Web3 Gaming": "#ff7f0e"
                },
                hover_data={
                    "revenue_per_user": ":$.2f",
                    "market_cap": ":$,.0f",
                    "volume_24h": ":$,.0f"
                })
            fig_revenue.update_layout(xaxis_tickangle=-45,
                                      xaxis_title="Project Name",
                                      yaxis_title="Revenue per User ($)",
                                      showlegend=True,
                                      legend=dict(orientation="h",
                                                  yanchor="bottom",
                                                  y=1.02,
                                                  xanchor="right",
                                                  x=1))
            st.plotly_chart(fig_revenue, use_container_width=True)

        with col2:
            # Market Cap to DAU Ratio with reference lines
            mcap_dau_data = filtered_df[filtered_df['mcap_dau_ratio'] >
                                        0].nlargest(20, 'mcap_dau_ratio')
            fig_mcap_dau = px.scatter(
                mcap_dau_data,
                x="volume_24h",
                y="mcap_dau_ratio",
                size="market_cap",
                color="category",
                hover_name="name",
                title="Market Cap/DAU Ratio - User Value Assessment",
                labels={
                    "volume_24h": "24h Volume ($) - Log Scale",
                    "mcap_dau_ratio": "Market Cap per Daily Active User ($)"
                },
                color_discrete_map={
                    "Web3": "#1f77b4",
                    "Web3 Gaming": "#ff7f0e"
                },
                hover_data={
                    "mcap_dau_ratio": ":$,.0f",
                    "volume_24h": ":$,.0f",
                    "market_cap": ":$,.0f"
                })
            fig_mcap_dau.update_layout(xaxis_type="log",
                                       legend=dict(orientation="h",
                                                   yanchor="bottom",
                                                   y=1.02,
                                                   xanchor="right",
                                                   x=1))
            # Add reference line at $1 per user
            fig_mcap_dau.add_hline(y=1,
                                   line_dash="dash",
                                   line_color="red",
                                   annotation_text="$1 per DAU baseline")
            st.plotly_chart(fig_mcap_dau, use_container_width=True)

        # Burn Rate Analysis
        col3, col4 = st.columns(2)

        with col3:
            # Burn rate estimates
            burn_data = filtered_df[filtered_df['burn_rate_estimate'] >
                                    0].nlargest(15, 'burn_rate_estimate')
            if not burn_data.empty:
                fig_burn = px.bar(
                    burn_data,
                    x="name",
                    y="burn_rate_estimate",
                    color="category",
                    title="Token Burn Rate Estimates (%)",
                    labels={"burn_rate_estimate": "Estimated Burn Rate (%)"})
                fig_burn.update_xaxes(tickangle=45)
                st.plotly_chart(fig_burn, use_container_width=True)
            else:
                st.info("Burn rate data not available for current selection")

        with col4:
            # Revenue efficiency heatmap
            top_projects = filtered_df.nlargest(15, 'revenue_per_user')
            metrics_for_heatmap = top_projects[[
                'name', 'revenue_per_user', 'token_velocity', 'mcap_dau_ratio'
            ]]

            fig_heatmap = px.imshow(metrics_for_heatmap.set_index('name').T,
                                    title="Revenue Metrics Heatmap (Top 15)",
                                    color_continuous_scale="Viridis",
                                    aspect="auto")
            fig_heatmap.update_xaxes(tickangle=45)
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab3:
        # Token Analysis Section
        st.subheader("🔄 Token Velocity & Supply Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Token velocity horizontal bar chart for better readability
            velocity_data = filtered_df[filtered_df['token_velocity'] >
                                        0].nlargest(15, 'token_velocity')
            fig_velocity = px.bar(
                velocity_data,
                x="token_velocity",
                y="name",
                color="category",
                orientation='h',
                title="Token Velocity - How Many Times Token Turns Over in 24h",
                labels={
                    "token_velocity": "Token Velocity (Volume/Market Cap)",
                    "name": "Project"
                },
                color_discrete_map={
                    "Web3": "#1f77b4",
                    "Web3 Gaming": "#ff7f0e"
                },
                hover_data={
                    "token_velocity": ":.4f",
                    "volume_24h": ":$,.0f",
                    "market_cap": ":$,.0f"
                })
            fig_velocity.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                legend=dict(orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1))
            # Add reference line at velocity = 1
            fig_velocity.add_vline(x=1,
                                   line_dash="dash",
                                   line_color="gray",
                                   annotation_text="High Velocity Threshold")
            st.plotly_chart(fig_velocity, use_container_width=True)

        with col2:
            # Price vs circulating supply
            fig_supply = px.scatter(filtered_df,
                                    x="circulating_supply",
                                    y="price",
                                    color="category",
                                    size="market_cap",
                                    hover_name="name",
                                    title="Price vs Circulating Supply",
                                    labels={
                                        "circulating_supply":
                                        "Circulating Supply",
                                        "price": "Price ($)"
                                    })
            fig_supply.update_layout(xaxis_type="log")
            st.plotly_chart(fig_supply, use_container_width=True)

        # Additional token metrics
        col3, col4 = st.columns(2)

        with col3:
            # Supply utilization
            supply_data = filtered_df[(filtered_df['total_supply'] > 0) & (
                filtered_df['circulating_supply'] > 0)].copy()

            if not supply_data.empty:
                supply_data['supply_ratio'] = supply_data[
                    'circulating_supply'] / supply_data['total_supply']
                supply_data = supply_data.nlargest(15, 'supply_ratio')

                fig_supply_ratio = px.bar(
                    supply_data,
                    x="name",
                    y="supply_ratio",
                    color="category",
                    title="Supply Utilization Ratio (Top 15)",
                    labels={"supply_ratio": "Circulating/Total Supply Ratio"})
                fig_supply_ratio.update_xaxes(tickangle=45)
                st.plotly_chart(fig_supply_ratio, use_container_width=True)
            else:
                st.info("Supply data not available for current selection")

        with col4:
            # Token velocity vs Market Cap
            velocity_vs_mcap = filtered_df[filtered_df['token_velocity'] > 0]
            fig_velocity_scatter = px.scatter(
                velocity_vs_mcap,
                x="market_cap",
                y="token_velocity",
                color="category",
                size="volume_24h",
                hover_name="name",
                title="Token Velocity vs Market Cap",
                labels={
                    "market_cap": "Market Cap ($)",
                    "token_velocity": "Token Velocity"
                })
            fig_velocity_scatter.update_layout(xaxis_type="log")
            st.plotly_chart(fig_velocity_scatter, use_container_width=True)

    with tab4:
        # Enhanced Performance heatmap
        st.subheader("📊 Price Performance Analysis")

        performance_cols = [
            'percent_change_1h', 'percent_change_24h', 'percent_change_7d'
        ]
        if all(col in filtered_df.columns for col in performance_cols):
            # Sort by 24h performance for better ordering
            performance_data = filtered_df.nlargest(
                20, 'percent_change_24h')[['name'] + performance_cols]

            # Create heatmap matrix
            heatmap_matrix = performance_data[performance_cols].T.values

            fig_heatmap = px.imshow(
                heatmap_matrix,
                labels={
                    'x': 'Projects (sorted by 24h performance)',
                    'y': 'Time Period',
                    'color': 'Price Change (%)'
                },
                x=performance_data['name'].tolist(),
                y=['1 Hour', '24 Hours', '7 Days'],  # Logical time ordering
                title=
                "Price Performance Heatmap - Top 20 Projects by 24h Change",
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                zmin=-10,
                zmax=10  # Better scale for percentage changes
            )

            fig_heatmap.update_layout(xaxis_tickangle=-45,
                                      height=400,
                                      font=dict(size=10))

            # Add annotations for extreme values
            for i, (idx, row) in enumerate(performance_data.iterrows()):
                for j, col in enumerate(performance_cols):
                    value = row[col]
                    if abs(value) > 5:  # Highlight significant changes
                        fig_heatmap.add_annotation(
                            x=i,
                            y=j,
                            text=f"{value:.1f}%",
                            showarrow=False,
                            font=dict(
                                color="white" if abs(value) > 7 else "black",
                                size=8))

            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("Performance data not available for selected projects")

    # Project table
    st.header("📋 Project Details")

    # Prepare display columns with key metrics
    display_columns = [
        'name', 'symbol', 'category', 'price', 'market_cap', 'volume_24h',
        'revenue_per_user', 'token_velocity', 'burn_rate_estimate',
        'mcap_dau_ratio', 'percent_change_24h', 'circulating_supply'
    ]

    display_df = filtered_df[display_columns].copy()

    # Format columns for display
    display_df['price'] = display_df['price'].apply(
        lambda x: f"${x:.4f}" if pd.notnull(x) else "N/A")
    display_df['market_cap'] = display_df['market_cap'].apply(
        lambda x: f"${format_number(float(x))}" if pd.notnull(x) else "N/A")
    display_df['volume_24h'] = display_df['volume_24h'].apply(
        lambda x: f"${format_number(float(x))}" if pd.notnull(x) else "N/A")
    display_df['revenue_per_user'] = display_df['revenue_per_user'].apply(
        lambda x: f"${x:.2f}" if pd.notnull(x) and x > 0 else "N/A")
    display_df['token_velocity'] = display_df['token_velocity'].apply(
        lambda x: f"{x:.4f}" if pd.notnull(x) and x > 0 else "N/A")
    display_df['burn_rate_estimate'] = display_df['burn_rate_estimate'].apply(
        lambda x: f"{x:.2f}%" if pd.notnull(x) and x > 0 else "N/A")
    display_df['mcap_dau_ratio'] = display_df['mcap_dau_ratio'].apply(
        lambda x: f"${format_number(float(x))}"
        if pd.notnull(x) and x > 0 else "N/A")
    display_df['percent_change_24h'] = display_df['percent_change_24h'].apply(
        lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
    display_df['circulating_supply'] = display_df['circulating_supply'].apply(
        lambda x: format_number(float(x)) if pd.notnull(x) else "N/A")

    st.dataframe(display_df,
                 column_config={
                     "name":
                     st.column_config.TextColumn("Project Name",
                                                 width="medium"),
                     "symbol":
                     st.column_config.TextColumn("Symbol", width="small"),
                     "category":
                     st.column_config.TextColumn("Category", width="small"),
                     "price":
                     st.column_config.NumberColumn("Price",
                                                   format="$%.4f",
                                                   width="small"),
                     "market_cap":
                     st.column_config.TextColumn("Market Cap", width="medium"),
                     "volume_24h":
                     st.column_config.TextColumn("24h Volume", width="medium"),
                     "revenue_per_user":
                     st.column_config.TextColumn("Revenue/User",
                                                 width="small"),
                     "token_velocity":
                     st.column_config.TextColumn("Token Velocity",
                                                 width="small"),
                     "burn_rate_estimate":
                     st.column_config.TextColumn("Burn Rate %", width="small"),
                     "mcap_dau_ratio":
                     st.column_config.TextColumn("Market Cap/DAU",
                                                 width="medium"),
                     "percent_change_24h":
                     st.column_config.TextColumn("24h Change", width="small"),
                     "circulating_supply":
                     st.column_config.TextColumn("Circulating Supply",
                                                 width="medium")
                 },
                 use_container_width=True,
                 height=600,
                 hide_index=True)

    # News feed section
    st.header("📰 Web3 News Feed")

    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def load_news():
        return data_fetcher.get_web3_news()

    try:
        news_articles = load_news()

        if news_articles:
            for article in news_articles[:10]:  # Show top 10 news
                with st.expander(f"📄 {article['title']}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(article['description'])
                        if article.get('url'):
                            st.link_button("Read Full Article", article['url'])
                    with col2:
                        st.write(
                            f"**Source:** {article.get('source', 'Unknown')}")
                        st.write(
                            f"**Published:** {article.get('published_at', 'Unknown')}"
                        )
        else:
            st.info("No recent news articles available.")

    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

    # Footer with last update time
    st.markdown("---")
    st.caption(
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

except Exception as e:
    st.error(f"Error loading dashboard: {str(e)}")
    st.info("Please check your internet connection and API keys.")
