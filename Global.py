import pandas as pd
import plotly.express as px
from datetime import datetime

def process_energy_data(raw_data_path):
    """Process raw energy consumption data and prepare for visualization"""
    # Load and clean data
    df = pd.read_csv(raw_data_path)
    
    # Data cleaning and transformation
    df['date'] = pd.to_datetime(df['date'])
    df['consumption'] = pd.to_numeric(df['consumption'], errors='coerce')
    
    # Calculate key metrics
    df['renewable_percentage'] = (df['renewable_energy'] / df['total_energy']) * 100
    df['yoy_change'] = df.groupby('country')['consumption'].pct_change() * 100
    
    # Create time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # Calculate rolling averages
    df['consumption_ma'] = df.groupby('country')['consumption'].rolling(
        window=12, min_periods=1
    ).mean().reset_index(0, drop=True)
    
    return df

def create_choropleth(df):
    """Create an interactive choropleth map"""
    fig = px.choropleth(
        df,
        locations='country_code',
        color='renewable_percentage',
        hover_name='country',
        color_continuous_scale='viridis',
        title='Global Renewable Energy Adoption'
    )
    
    fig.update_layout(
        title_x=0.5,
        geo=dict(showframe=False, showcoastlines=True),
        width=1000,
        height=600
    )
    
    return fig

def generate_trend_analysis(df):
    """Generate trend analysis visualizations"""
    # Create time series plot
    fig = px.line(
        df,
        x='date',
        y='consumption_ma',
        color='country',
        title='Energy Consumption Trends by Country'
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Energy Consumption (TWh)',
        legend_title='Country',
        hovermode='x unified'
    )
    
    return fig

def calculate_sustainability_metrics(df):
    """Calculate sustainability-related metrics"""
    metrics = {
        'total_renewable_energy': df['renewable_energy'].sum(),
        'average_adoption_rate': df['renewable_percentage'].mean(),
        'top_performers': df.nlargest(5, 'renewable_percentage')[
            ['country', 'renewable_percentage']
        ].to_dict('records'),
        'year_over_year_growth': df.groupby('year')['renewable_percentage'].mean().pct_change().iloc[-1]
    }
    
    return metrics