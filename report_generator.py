import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from io import StringIO

class ReportGenerator:
    """Generate comprehensive retail analytics reports"""
    
    def __init__(self):
        self.report_templates = {
            'executive_summary': self._executive_summary_template,
            'sales_performance': self._sales_performance_template,
            'customer_analysis': self._customer_analysis_template,
            'product_performance': self._product_performance_template,
            'operational_insights': self._operational_insights_template
        }
    
    def generate_comprehensive_report(self, data, analytics_results, customer_segments=None, predictions=None):
        """Generate a comprehensive retail analytics report"""
        if data.empty:
            return "No data available for report generation."
        
        report_sections = []
        
        # Header
        report_sections.append(self._generate_header())
        
        # Executive Summary
        report_sections.append(self._executive_summary_template(data, analytics_results))
        
        # Sales Performance Analysis
        report_sections.append(self._sales_performance_template(data, analytics_results))
        
        # Customer Analysis
        if customer_segments:
            report_sections.append(self._customer_analysis_template(data, customer_segments))
        
        # Product Performance
        report_sections.append(self._product_performance_template(data, analytics_results))
        
        # Operational Insights
        report_sections.append(self._operational_insights_template(data, analytics_results))
        
        # Predictive Insights
        if predictions:
            report_sections.append(self._predictive_insights_template(predictions))
        
        # Recommendations
        report_sections.append(self._generate_recommendations(data, analytics_results, customer_segments))
        
        # Footer
        report_sections.append(self._generate_footer())
        
        return "\n\n".join(report_sections)
    
    def _generate_header(self):
        """Generate report header"""
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"""
# 📊 RETAIL ANALYTICS COMPREHENSIVE REPORT
## Generated on {current_date}

---
        """
    
    def _executive_summary_template(self, data, analytics_results):
        """Generate executive summary section"""
        summary_stats = analytics_results.get('summary_stats', {})
        
        total_revenue = summary_stats.get('total_revenue', 0)
        total_transactions = summary_stats.get('total_transactions', 0)
        avg_transaction = summary_stats.get('average_transaction_value', 0)
        unique_customers = summary_stats.get('unique_customers', 0)
        unique_products = summary_stats.get('unique_products', 0)
        
        return f"""
## 🎯 EXECUTIVE SUMMARY

### Key Performance Indicators
- **Total Revenue**: ${total_revenue:,.2f}
- **Total Transactions**: {total_transactions:,}
- **Average Transaction Value**: ${avg_transaction:.2f}
- **Unique Customers**: {unique_customers:,}
- **Product Portfolio**: {unique_products} unique products
- **Revenue per Customer**: ${summary_stats.get('revenue_per_customer', 0):.2f}

### Business Health Overview
The retail operation shows {'strong' if total_revenue > 10000 else 'moderate' if total_revenue > 5000 else 'developing'} performance metrics with a diverse customer base and product portfolio.
        """
    
    def _sales_performance_template(self, data, analytics_results):
        """Generate sales performance section"""
        category_performance = analytics_results.get('category_performance', pd.DataFrame())
        store_performance = analytics_results.get('store_performance', pd.DataFrame())
        
        # Top performing category
        top_category = ""
        top_store = ""
        
        if not category_performance.empty:
            top_category = category_performance.iloc[0]['category']
            top_category_revenue = category_performance.iloc[0]['revenue']
        
        if not store_performance.empty:
            top_store = store_performance.iloc[0]['store_id']
            top_store_revenue = store_performance.iloc[0]['revenue']
        
        # Sales trend analysis
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        
        if len(data_copy) > 1:
            # Calculate growth trend
            data_sorted = data_copy.sort_values('timestamp')
            recent_sales = data_sorted.tail(len(data_sorted)//2)['total_amount'].sum()
            older_sales = data_sorted.head(len(data_sorted)//2)['total_amount'].sum()
            growth_rate = ((recent_sales - older_sales) / older_sales * 100) if older_sales > 0 else 0
        else:
            growth_rate = 0
        
        return f"""
## 📈 SALES PERFORMANCE ANALYSIS

### Category Performance
- **Top Performing Category**: {top_category}
- **Category Revenue**: ${top_category_revenue:,.2f} if 'top_category_revenue' in locals() else 'N/A'
- **Total Categories**: {len(category_performance)} active categories

### Store Performance  
- **Best Performing Store**: {top_store}
- **Store Revenue**: ${top_store_revenue:,.2f} if 'top_store_revenue' in locals() else 'N/A'
- **Total Active Stores**: {len(store_performance)}

### Growth Analysis
- **Recent Growth Trend**: {growth_rate:.1f}% {'📈 Positive' if growth_rate > 0 else '📉 Negative' if growth_rate < 0 else '➡️ Flat'}
- **Performance Status**: {'Expanding' if growth_rate > 5 else 'Stable' if growth_rate > -5 else 'Declining'}
        """
    
    def _customer_analysis_template(self, data, customer_segments):
        """Generate customer analysis section"""
        if not customer_segments or 'segment_stats' not in customer_segments:
            return """
## 👥 CUSTOMER ANALYSIS
Customer segmentation data not available.
            """
        
        segment_stats = customer_segments['segment_stats']
        
        # Find largest and most valuable segments
        largest_segment = max(segment_stats.items(), key=lambda x: x[1]['customer_count'])
        most_valuable_segment = max(segment_stats.items(), key=lambda x: x[1]['total_revenue'])
        
        return f"""
## 👥 CUSTOMER ANALYSIS

### Customer Segmentation Overview
- **Total Segments Identified**: {len(segment_stats)}
- **Largest Segment**: {largest_segment[0]} ({largest_segment[1]['customer_count']} customers)
- **Most Valuable Segment**: {most_valuable_segment[0]} (${most_valuable_segment[1]['total_revenue']:,.2f} revenue)

### Segment Performance Details
{self._format_segment_details(segment_stats)}

### Customer Insights
- **High-Value Customer Ratio**: {sum(1 for s in segment_stats.values() if s['avg_monetary'] > 100) / len(segment_stats) * 100:.1f}%
- **Customer Retention Opportunity**: Focus on segments with high recency scores
        """
    
    def _format_segment_details(self, segment_stats):
        """Format segment details for the report"""
        details = []
        for segment_name, stats in segment_stats.items():
            details.append(f"""
**{segment_name}**
- Customers: {stats['customer_count']}
- Avg. Purchase Frequency: {stats['avg_frequency']:.1f}
- Avg. Order Value: ${stats['avg_monetary']:.2f}
- Total Revenue: ${stats['total_revenue']:,.2f}
            """)
        return "\n".join(details)
    
    def _product_performance_template(self, data, analytics_results):
        """Generate product performance section"""
        product_performance = analytics_results.get('product_performance', pd.DataFrame())
        
        if product_performance.empty:
            return """
## 🛍️ PRODUCT PERFORMANCE ANALYSIS
Product performance data not available.
            """
        
        # Top products analysis
        top_products = product_performance.head(5)
        
        # Category diversity
        categories = product_performance['category'].nunique()
        
        return f"""
## 🛍️ PRODUCT PERFORMANCE ANALYSIS

### Top Performing Products
{self._format_top_products(top_products)}

### Product Portfolio Analysis
- **Total Products**: {len(product_performance)}
- **Active Categories**: {categories}
- **Product Diversity Score**: {categories / len(product_performance) * 100:.1f}%

### Performance Insights
- **Revenue Concentration**: Top 5 products account for {top_products['revenue'].sum() / product_performance['revenue'].sum() * 100:.1f}% of total revenue
- **Bestseller Categories**: {', '.join(top_products['category'].value_counts().head(3).index.tolist())}
        """
    
    def _format_top_products(self, top_products):
        """Format top products for the report"""
        if top_products.empty:
            return "No product data available."
        
        formatted = []
        for i, (_, product) in enumerate(top_products.iterrows(), 1):
            formatted.append(f"""
{i}. **{product['product_name']}** ({product['category']})
   - Revenue: ${product['revenue']:,.2f}
   - Units Sold: {product['quantity_sold']:,}
   - Avg. Transaction Value: ${product['avg_transaction']:.2f}
            """)
        return "\n".join(formatted)
    
    def _operational_insights_template(self, data, analytics_results):
        """Generate operational insights section"""
        trends = analytics_results.get('trends', {})
        
        # Calculate operational metrics
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        data_copy['hour'] = data_copy['timestamp'].dt.hour
        
        peak_hour = data_copy.groupby('hour')['total_amount'].sum().idxmax()
        peak_revenue = data_copy.groupby('hour')['total_amount'].sum().max()
        
        # Payment method analysis
        payment_methods = data_copy['payment_method'].value_counts()
        preferred_payment = payment_methods.index[0] if len(payment_methods) > 0 else "N/A"
        
        return f"""
## ⚙️ OPERATIONAL INSIGHTS

### Peak Performance Analysis
- **Peak Hour**: {peak_hour}:00 (${peak_revenue:,.2f} revenue)
- **Business Pattern**: {'Strong daytime performance' if 9 <= peak_hour <= 17 else 'Evening/night activity' if peak_hour >= 18 else 'Early morning activity'}

### Payment & Transaction Patterns
- **Preferred Payment Method**: {preferred_payment}
- **Payment Diversity**: {len(payment_methods)} different payment methods accepted
- **Average Transaction Processing**: {len(data_copy) / data_copy['timestamp'].dt.date.nunique():.1f} transactions per day

### Operational Efficiency
- **Store Utilization**: {analytics_results.get('summary_stats', {}).get('unique_stores', 0)} active locations
- **Product Turnover**: {analytics_results.get('summary_stats', {}).get('unique_products', 0)} products in rotation
- **Customer Engagement**: {analytics_results.get('summary_stats', {}).get('transactions_per_customer', 0):.1f} avg transactions per customer
        """
    
    def _predictive_insights_template(self, predictions):
        """Generate predictive insights section"""
        if not predictions:
            return """
## 🔮 PREDICTIVE INSIGHTS
Predictive analytics data not available.
            """
        
        sales_forecast = predictions.get('sales_forecast', {})
        demand_forecast = predictions.get('demand_forecast', {})
        
        return f"""
## 🔮 PREDICTIVE INSIGHTS

### Sales Forecasting
- **Forecast Accuracy**: {sales_forecast.get('model_score', 0) * 100:.1f}%
- **Predicted Revenue (7 days)**: ${sales_forecast.get('forecast_total', 0):,.2f}
- **Growth Trajectory**: {'Upward' if sales_forecast.get('forecast_total', 0) > 0 else 'Stable'}

### Demand Predictions
- **Products Analyzed**: {demand_forecast.get('total_products_analyzed', 0)}
- **Increasing Demand**: {demand_forecast.get('products_increasing', 0)} products
- **Declining Demand**: {demand_forecast.get('products_decreasing', 0)} products

### Strategic Implications
- **Inventory Planning**: Adjust stock levels based on demand forecasts
- **Resource Allocation**: Focus on high-growth product categories
- **Market Opportunities**: {'Expansion potential identified' if sales_forecast.get('forecast_total', 0) > 10000 else 'Maintain current operations'}
        """
    
    def _generate_recommendations(self, data, analytics_results, customer_segments=None):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Revenue recommendations
        summary_stats = analytics_results.get('summary_stats', {})
        avg_transaction = summary_stats.get('average_transaction_value', 0)
        
        if avg_transaction < 50:
            recommendations.append("💰 **Increase Average Transaction Value**: Implement upselling strategies and product bundling")
        
        # Customer recommendations
        if customer_segments and 'segment_stats' in customer_segments:
            segment_stats = customer_segments['segment_stats']
            high_risk_segments = [name for name, stats in segment_stats.items() 
                                if stats.get('avg_recency', 0) > 30]
            
            if high_risk_segments:
                recommendations.append(f"🎯 **Customer Retention**: Focus on re-engaging {', '.join(high_risk_segments)} segments")
        
        # Product recommendations
        category_performance = analytics_results.get('category_performance', pd.DataFrame())
        if not category_performance.empty:
            top_category = category_performance.iloc[0]['category']
            recommendations.append(f"📦 **Inventory Focus**: Expand {top_category} category based on strong performance")
        
        # Operational recommendations
        trends = analytics_results.get('trends', {})
        peak_hour = trends.get('peak_hour')
        if peak_hour:
            recommendations.append(f"⏰ **Staffing Optimization**: Ensure adequate staffing during peak hour ({peak_hour}:00)")
        
        # General recommendations
        recommendations.extend([
            "📊 **Data-Driven Decisions**: Continue monitoring KPIs and adjust strategies based on performance",
            "🔄 **Regular Reviews**: Schedule monthly analytics reviews to track progress",
            "🎨 **Customer Experience**: Focus on improving customer satisfaction scores",
            "🚀 **Innovation**: Consider new product lines based on customer feedback and trends"
        ])
        
        return f"""
## 💡 STRATEGIC RECOMMENDATIONS

### Priority Actions
{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations[:5])])}

### Long-term Initiatives
{chr(10).join([f"• {rec}" for rec in recommendations[5:]])}

### Success Metrics to Track
- Monthly revenue growth rate
- Customer acquisition and retention rates
- Average transaction value trends
- Product performance rankings
- Customer satisfaction scores
        """
    
    def _generate_footer(self):
        """Generate report footer"""
        return f"""
---

## 📋 REPORT SUMMARY

This comprehensive retail analytics report provides insights into sales performance, customer behavior, product analytics, and operational efficiency. The recommendations are based on data-driven analysis and should be reviewed regularly to ensure continued business growth.

**Report Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Data Analysis Period**: Based on available transaction data
**Next Review Date**: {(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}

---
        """
    
    def export_to_csv(self, data, filename=None):
        """Export data to CSV format"""
        if filename is None:
            filename = f"retail_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Convert to CSV string
        output = StringIO()
        data.to_csv(output, index=False)
        csv_content = output.getvalue()
        output.close()
        
        return csv_content, filename
    
    def generate_kpi_dashboard_data(self, data, analytics_results):
        """Generate KPI data for dashboard display"""
        if data.empty:
            return {}
        
        summary_stats = analytics_results.get('summary_stats', {})
        trends = analytics_results.get('trends', {})
        
        # Calculate additional KPIs
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        
        # Recent performance (last 24 hours)
        recent_cutoff = data_copy['timestamp'].max() - timedelta(hours=24)
        recent_data = data_copy[data_copy['timestamp'] >= recent_cutoff]
        
        kpis = {
            # Core metrics
            'total_revenue': summary_stats.get('total_revenue', 0),
            'total_transactions': summary_stats.get('total_transactions', 0),
            'avg_transaction_value': summary_stats.get('average_transaction_value', 0),
            'unique_customers': summary_stats.get('unique_customers', 0),
            
            # Growth metrics
            'revenue_growth': trends.get('revenue_growth_percent', 0),
            'transaction_growth': trends.get('transaction_growth_percent', 0),
            
            # Recent performance
            'recent_revenue_24h': recent_data['total_amount'].sum(),
            'recent_transactions_24h': len(recent_data),
            'recent_customers_24h': recent_data['customer_id'].nunique(),
            
            # Performance indicators
            'revenue_per_customer': summary_stats.get('revenue_per_customer', 0),
            'transactions_per_customer': summary_stats.get('transactions_per_customer', 0),
            'peak_hour': trends.get('peak_hour', 'N/A'),
            
            # Category insights
            'total_categories': len(analytics_results.get('category_performance', pd.DataFrame())),
            'total_stores': summary_stats.get('unique_stores', 0),
            'total_products': summary_stats.get('unique_products', 0)
        }
        
        return kpis