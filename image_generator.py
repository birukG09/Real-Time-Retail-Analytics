import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns
import plotly.graph_objects as go
import io
import base64

class ImageGenerator:
    """Generate demo images and graphics for the retail dashboard"""
    
    def __init__(self):
        # Set style for better looking plots
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_product_category_images(self):
        """Create representative images for different product categories"""
        category_images = {}
        
        # Electronics - Circuit pattern
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1e1e2e')
        ax.set_facecolor('#1e1e2e')
        
        # Create circuit-like pattern
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
        y2 = np.cos(x * 1.5) + np.random.normal(0, 0.1, 100)
        
        ax.plot(x, y1, color='#00ff88', linewidth=2, alpha=0.8)
        ax.plot(x, y2, color='#0088ff', linewidth=2, alpha=0.8)
        ax.scatter(x[::10], y1[::10], color='#ff6b35', s=30, alpha=0.9)
        
        ax.set_title('Electronics', color='white', fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#1e1e2e', dpi=100)
        buffer.seek(0)
        category_images['Electronics'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Clothing - Fashion pattern
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#f8f9fa')
        colors = ['#ff6b9d', '#c44569', '#f8b500', '#feca57']
        
        # Create fashion-inspired pattern
        angles = np.linspace(0, 2*np.pi, 8)
        for i, angle in enumerate(angles):
            x = np.cos(angle) * (i + 1) * 0.3
            y = np.sin(angle) * (i + 1) * 0.3
            circle = plt.Circle((x, y), 0.2, color=colors[i % len(colors)], alpha=0.7)
            ax.add_patch(circle)
        
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_title('Clothing', fontsize=16, fontweight='bold', color='#2c3e50')
        ax.axis('off')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#f8f9fa', dpi=100)
        buffer.seek(0)
        category_images['Clothing'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Food & Beverages - Organic pattern
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#2d5a27')
        
        # Create organic food pattern
        theta = np.linspace(0, 4*np.pi, 200)
        r = 1 + 0.3 * np.sin(5*theta) + 0.1 * np.random.normal(0, 1, 200)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        scatter = ax.scatter(x, y, c=theta, cmap='Greens', alpha=0.8, s=20)
        ax.set_title('Food & Beverages', color='white', fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#2d5a27', dpi=100)
        buffer.seek(0)
        category_images['Food & Beverages'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return category_images
    
    def create_dashboard_hero_image(self):
        """Create an attractive hero image for the dashboard"""
        fig = plt.figure(figsize=(12, 6), facecolor='#667eea')
        
        # Create a gradient-like effect with data visualization elements
        gs = fig.add_gridspec(2, 3, hspace=0.1, wspace=0.1)
        
        # Main chart area
        ax1 = fig.add_subplot(gs[:, :2])
        ax1.set_facecolor('none')
        
        # Create sample sales data visualization
        days = np.arange(30)
        sales = 1000 + np.cumsum(np.random.normal(50, 100, 30))
        sales = np.maximum(sales, 500)  # Ensure positive values
        
        # Main trend line
        ax1.plot(days, sales, linewidth=4, color='white', alpha=0.9)
        ax1.fill_between(days, sales, alpha=0.3, color='white')
        
        # Add some data points
        highlight_days = [5, 10, 15, 20, 25]
        ax1.scatter([days[i] for i in highlight_days], 
                   [sales[i] for i in highlight_days], 
                   s=100, color='#ffd700', zorder=5, edgecolors='white', linewidth=2)
        
        ax1.set_title('Real-Time Sales Analytics', color='white', fontsize=20, fontweight='bold', pad=20)
        ax1.set_xlabel('Days', color='white', fontsize=12)
        ax1.set_ylabel('Revenue ($)', color='white', fontsize=12)
        ax1.grid(True, alpha=0.3, color='white')
        ax1.tick_params(colors='white')
        
        # Side metrics
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.set_facecolor('#f0f8ff')
        
        # Create a mini donut chart
        sizes = [30, 25, 20, 15, 10]
        colors = ['#ff6b9d', '#feca57', '#ff6b35', '#0abde3', '#10ac84']
        
        wedges, texts = ax2.pie(sizes, colors=colors, startangle=90)
        # Create donut by adding white circle
        centre_circle = plt.Circle((0,0), 0.6, fc='white', alpha=0.8)
        ax2.add_artist(centre_circle)
        ax2.set_title('Categories', color='white', fontweight='bold')
        
        # Bottom metrics
        ax3 = fig.add_subplot(gs[1, 2])
        ax3.set_facecolor('#f0f8ff')
        
        # Create bar chart
        categories = ['Q1', 'Q2', 'Q3', 'Q4']
        values = [23, 34, 31, 20]
        bars = ax3.bar(categories, values, color=['#ff6b9d', '#feca57', '#ff6b35', '#0abde3'])
        
        ax3.set_title('Quarterly Growth', color='white', fontweight='bold')
        ax3.tick_params(colors='white')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#667eea', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        hero_image = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return hero_image
    
    def create_feature_icons(self):
        """Create icons for different features"""
        icons = {}
        
        # Analytics icon
        fig, ax = plt.subplots(figsize=(2, 2), facecolor='#f8f9fa')
        
        # Create bar chart icon
        bars_x = [0.2, 0.4, 0.6, 0.8]
        bars_y = [0.3, 0.7, 0.5, 0.9]
        colors = ['#667eea', '#764ba2', '#667eea', '#764ba2']
        
        bars = ax.bar(bars_x, bars_y, width=0.15, color=colors)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#f8f9fa', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        icons['analytics'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Customer icon
        fig, ax = plt.subplots(figsize=(2, 2), facecolor='#f8f9fa')
        
        # Create people/customer representation
        circle1 = plt.Circle((0.3, 0.7), 0.1, color='#ff6b9d', alpha=0.8)
        circle2 = plt.Circle((0.5, 0.7), 0.1, color='#feca57', alpha=0.8)
        circle3 = plt.Circle((0.7, 0.7), 0.1, color='#0abde3', alpha=0.8)
        
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        
        # Add bodies
        rect1 = plt.Rectangle((0.25, 0.4), 0.1, 0.2, color='#ff6b9d', alpha=0.6)
        rect2 = plt.Rectangle((0.45, 0.4), 0.1, 0.2, color='#feca57', alpha=0.6)
        rect3 = plt.Rectangle((0.65, 0.4), 0.1, 0.2, color='#0abde3', alpha=0.6)
        
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.add_patch(rect3)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#f8f9fa', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        icons['customers'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Prediction icon
        fig, ax = plt.subplots(figsize=(2, 2), facecolor='#f8f9fa')
        
        # Create crystal ball/prediction icon
        x = np.linspace(0, 2*np.pi, 100)
        y1 = 0.5 + 0.3 * np.sin(x)
        y2 = 0.5 + 0.2 * np.cos(2*x)
        
        ax.plot(x, y1, color='#9b59b6', linewidth=3, alpha=0.8)
        ax.plot(x, y2, color='#e74c3c', linewidth=2, alpha=0.6)
        
        # Add prediction arrow
        arrow = plt.Arrow(4, 0.5, 1, 0.2, width=0.3, color='#f39c12', alpha=0.8)
        ax.add_patch(arrow)
        
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#f8f9fa', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        icons['predictions'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return icons
    
    def create_kpi_background_images(self):
        """Create background patterns for KPI cards"""
        backgrounds = {}
        
        # Revenue background
        fig, ax = plt.subplots(figsize=(3, 2), facecolor='#2ecc71')
        
        # Create money/growth pattern
        x = np.linspace(0, 4*np.pi, 200)
        y = np.exp(x/8) * np.sin(x) * 0.1
        ax.plot(x, y, color='white', alpha=0.3, linewidth=2)
        
        # Add dollar signs pattern
        for i in range(5):
            ax.text(i*np.pi, 0.05, '$', fontsize=20, color='white', alpha=0.2, ha='center')
        
        ax.set_xlim(0, 4*np.pi)
        ax.set_ylim(-0.1, 0.1)
        ax.axis('off')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#2ecc71', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        backgrounds['revenue'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Transactions background
        fig, ax = plt.subplots(figsize=(3, 2), facecolor='#3498db')
        
        # Create transaction flow pattern
        for i in range(10):
            x_pos = i * 0.4
            y_pos = 0.5 + 0.3 * np.sin(i)
            circle = plt.Circle((x_pos, y_pos), 0.1, color='white', alpha=0.2)
            ax.add_patch(circle)
            if i < 9:
                ax.arrow(x_pos + 0.1, y_pos, 0.2, 0, head_width=0.05, head_length=0.05, 
                        fc='white', ec='white', alpha=0.3)
        
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', facecolor='#3498db', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        backgrounds['transactions'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return backgrounds