"""
Utility functions for the Web3 dashboard
"""
import numpy as np
from typing import Dict, Any, List

def format_number(num: float) -> str:
    """
    Format large numbers with appropriate suffixes (K, M, B, T)
    """
    if num is None or np.isnan(num):
        return "0"
    
    if abs(num) >= 1e12:
        return f"{num/1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"{num/1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"{num/1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"

def calculate_metrics(market_data: Dict[str, Any]) -> float:
    """
    Calculate revenue per user approximation based on market data
    Uses market cap and volume to estimate revenue efficiency
    """
    try:
        market_cap = market_data.get('market_cap', 0)
        volume_24h = market_data.get('volume_24h', 0)
        price = market_data.get('price', 1)
        
        if market_cap > 0 and volume_24h > 0 and price > 0:
            # Estimate daily active users from volume and price
            estimated_transactions = volume_24h / (price * 5)  # Assume avg transaction is 5 tokens
            estimated_dau = max(1, estimated_transactions / 3)  # Assume 3 transactions per user
            
            # Revenue per user approximation
            revenue_per_user = (volume_24h * 0.003) / estimated_dau  # Assume 0.3% transaction fee
            return revenue_per_user
        
        return 0.0
    except (ZeroDivisionError, TypeError):
        return 0.0

def calculate_token_velocity(volume_24h: float, market_cap: float) -> float:
    """
    Calculate token velocity (Volume / Market Cap)
    Higher velocity indicates more frequent token usage
    """
    try:
        if market_cap > 0:
            return volume_24h / market_cap
        return 0.0
    except (ZeroDivisionError, TypeError):
        return 0.0

def calculate_burn_rate_estimate(supply_data: Dict[str, Any]) -> float:
    """
    Estimate burn rate based on supply metrics
    This is an approximation since real burn data requires specialized APIs
    """
    try:
        circulating_supply = supply_data.get('circulating_supply', 0)
        total_supply = supply_data.get('total_supply', 0)
        max_supply = supply_data.get('max_supply', 0)
        
        if max_supply and total_supply and max_supply > 0:
            # Estimate based on supply utilization
            burn_estimate = ((max_supply - total_supply) / max_supply) * 100
            return max(0, burn_estimate)
        
        return 0.0
    except (ZeroDivisionError, TypeError):
        return 0.0

def calculate_market_cap_to_dau_ratio(market_cap: float, volume_24h: float, price: float) -> float:
    """
    Approximate Market Cap to Daily Active Users ratio
    Uses volume and price to estimate daily active users
    """
    try:
        if price > 0 and volume_24h > 0:
            # Rough estimation: daily volume / average transaction size
            estimated_daily_transactions = volume_24h / (price * 10)  # Assume avg transaction is 10 tokens
            estimated_dau = estimated_daily_transactions / 5  # Assume 5 transactions per user per day
            
            if estimated_dau > 0:
                return market_cap / estimated_dau
        
        return 0.0
    except (ZeroDivisionError, TypeError):
        return 0.0

def get_color_palette() -> List[str]:
    """
    Returns a professional color palette for charts
    """
    return [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf'   # Cyan
    ]

def validate_api_response(response_data: Dict) -> bool:
    """
    Validate API response structure
    """
    if not isinstance(response_data, dict):
        return False
    
    required_fields = ['data']
    return all(field in response_data for field in required_fields)

def clean_numeric_data(value: Any, default: float = 0.0) -> float:
    """
    Clean and validate numeric data from API responses
    """
    if value is None:
        return default
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def calculate_performance_score(price_changes: Dict[str, float]) -> float:
    """
    Calculate overall performance score based on price changes
    """
    try:
        weights = {
            'percent_change_1h': 0.1,
            'percent_change_24h': 0.4,
            'percent_change_7d': 0.5
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for period, change in price_changes.items():
            if period in weights and change is not None:
                weighted_score += change * weights[period]
                total_weight += weights[period]
        
        if total_weight > 0:
            return weighted_score / total_weight
        
        return 0.0
    except (TypeError, KeyError):
        return 0.0

def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format percentage values with appropriate styling
    """
    if value is None or np.isnan(value):
        return "0.00%"
    
    formatted = f"{value:.{decimals}f}%"
    return formatted

def get_risk_level(volatility: float) -> str:
    """
    Categorize risk level based on volatility
    """
    if volatility < 5:
        return "Low"
    elif volatility < 15:
        return "Medium"
    elif volatility < 30:
        return "High"
    else:
        return "Very High"

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe ratio for risk-adjusted returns
    """
    try:
        if not returns or len(returns) < 2:
            return 0.0
        
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return == 0:
            return 0.0
        
        return float((mean_return - risk_free_rate) / std_return)
    except (TypeError, ValueError):
        return 0.0

def calculate_network_value_score(market_cap: float, volume_24h: float, velocity: float) -> float:
    """
    Calculate a composite network value score based on utility and size
    Higher score indicates better network value proposition
    """
    try:
        if market_cap <= 0 or volume_24h <= 0:
            return 0.0
        
        # Network effect score: larger networks with high utility score higher
        size_factor = np.log10(market_cap / 1e6)  # Log scale for market cap in millions
        utility_factor = min(velocity * 10, 5)  # Cap utility factor at 5x
        liquidity_factor = volume_24h / market_cap  # Volume to market cap ratio
        
        # Composite score with weights
        score = (size_factor * 0.3) + (utility_factor * 0.5) + (liquidity_factor * 20 * 0.2)
        return max(0, score)
    except (ValueError, TypeError):
        return 0.0

def calculate_sustainability_index(revenue_per_user: float, burn_rate: float, velocity: float) -> float:
    """
    Calculate project sustainability index
    Higher score indicates more sustainable tokenomics
    """
    try:
        revenue_score = min(revenue_per_user, 10) / 10  # Cap at $10, normalize to 0-1
        velocity_score = min(velocity, 1) / 1  # Cap at 1x, normalize to 0-1
        burn_score = min(burn_rate, 50) / 50  # Cap at 50%, normalize to 0-1
        
        # Weighted composite (revenue most important, then velocity, then burn)
        sustainability = (revenue_score * 0.5) + (velocity_score * 0.3) + (burn_score * 0.2)
        return sustainability * 100  # Return as percentage
    except (TypeError, ValueError):
        return 0.0

def categorize_project_stage(market_cap: float, velocity: float, revenue_per_user: float) -> str:
    """
    Categorize projects by their development stage based on metrics
    """
    try:
        if market_cap < 10e6:  # Less than $10M
            return "Early Stage"
        elif market_cap < 100e6:  # $10M - $100M
            if velocity > 0.1 and revenue_per_user > 0.5:
                return "Growing"
            else:
                return "Developing"
        elif market_cap < 1e9:  # $100M - $1B
            if velocity > 0.05 and revenue_per_user > 1:
                return "Established"
            else:
                return "Mature"
        else:  # Over $1B
            if velocity > 0.02:
                return "Blue Chip"
            else:
                return "Legacy"
    except (TypeError, ValueError):
        return "Unknown"
