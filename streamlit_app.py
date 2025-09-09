import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

# Try importing plotly, fall back if not available
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Password protection - matching your exact style
def check_password():
    def password_entered():
        if st.session_state["password"] == "Modulos2025P!":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 2rem 0;">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem;">Modulos AI GRC</h1>
            <h3 style="color: white; opacity: 0.9; font-weight: 300;">Premium Pricing Calculator</h3>
        </div>
        """, unsafe_allow_html=True)
        st.text_input("Enter Password", type="password", on_change=password_entered, key="password", 
                     placeholder="Enter your access credentials")
        st.markdown("*Please enter password to access the Modulos AI GRC pricing calculator*")
        st.info("Contact your Modulos AI representative for access credentials")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 2rem 0;">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem;">Modulos AI GRC</h1>
            <h3 style="color: white; opacity: 0.9; font-weight: 300;">Premium Pricing Calculator</h3>
        </div>
        """, unsafe_allow_html=True)
        st.text_input("Enter Password", type="password", on_change=password_entered, key="password",
                     placeholder="Enter your access credentials")
        st.error("Password incorrect. Please try again.")
        st.info("Contact your Modulos AI representative for access credentials")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Modulos AI GRC - Pricing Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Exact CSS styling from your file
st.markdown("""
<style>
    .main { font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem; border-radius: 20px; margin-bottom: 3rem;
        text-align: center; box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 { color: white; margin-bottom: 0.5rem; font-weight: 700; font-size: 3.5rem; }
    .main-header p { color: white; opacity: 0.95; font-size: 1.4rem; font-weight: 300; }
    .premium-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafe 100%);
        padding: 2rem; border-radius: 16px; border: 1px solid #e1e8f7;
        margin: 1.5rem 0; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    .highlight-card { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; }
    .metric-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        border-left: 4px solid #667eea; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .simple-breakdown {
        background: #f8fafe; padding: 2rem; border-radius: 12px;
        border: 1px solid #e1e8f7; margin: 1rem 0;
    }
    .simple-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.75rem 0; border-bottom: 1px solid #e1e8f7;
    }
    .simple-final {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1rem; font-weight: 600; background: #667eea; color: white;
        margin: 0.5rem -2rem -2rem -2rem; border-radius: 0 0 12px 12px;
    }
    .discount-badge {
        background: linear-gradient(135deg, #e74c3c, #c0392b); color: white;
        padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
    }
    .savings-badge {
        background: linear-gradient(135deg, #27ae60, #229954); color: white;
        padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
    }
    .cap-badge {
        background: linear-gradient(135deg, #f39c12, #e67e22); color: white;
        padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
    }
    .stats-container {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem; margin: 2rem 0;
    }
    .stat-box {
        background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e1e8f7;
        text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .stat-value { font-size: 2rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem; }
    .stat-label { font-size: 0.9rem; color: #666; font-weight: 500; }
    .section-header {
        font-size: 2rem; color: #2c3e50; margin-bottom: 2rem;
        font-weight: 600; text-align: center;
    }
    .optimization-alert {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem; border-radius: 12px; border-left: 4px solid #e74c3c;
        margin: 1.5rem 0; box-shadow: 0 4px 20px rgba(231, 76, 60, 0.1);
    }
    .optimal-badge {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem; border-radius: 12px; border-left: 4px solid #27ae60;
        margin: 1.5rem 0; box-shadow: 0 4px 20px rgba(39, 174, 96, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header - matching your exact branding
st.markdown("""
<div class="main-header">
    <h1>Modulos AI GRC</h1>
    <p>Professional AI Governance Pricing Calculator</p>
</div>
""", unsafe_allow_html=True)

# Pricing data structure based on your Excel file
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
    """Create an interactive pricing chart matching your style."""
    
    # Generate data points for visualization
    app_ranges = []
    prices = []
    tier_names = []
    colors = []
    
    # Using your color palette
    color_palette = ['#667eea', '#764ba2', '#e74c3c', '#27ae60', '#f39c12', '#8b5cf6']
    
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
    
    fig = go.Figure()
    
    # Add lines for each tier
    for i, tier in enumerate(PRICING_TIERS):
        if tier["max_apps"] == float('inf'):
            max_range = 1500
        else:
            max_range = min(tier["max_apps"], 1500)
        
        tier_apps = list(range(tier["min_apps"], max_range + 1, 10))
        tier_prices = [calculate_price(apps, tier) for apps in tier_apps]
        
        fig.add_trace(go.Scatter(
            x=tier_apps,
            y=tier_prices,
            mode='lines+markers',
            name=tier["name"],
            line=dict(color=color_palette[i % len(color_palette)], width=3),
            marker=dict(size=6),
            hovertemplate=f'<b>{tier["name"]}</b><br>' +
                         'Apps: %{x}<br>' +
                         'Price: €%{y:,.0f}<extra></extra>'
        ))
    
    # Add current selection point
    current_tier = find_appropriate_tier(num_apps)
    current_price = calculate_price(num_apps, current_tier)
    
    fig.add_scatter(
        x=[num_apps], 
        y=[current_price], 
        mode='markers', 
        marker=dict(size=20, color='#e74c3c', symbol='diamond'),
        name='Your Selection',
        hovertemplate=f'<b>Your Configuration</b><br>' +
                     f'Apps: {num_apps}<br>' +
                     f'Price: €{current_price:,.0f}<br>' +
                     f'Tier: {current_tier["name"]}<extra></extra>'
    )
    
    # Add inflection points
    for tier in PRICING_TIERS:
        if tier["inflection_point"] and tier["inflection_point"] <= 1500:
            inflection_price = calculate_price(int(tier["inflection_point"]), tier)
            fig.add_vline(
                x=tier["inflection_point"], 
                line_dash="dash", 
                line_color="orange", 
                opacity=0.7,
                annotation_text=f"{tier['name']} Optimization Point"
            )
    
    fig.update_layout(
        title={
            'text': '<b>Modulos AI GRC Pricing Structure</b><br><sub>Interactive Pricing Across All Tiers</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Inter', 'size': 20}
        },
        xaxis_title='Number of AI Systems',
        yaxis_title='Investment (EUR)',
        height=600,
        showlegend=True,
        template="plotly_white",
        hovermode='closest',
        plot_bgcolor='rgba(248, 250, 254, 0.8)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=12, family='Inter', color='#475569'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(148, 163, 184, 0.2)',
            borderwidth=1
        )
    )
    
    return fig

def main():
    st.markdown('<h2 class="section-header">AI System Portfolio Pricing</h2>', unsafe_allow_html=True)
    
    # Configuration section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: #667eea; margin-bottom: 1rem;">Portfolio Configuration</h4>
        </div>
        """, unsafe_allow_html=True)
        
        num_apps = st.number_input(
            "Number of AI Systems",
            min_value=1,
            max_value=2000,
            value=100,
            step=1,
            help="Enter the total number of AI systems in your portfolio"
        )
        
        # Risk Quantification Toggle
        st.markdown("### Risk Quantification")
        risk_quantification = st.checkbox(
            "Enable Risk Quantification (+30%)",
            value=False,
            help="Enable advanced risk quantification features. This increases pricing by 30% but provides enhanced risk assessment and compliance capabilities."
        )
        
        if risk_quantification:
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <p style="margin: 0; font-size: 0.9rem; color: #856404;"><strong>Risk Quantification Enabled</strong><br>
                Advanced risk assessment and compliance features included (+30% premium)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8fafe; padding: 1.5rem; border-radius: 12px; border: 1px solid #e1e8f7; margin-top: 1rem;">
            <h5 style="color: #2c3e50; margin-bottom: 1rem;">Available Tiers</h5>
        """, unsafe_allow_html=True)
        
        for tier in PRICING_TIERS:
            max_display = "∞" if tier["max_apps"] == float('inf') else tier["max_apps"]
            st.markdown(f"• **{tier['name']}**: {tier['min_apps']} - {max_display} AI systems")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Current pricing calculation
        current_tier = find_appropriate_tier(num_apps)
        price_result = calculate_price(num_apps, current_tier, risk_quantification)
        current_price = price_result['total_price']
        
        st.markdown(f"""
        <div class="premium-card highlight-card">
            <h3>Investment Analysis for {num_apps} AI Systems</h3>
            <h2 style="font-size: 2.5rem; margin: 1rem 0;">€{current_price:,.0f}</h2>
            <p style="font-size: 1.2rem;">Selected Tier: {current_tier["name"]}</p>
            {'<p style="font-size: 1rem; opacity: 0.9;">Risk Quantification: Enabled (+30%)</p>' if risk_quantification else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        price_per_app_calc = current_price / num_apps
        base_price_per_app = price_result['subtotal'] / num_apps
        
        if risk_quantification:
            st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-value">€{price_per_app_calc:.0f}</div>
                    <div class="stat-label">Total Cost per AI System</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">€{base_price_per_app:.0f}</div>
                    <div class="stat-label">Base Cost per AI System</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">€{price_result['risk_premium']:,.0f}</div>
                    <div class="stat-label">Risk Premium Total</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{current_tier["min_apps"]}-{current_tier["max_apps"] if current_tier["max_apps"] != float('inf') else '∞'}</div>
                    <div class="stat-label">Tier Range</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-value">€{price_per_app_calc:.0f}</div>
                    <div class="stat-label">Cost per AI System</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{current_tier["min_apps"]}-{current_tier["max_apps"] if current_tier["max_apps"] != float('inf') else '∞'}</div>
                    <div class="stat-label">Tier Range</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Optimization recommendation
    recommendation = find_optimal_recommendation(num_apps, risk_quantification)
    
    if recommendation:
        st.markdown(f"""
        <div class="optimization-alert">
            <h4 style="color: #c0392b; margin-bottom: 1rem;">Optimization Opportunity Detected</h4>
            <p><strong>{recommendation["reason"]}</strong></p>
            <div style="margin-top: 1rem;">
                <p>• Current Configuration: €{recommendation['current_price']:,.0f}</p>
                <p>• Recommended Tier: {recommendation['recommended_tier']['name']} - €{recommendation['recommended_price']:,.0f}</p>
                <p style="color: #c0392b; font-weight: 600;">• Potential Savings: €{recommendation['savings']:,.0f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="optimal-badge">
            <h4 style="color: #229954; margin-bottom: 1rem;">Optimal Configuration</h4>
            <p>You're getting the best value with the <strong>{current_tier['name']}</strong> tier for {num_apps} AI systems!</p>
            <p>This configuration provides optimal cost efficiency for your portfolio size.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Pricing breakdown
    st.markdown('<h3 class="section-header">Investment Breakdown</h3>', unsafe_allow_html=True)
    
    additional_apps = max(0, num_apps - current_tier['min_apps'])
    
    if risk_quantification:
        st.markdown(f"""
        <div class="simple-breakdown">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">Pricing Components</h4>
            <div class="simple-item">
                <span>Base Tier Price ({current_tier['name']})</span>
                <strong>€{current_tier['base_price']:,.0f}</strong>
            </div>
            <div class="simple-item">
                <span>Additional AI Systems ({additional_apps} × €{current_tier['price_per_app']:,.0f})</span>
                <strong>€{price_result['additional_cost']:,.0f}</strong>
            </div>
            <div class="simple-item">
                <span>Subtotal (Base + Additional)</span>
                <strong>€{price_result['subtotal']:,.0f}</strong>
            </div>
            <div class="simple-item">
                <span>Risk Quantification Premium (+30%)</span>
                <strong>€{price_result['risk_premium']:,.0f}</strong>
            </div>
            <div class="simple-final">
                <span>Total Investment</span>
                <strong>€{current_price:,.0f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="simple-breakdown">
            <h4 style="margin-bottom: 1rem; color: #2c3e50;">Pricing Components</h4>
            <div class="simple-item">
                <span>Base Tier Price ({current_tier['name']})</span>
                <strong>€{current_tier['base_price']:,.0f}</strong>
            </div>
            <div class="simple-item">
                <span>Additional AI Systems ({additional_apps} × €{current_tier['price_per_app']:,.0f})</span>
                <strong>€{price_result['additional_cost']:,.0f}</strong>
            </div>
            <div class="simple-final">
                <span>Total Investment</span>
                <strong>€{current_price:,.0f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk Quantification Information Panel
    if risk_quantification:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: #667eea; margin-bottom: 1rem;">Risk Quantification Features Included</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <h5 style="color: #2c3e50; margin-bottom: 0.5rem;">Enhanced Risk Assessment</h5>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #666;">
                        <li>Advanced risk scoring algorithms</li>
                        <li>Automated compliance monitoring</li>
                        <li>Real-time risk alerting system</li>
                    </ul>
                </div>
                <div>
                    <h5 style="color: #2c3e50; margin-bottom: 0.5rem;">Quantitative Analysis</h5>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #666;">
                        <li>Statistical risk modeling</li>
                        <li>Predictive risk analytics</li>
                        <li>Custom risk reporting</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tier comparison table
    st.markdown('<h3 class="section-header">Tier Comparison Analysis</h3>', unsafe_allow_html=True)
    
    comparison_data = []
    for tier in PRICING_TIERS:
        price_result_tier = calculate_price(num_apps, tier, risk_quantification)
        price_for_tier = price_result_tier['total_price']
        is_selected = tier == current_tier
        
        comparison_data.append({
            "Tier": tier["name"],
            "Range": f"{tier['min_apps']}-{tier['max_apps'] if tier['max_apps'] != float('inf') else '∞'}",
            "Base Price": f"€{tier['base_price']:,.0f}",
            "Per Additional": f"€{tier['price_per_app']:,.0f}",
            "Your Price": f"€{price_for_tier:,.0f}" + (" (+30% Risk)" if risk_quantification else ""),
            "Selected": "✅" if is_selected else ""
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #667eea; margin-bottom: 1rem;">Complete Tier Analysis</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Interactive visualization
    if PLOTLY_AVAILABLE:
        st.markdown('<h3 class="section-header">Interactive Pricing Visualization</h3>', unsafe_allow_html=True)
        fig = create_pricing_chart(num_apps, risk_quantification)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Enhanced visualizations require Plotly. Install plotly for interactive charts.")
    
    # Footer - matching your exact styling
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafe 0%, #e8ecff 100%); border-radius: 15px; margin-top: 2rem;">
        <h4 style="color: #667eea; margin-bottom: 1rem;">Modulos AI GRC</h4>
        <p style="color: #666; margin-bottom: 0.5rem;">Professional AI Governance Solutions</p>
        <p style="color: #888; font-size: 0.9rem;">Secure, Password-Protected Pricing Calculator</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
