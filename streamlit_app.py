import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Optional

# Page configuration
st.set_page_config(
    page_title="Modulos Pricing Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .pricing-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .alert-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #51cf66;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Password protection
def check_password():
    """Returns True if the password is correct."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Modulos2025P!":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("Please enter the password to access the pricing calculator.")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Password incorrect. Please try again.")
        return False
    else:
        # Password correct.
        return True

# Pricing data structure based on Excel file
PRICING_TIERS = [
    {
        "name": "Mod Mini",
        "min_apps": 10,
        "max_apps": 49,
        "base_price": 20000,
        "price_per_app": 2000,
        "inflection_point": 42.5,
        "inflection_percentage": 0.85
    },
    {
        "name": "Mod 50",
        "min_apps": 50,
        "max_apps": 99,
        "base_price": 85000,
        "price_per_app": 1700,
        "inflection_point": 88.24,
        "inflection_percentage": 0.88
    },
    {
        "name": "Mod 100",
        "min_apps": 100,
        "max_apps": 199,
        "base_price": 150000,
        "price_per_app": 1500,
        "inflection_point": 146.67,
        "inflection_percentage": 0.73
    },
    {
        "name": "Mod 200",
        "min_apps": 200,
        "max_apps": 349,
        "base_price": 220000,
        "price_per_app": 1100,
        "inflection_point": 222.73,
        "inflection_percentage": 0.64
    },
    {
        "name": "Mod 350",
        "min_apps": 350,
        "max_apps": 999,
        "base_price": 245000,
        "price_per_app": 700,
        "inflection_point": 642.86,
        "inflection_percentage": 0.64
    },
    {
        "name": "Mod 1000+",
        "min_apps": 1000,
        "max_apps": float('inf'),
        "base_price": 450000,
        "price_per_app": 450,
        "inflection_point": None,
        "inflection_percentage": None
    }
]

def find_appropriate_tier(num_apps: int) -> Dict:
    """Find the appropriate pricing tier for given number of apps."""
    for tier in PRICING_TIERS:
        if tier["min_apps"] <= num_apps <= tier["max_apps"]:
            return tier
    return PRICING_TIERS[-1]  # Default to highest tier

def calculate_price(num_apps: int, tier: Dict) -> float:
    """Calculate price based on tier and number of apps."""
    if num_apps < tier["min_apps"]:
        return tier["base_price"]
    
    additional_apps = num_apps - tier["min_apps"]
    return tier["base_price"] + (additional_apps * tier["price_per_app"])

def find_optimal_recommendation(num_apps: int) -> Optional[Dict]:
    """Find if there's a better tier recommendation."""
    current_tier = find_appropriate_tier(num_apps)
    current_price = calculate_price(num_apps, current_tier)
    
    # Check if next tier would be more cost-effective
    current_index = PRICING_TIERS.index(current_tier)
    
    if current_index < len(PRICING_TIERS) - 1:
        next_tier = PRICING_TIERS[current_index + 1]
        next_tier_min_price = next_tier["base_price"]
        
        # Check if the inflection point suggests upgrading
        if (current_tier["inflection_point"] and 
            num_apps >= current_tier["inflection_point"]):
            return {
                "recommended_tier": next_tier,
                "current_price": current_price,
                "recommended_price": next_tier_min_price,
                "savings": current_price - next_tier_min_price,
                "reason": f"You're past the inflection point ({current_tier['inflection_point']:.0f} apps). Upgrading to {next_tier['name']} would be more cost-effective."
            }
    
    return None

def create_pricing_chart(num_apps: int):
    """Create an interactive pricing chart."""
    
    # Generate data points for visualization
    app_ranges = []
    prices = []
    tier_names = []
    colors = []
    
    color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for i, tier in enumerate(PRICING_TIERS):
        if tier["max_apps"] == float('inf'):
            max_range = 1500
        else:
            max_range = min(tier["max_apps"], 1500)
            
        tier_apps = list(range(tier["min_apps"], max_range + 1, 10))
        tier_prices = [calculate_price(apps, tier) for apps in tier_apps]
        
        app_ranges.extend(tier_apps)
        prices.extend(tier_prices)
        tier_names.extend([tier["name"]] * len(tier_apps))
        colors.extend([color_palette[i % len(color_palette)]] * len(tier_apps))
    
    df = pd.DataFrame({
        'Apps': app_ranges,
        'Price': prices,
        'Tier': tier_names,
        'Color': colors
    })
    
    fig = px.line(df, x='Apps', y='Price', color='Tier', 
                  title='Pricing Structure Across All Tiers',
                  labels={'Price': 'Price (USD)', 'Apps': 'Number of Apps'})
    
    # Add current selection point
    current_tier = find_appropriate_tier(num_apps)
    current_price = calculate_price(num_apps, current_tier)
    
    fig.add_scatter(x=[num_apps], y=[current_price], 
                   mode='markers', marker=dict(size=15, color='red'),
                   name='Your Selection')
    
    # Add inflection points
    for tier in PRICING_TIERS:
        if tier["inflection_point"] and tier["inflection_point"] <= 1500:
            inflection_price = calculate_price(int(tier["inflection_point"]), tier)
            fig.add_vline(x=tier["inflection_point"], line_dash="dash", 
                         line_color="orange", opacity=0.7,
                         annotation_text=f"{tier['name']} Inflection")
    
    fig.update_layout(
        height=500,
        showlegend=True,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig

def main():
    if not check_password():
        return
    
    # Header
    st.markdown('<h1 class="main-header">Modulos Pricing Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar for input
    with st.sidebar:
        st.header("📊 Configure Your Quote")
        
        num_apps = st.number_input(
            "Number of Apps",
            min_value=1,
            max_value=2000,
            value=100,
            step=1,
            help="Enter the number of apps you need to price"
        )
        
        st.markdown("---")
        
        # Show tier information
        st.subheader("🏷️ Available Tiers")
        for tier in PRICING_TIERS:
            max_display = "∞" if tier["max_apps"] == float('inf') else tier["max_apps"]
            st.write(f"**{tier['name']}**: {tier['min_apps']} - {max_display} apps")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Current pricing calculation
        current_tier = find_appropriate_tier(num_apps)
        current_price = calculate_price(num_apps, current_tier)
        
        st.markdown(f'<div class="pricing-card">', unsafe_allow_html=True)
        st.subheader(f"💰 Pricing for {num_apps} Apps")
        
        subcol1, subcol2, subcol3 = st.columns(3)
        
        with subcol1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Selected Tier", current_tier["name"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with subcol2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Total Price", f"${current_price:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with subcol3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            price_per_app_calc = current_price / num_apps
            st.metric("Price per App", f"${price_per_app_calc:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Optimization recommendation
        recommendation = find_optimal_recommendation(num_apps)
        
        if recommendation:
            st.markdown(f'<div class="alert-box">', unsafe_allow_html=True)
            st.subheader("⚠️ Optimization Alert!")
            st.write(recommendation["reason"])
            st.write(f"**Current Price**: ${recommendation['current_price']:,.0f}")
            st.write(f"**Recommended Tier**: {recommendation['recommended_tier']['name']} - ${recommendation['recommended_price']:,.0f}")
            st.write(f"**Potential Savings**: ${recommendation['savings']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
            st.subheader("✅ Optimal Pricing")
            st.write(f"You're getting the best value with the **{current_tier['name']}** tier!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Pricing breakdown
        st.subheader("📋 Pricing Breakdown")
        
        breakdown_data = {
            "Component": ["Base Price", "Additional Apps", "Price per Additional App", "Total"],
            "Value": [
                f"${current_tier['base_price']:,.0f}",
                max(0, num_apps - current_tier['min_apps']),
                f"${current_tier['price_per_app']:,.0f}",
                f"${current_price:,.0f}"
            ]
        }
        
        st.table(pd.DataFrame(breakdown_data))
    
    with col2:
        # Tier comparison table
        st.subheader("🔍 Tier Comparison")
        
        comparison_data = []
        for tier in PRICING_TIERS:
            price_for_tier = calculate_price(num_apps, tier)
            comparison_data.append({
                "Tier": tier["name"],
                "Range": f"{tier['min_apps']}-{tier['max_apps'] if tier['max_apps'] != float('inf') else '∞'}",
                "Price for Your Apps": f"${price_for_tier:,.0f}",
                "Selected": "✅" if tier == current_tier else ""
            })
        
        st.dataframe(
            pd.DataFrame(comparison_data),
            use_container_width=True,
            hide_index=True
        )
    
    # Interactive chart
    st.subheader("📈 Interactive Pricing Visualization")
    fig = create_pricing_chart(num_apps)
    st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "Modulos Pricing Calculator | Built with ❤️ using Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()