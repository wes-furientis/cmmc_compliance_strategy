#!/usr/bin/env python3
"""
Generate cost breakdown pie charts for CMMC Compliance Strategy document.
Creates both initial implementation and annual operational cost charts.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Define color palette - professional blues and grays
colors = [
    '#1a365d',  # Dark navy
    '#2b6cb0',  # Medium blue
    '#3182ce',  # Bright blue
    '#4a90d9',  # Light blue
    '#63a4e8',  # Lighter blue
    '#7cb8f7',  # Very light blue
    '#4a5568',  # Gray
]

# Initial Implementation Costs (midpoint values from document)
initial_costs = {
    'Cloud Setup\n(AWS GovCloud)': 27500,
    'M365 GCC High\nSetup': 17500,
    'Security\nTooling': 75000,
    'Hardware\n(Endpoints)': 57500,
    'Network\nEquipment': 27500,
    'Consulting\nServices': 95000,
    'C3PAO\nAssessment': 45000,
}

# Annual Operational Costs (midpoint values from document)
annual_costs = {
    'AWS GovCloud\nConsumption': 270000,
    'M365 GCC High\nLicensing': 26000,
    'Security Tooling\nRenewals': 45000,
    'Personnel\n(Security/Compliance)': 200000,
    'Training': 17500,
}

def create_pie_chart(costs, title, filename, total_label):
    """Create a single pie chart with the given costs."""

    labels = list(costs.keys())
    values = list(costs.values())
    total = sum(values)

    # Calculate percentages for labels
    percentages = [(v / total) * 100 for v in values]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color='#ffffff', width=2)
        ),
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(size=11, color='#1a365d'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        pull=[0.02] * len(labels),  # Slight separation for all slices
    )])

    fig.update_layout(
        title=dict(
            text=f'<b>{title}</b>',
            font=dict(size=18, color='#1a365d', family='Arial, sans-serif'),
            x=0.5,
            y=0.95,
        ),
        annotations=[
            dict(
                text=f'<b>{total_label}</b><br>${total:,.0f}',
                x=0.5, y=0.5,
                font=dict(size=14, color='#1a365d', family='Arial, sans-serif'),
                showarrow=False
            )
        ],
        showlegend=False,
        width=800,
        height=600,
        margin=dict(t=80, b=40, l=100, r=100),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    # Save as PNG
    output_path = os.path.join(os.path.dirname(__file__), filename)
    fig.write_image(output_path, scale=2)
    print(f"Created: {output_path}")

    return fig

def create_combined_chart():
    """Create a combined chart with both pie charts side by side."""

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'pie'}, {'type': 'pie'}]],
        subplot_titles=[
            '<b>Initial Implementation Costs</b>',
            '<b>Annual Operational Costs</b>'
        ]
    )

    # Initial costs pie
    initial_labels = list(initial_costs.keys())
    initial_values = list(initial_costs.values())
    initial_total = sum(initial_values)

    fig.add_trace(go.Pie(
        labels=initial_labels,
        values=initial_values,
        hole=0.4,
        marker=dict(
            colors=colors[:len(initial_labels)],
            line=dict(color='#ffffff', width=2)
        ),
        textposition='outside',
        textinfo='percent',
        textfont=dict(size=10, color='#1a365d'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        domain=dict(x=[0, 0.45]),
    ), row=1, col=1)

    # Annual costs pie
    annual_labels = list(annual_costs.keys())
    annual_values = list(annual_costs.values())
    annual_total = sum(annual_values)

    fig.add_trace(go.Pie(
        labels=annual_labels,
        values=annual_values,
        hole=0.4,
        marker=dict(
            colors=colors[:len(annual_labels)],
            line=dict(color='#ffffff', width=2)
        ),
        textposition='outside',
        textinfo='percent',
        textfont=dict(size=10, color='#1a365d'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        domain=dict(x=[0.55, 1]),
    ), row=1, col=2)

    fig.update_layout(
        title=dict(
            text='<b>CMMC Level 2 Compliance Cost Breakdown</b>',
            font=dict(size=20, color='#1a365d', family='Arial, sans-serif'),
            x=0.5,
            y=0.98,
        ),
        annotations=[
            # Initial costs center annotation
            dict(
                text=f'<b>Total</b><br>${initial_total:,.0f}',
                x=0.18, y=0.5,
                font=dict(size=12, color='#1a365d', family='Arial, sans-serif'),
                showarrow=False
            ),
            # Annual costs center annotation
            dict(
                text=f'<b>Total</b><br>${annual_total:,.0f}',
                x=0.82, y=0.5,
                font=dict(size=12, color='#1a365d', family='Arial, sans-serif'),
                showarrow=False
            ),
            # Subtitle annotations (replacing subplot_titles for better control)
            dict(
                text='<b>Initial Implementation</b><br>(One-Time)',
                x=0.18, y=1.08,
                font=dict(size=14, color='#1a365d', family='Arial, sans-serif'),
                showarrow=False,
                xref='paper',
                yref='paper'
            ),
            dict(
                text='<b>Annual Operations</b><br>(Recurring)',
                x=0.82, y=1.08,
                font=dict(size=14, color='#1a365d', family='Arial, sans-serif'),
                showarrow=False,
                xref='paper',
                yref='paper'
            ),
        ],
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=10, color='#1a365d'),
        ),
        width=1200,
        height=700,
        margin=dict(t=120, b=100, l=80, r=80),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    # Remove default subplot titles
    fig.layout.annotations = [a for a in fig.layout.annotations if 'Initial' not in str(a.text) and 'Annual' not in str(a.text) or '$' in str(a.text)]

    # Save as PNG
    output_path = os.path.join(os.path.dirname(__file__), 'cost_breakdown_combined.png')
    fig.write_image(output_path, scale=2)
    print(f"Created: {output_path}")

    return fig

if __name__ == '__main__':
    print("Generating CMMC Compliance Cost Charts...")
    print("-" * 50)

    # Create individual charts
    create_pie_chart(
        initial_costs,
        'Initial Implementation Costs',
        'cost_initial_implementation.png',
        'Total'
    )

    create_pie_chart(
        annual_costs,
        'Annual Operational Costs',
        'cost_annual_operations.png',
        'Annual'
    )

    # Create combined chart
    create_combined_chart()

    print("-" * 50)
    print("All charts generated successfully!")
