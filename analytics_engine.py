import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AnalyticsEngine:
    """Engine for calculating retail analytics metrics"""
    
    def __init__(self):
        pass
    
    def calculate_metrics(self, data):
        """Calculate comprehensive retail metrics"""
        if data.empty:
            return self._empty_metrics()
        
        return {
            'summary_stats': self._calculate_summary_stats(data),
            'time_series': self._calculate_time_series(data),
            'category_performance': self._calculate_category_performance(data),
            'store_performance': self._calculate_store_performance(data),
            'product_performance': self._calculate_product_performance(data),
            'customer_insights': self._calculate_customer_insights(data),
            'trends': self._calculate_trends(data)
        }
    
    def _empty_metrics(self):
        """Return empty metrics structure"""
        return {
            'summary_stats': {},
            'time_series': pd.DataFrame(),
            'category_performance': pd.DataFrame(),
            'store_performance': pd.DataFrame(),
            'product_performance': pd.DataFrame(),
            'customer_insights': {},
            'trends': {}
        }
    
    def _calculate_summary_stats(self, data):
        """Calculate basic summary statistics"""
        return {
            'total_revenue': data['total_amount'].sum(),
            'total_transactions': len(data),
            'average_transaction_value': data['total_amount'].mean(),
            'median_transaction_value': data['total_amount'].median(),
            'total_units_sold': data['quantity'].sum(),
            'unique_products': data['product_name'].nunique(),
            'unique_customers': data['customer_id'].nunique(),
            'unique_stores': data['store_id'].nunique(),
            'revenue_per_customer': data.groupby('customer_id')['total_amount'].sum().mean(),
            'transactions_per_customer': data.groupby('customer_id').size().mean(),
            'most_popular_payment': data['payment_method'].mode().iloc[0] if not data.empty else None
        }
    
    def _calculate_time_series(self, data):
        """Calculate time-based metrics"""
        if data.empty:
            return pd.DataFrame()
        
        # Ensure timestamp is datetime
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Create time series with different granularities
        hourly_sales = data.groupby(data['timestamp'].dt.floor('H')).agg({
            'total_amount': 'sum',
            'transaction_id': 'count',
            'quantity': 'sum'
        }).rename(columns={'transaction_id': 'transaction_count'})
        
        # Add moving averages
        if len(hourly_sales) >= 3:
            hourly_sales['revenue_ma_3'] = hourly_sales['total_amount'].rolling(window=3, min_periods=1).mean()
        
        return hourly_sales.reset_index()
    
    def _calculate_category_performance(self, data):
        """Calculate category-wise performance metrics"""
        if data.empty:
            return pd.DataFrame()
        
        category_metrics = data.groupby('category').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'unit_price': 'mean'
        }).round(2)
        
        # Flatten column names
        category_metrics.columns = ['revenue', 'avg_transaction', 'transaction_count', 'units_sold', 'avg_unit_price']
        category_metrics = category_metrics.reset_index()
        
        # Calculate market share
        total_revenue = category_metrics['revenue'].sum()
        category_metrics['market_share_pct'] = (category_metrics['revenue'] / total_revenue * 100).round(2)
        
        # Calculate revenue per transaction
        category_metrics['revenue_per_transaction'] = (category_metrics['revenue'] / category_metrics['transaction_count']).round(2)
        
        return category_metrics.sort_values('revenue', ascending=False)
    
    def _calculate_store_performance(self, data):
        """Calculate store-wise performance metrics"""
        if data.empty:
            return pd.DataFrame()
        
        store_metrics = data.groupby('store_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'customer_id': 'nunique',
            'product_name': 'nunique'
        }).round(2)
        
        # Flatten column names
        store_metrics.columns = ['revenue', 'avg_transaction', 'transaction_count', 
                                'units_sold', 'unique_customers', 'unique_products']
        store_metrics = store_metrics.reset_index()
        
        # Calculate additional metrics
        store_metrics['revenue_per_customer'] = (store_metrics['revenue'] / store_metrics['unique_customers']).round(2)
        store_metrics['transactions_per_customer'] = (store_metrics['transaction_count'] / store_metrics['unique_customers']).round(2)
        
        return store_metrics.sort_values('revenue', ascending=False)
    
    def _calculate_product_performance(self, data):
        """Calculate product-wise performance metrics"""
        if data.empty:
            return pd.DataFrame()
        
        product_metrics = data.groupby(['product_name', 'category']).agg({
            'total_amount': ['sum', 'mean'],
            'quantity': 'sum',
            'transaction_id': 'count',
            'unit_price': 'mean'
        }).round(2)
        
        # Flatten column names
        product_metrics.columns = ['revenue', 'avg_transaction', 'quantity_sold', 
                                  'transaction_count', 'avg_unit_price']
        product_metrics = product_metrics.reset_index()
        
        # Calculate revenue rank within category
        product_metrics['category_rank'] = product_metrics.groupby('category')['revenue'].rank(ascending=False, method='dense')
        
        return product_metrics.sort_values('revenue', ascending=False)
    
    def _calculate_customer_insights(self, data):
        """Calculate customer behavior insights"""
        if data.empty:
            return {}
        
        customer_metrics = data.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'category': lambda x: x.nunique(),
            'store_id': lambda x: x.nunique()
        })
        
        # Flatten column names
        customer_metrics.columns = ['total_spent', 'avg_transaction', 'transaction_count',
                                   'total_items', 'categories_shopped', 'stores_visited']
        
        return {
            'total_customers': len(customer_metrics),
            'avg_customer_value': customer_metrics['total_spent'].mean(),
            'avg_transactions_per_customer': customer_metrics['transaction_count'].mean(),
            'avg_categories_per_customer': customer_metrics['categories_shopped'].mean(),
            'avg_stores_per_customer': customer_metrics['stores_visited'].mean(),
            'high_value_customers': len(customer_metrics[customer_metrics['total_spent'] > customer_metrics['total_spent'].quantile(0.9)]),
            'frequent_customers': len(customer_metrics[customer_metrics['transaction_count'] >= 3])
        }
    
    def _calculate_trends(self, data):
        """Calculate trend analysis"""
        if data.empty or len(data) < 2:
            return {}
        
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data = data.sort_values('timestamp')
        
        # Calculate growth trends
        recent_data = data.tail(len(data) // 2) if len(data) > 4 else data
        older_data = data.head(len(data) // 2) if len(data) > 4 else data
        
        if not recent_data.empty and not older_data.empty:
            recent_avg_revenue = recent_data['total_amount'].mean()
            older_avg_revenue = older_data['total_amount'].mean()
            
            revenue_growth = ((recent_avg_revenue - older_avg_revenue) / older_avg_revenue * 100) if older_avg_revenue > 0 else 0
            
            recent_transaction_count = len(recent_data)
            older_transaction_count = len(older_data)
            
            transaction_growth = ((recent_transaction_count - older_transaction_count) / older_transaction_count * 100) if older_transaction_count > 0 else 0
        else:
            revenue_growth = 0
            transaction_growth = 0
        
        # Peak hours analysis
        data['hour'] = data['timestamp'].dt.hour
        hourly_transactions = data.groupby('hour').size()
        peak_hour = hourly_transactions.idxmax() if not hourly_transactions.empty else None
        
        # Category trends
        category_recent = recent_data.groupby('category')['total_amount'].sum() if not recent_data.empty else pd.Series()
        category_older = older_data.groupby('category')['total_amount'].sum() if not older_data.empty else pd.Series()
        
        growing_categories = []
        for category in category_recent.index:
            if category in category_older.index and category_older[category] > 0:
                growth = (category_recent[category] - category_older[category]) / category_older[category] * 100
                if growth > 0:
                    growing_categories.append((category, growth))
        
        growing_categories = sorted(growing_categories, key=lambda x: x[1], reverse=True)
        
        return {
            'revenue_growth_percent': round(revenue_growth, 2),
            'transaction_growth_percent': round(transaction_growth, 2),
            'peak_hour': peak_hour,
            'growing_categories': growing_categories[:3] if growing_categories else [],
            'data_timespan_minutes': (data['timestamp'].max() - data['timestamp'].min()).total_seconds() / 60
        }
    
    def get_real_time_kpis(self, data, lookback_minutes=10):
        """Calculate real-time KPIs for dashboard"""
        if data.empty:
            return {}
        
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Filter to recent data
        cutoff_time = data['timestamp'].max() - timedelta(minutes=lookback_minutes)
        recent_data = data[data['timestamp'] >= cutoff_time]
        
        if recent_data.empty:
            return {}
        
        return {
            'transactions_last_10min': len(recent_data),
            'revenue_last_10min': recent_data['total_amount'].sum(),
            'avg_transaction_last_10min': recent_data['total_amount'].mean(),
            'top_product_last_10min': recent_data['product_name'].mode().iloc[0] if not recent_data.empty else None,
            'active_stores_last_10min': recent_data['store_id'].nunique(),
            'revenue_per_minute': recent_data['total_amount'].sum() / lookback_minutes
        }
