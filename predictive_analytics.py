import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalytics:
    """Advanced predictive analytics for retail forecasting"""
    
    def __init__(self):
        self.sales_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.demand_model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def forecast_sales(self, data, forecast_days=7):
        """Forecast sales for the next N days"""
        if data.empty:
            return pd.DataFrame(), {}
        
        try:
            # Prepare time series data
            ts_data = self._prepare_time_series(data)
            
            if len(ts_data) < 7:  # Need minimum data points
                return pd.DataFrame(), {'error': 'Insufficient data for forecasting'}
            
            # Create features for time series forecasting
            features_df = self._create_time_features(ts_data)
            
            if features_df.empty:
                return pd.DataFrame(), {'error': 'Could not create features'}
            
            # Train model
            X = features_df.drop(['revenue', 'timestamp'], axis=1)
            y = features_df['revenue']
            
            self.sales_model.fit(X, y)
            
            # Generate future dates and features
            future_data = self._generate_future_features(ts_data, forecast_days)
            
            if future_data.empty:
                return pd.DataFrame(), {'error': 'Could not generate future features'}
            
            # Make predictions
            future_X = future_data.drop(['timestamp'], axis=1)
            predictions = self.sales_model.predict(future_X)
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'date': future_data['timestamp'],
                'predicted_revenue': np.maximum(predictions, 0),  # Ensure non-negative
                'confidence_lower': np.maximum(predictions * 0.8, 0),
                'confidence_upper': predictions * 1.2
            })
            
            # Calculate model metrics
            train_predictions = self.sales_model.predict(X)
            metrics = {
                'mae': mean_absolute_error(y, train_predictions),
                'rmse': np.sqrt(mean_squared_error(y, train_predictions)),
                'model_score': self.sales_model.score(X, y),
                'forecast_total': forecast_df['predicted_revenue'].sum()
            }
            
            self.is_fitted = True
            return forecast_df.round(2), metrics
            
        except Exception as e:
            return pd.DataFrame(), {'error': f'Forecasting error: {str(e)}'}
    
    def _prepare_time_series(self, data):
        """Prepare data for time series analysis"""
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        
        # Aggregate by hour
        hourly_data = data_copy.groupby(data_copy['timestamp'].dt.floor('H')).agg({
            'total_amount': 'sum',
            'transaction_id': 'count',
            'quantity': 'sum'
        }).rename(columns={
            'total_amount': 'revenue',
            'transaction_id': 'transactions',
            'quantity': 'items_sold'
        })
        
        # Fill missing hours with zero
        if not hourly_data.empty:
            full_range = pd.date_range(
                start=hourly_data.index.min(),
                end=hourly_data.index.max(),
                freq='H'
            )
            hourly_data = hourly_data.reindex(full_range, fill_value=0)
        
        return hourly_data.reset_index().rename(columns={'index': 'timestamp'})
    
    def _create_time_features(self, ts_data):
        """Create time-based features for forecasting"""
        if ts_data.empty:
            return pd.DataFrame()
        
        df = ts_data.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Time features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Lag features
        df['revenue_lag_1'] = df['revenue'].shift(1)
        df['revenue_lag_24'] = df['revenue'].shift(24)  # 24 hours ago
        
        # Rolling averages
        df['revenue_ma_3'] = df['revenue'].rolling(window=3, min_periods=1).mean()
        df['revenue_ma_12'] = df['revenue'].rolling(window=12, min_periods=1).mean()
        df['revenue_ma_24'] = df['revenue'].rolling(window=24, min_periods=1).mean()
        
        # Trend features
        df['hour_rank'] = df.groupby('hour')['revenue'].transform('mean')
        df['dow_rank'] = df.groupby('day_of_week')['revenue'].transform('mean')
        
        # Fill NaN values
        df = df.fillna(method='bfill').fillna(0)
        
        return df
    
    def _generate_future_features(self, historical_data, forecast_days):
        """Generate features for future time periods"""
        if historical_data.empty:
            return pd.DataFrame()
        
        # Get the last timestamp and generate future timestamps
        last_timestamp = historical_data['timestamp'].max()
        future_timestamps = pd.date_range(
            start=last_timestamp + timedelta(hours=1),
            periods=forecast_days * 24,
            freq='H'
        )
        
        # Create future dataframe
        future_df = pd.DataFrame({'timestamp': future_timestamps})
        
        # Add time features
        future_df['hour'] = future_df['timestamp'].dt.hour
        future_df['day_of_week'] = future_df['timestamp'].dt.dayofweek
        future_df['day_of_month'] = future_df['timestamp'].dt.day
        future_df['month'] = future_df['timestamp'].dt.month
        future_df['is_weekend'] = (future_df['day_of_week'] >= 5).astype(int)
        
        # Use historical averages for lag features and moving averages
        recent_revenue = historical_data['revenue'].tail(24).mean()
        future_df['revenue_lag_1'] = recent_revenue
        future_df['revenue_lag_24'] = recent_revenue
        future_df['revenue_ma_3'] = recent_revenue
        future_df['revenue_ma_12'] = recent_revenue
        future_df['revenue_ma_24'] = recent_revenue
        
        # Use historical patterns for trend features
        hour_patterns = historical_data.groupby(historical_data['timestamp'].dt.hour)['revenue'].mean()
        dow_patterns = historical_data.groupby(historical_data['timestamp'].dt.dayofweek)['revenue'].mean()
        
        future_df['hour_rank'] = future_df['hour'].map(hour_patterns).fillna(recent_revenue)
        future_df['dow_rank'] = future_df['day_of_week'].map(dow_patterns).fillna(recent_revenue)
        
        return future_df
    
    def demand_forecasting(self, data):
        """Forecast product demand patterns"""
        if data.empty:
            return pd.DataFrame(), {}
        
        try:
            # Aggregate demand by product and time
            data_copy = data.copy()
            data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
            data_copy['date'] = data_copy['timestamp'].dt.date
            
            # Daily product demand
            daily_demand = data_copy.groupby(['date', 'product_name', 'category']).agg({
                'quantity': 'sum',
                'total_amount': 'sum'
            }).reset_index()
            
            # Get top products for forecasting
            top_products = data_copy.groupby('product_name')['quantity'].sum().nlargest(10).index
            
            product_forecasts = {}
            
            for product in top_products:
                product_data = daily_demand[daily_demand['product_name'] == product].copy()
                
                if len(product_data) >= 3:  # Need minimum data
                    # Simple trend analysis
                    product_data['day_num'] = range(len(product_data))
                    
                    # Fit linear trend
                    X = product_data[['day_num']].values
                    y = product_data['quantity'].values
                    
                    self.demand_model.fit(X, y)
                    
                    # Predict next 7 days
                    future_days = np.array([[len(product_data) + i] for i in range(1, 8)])
                    future_demand = np.maximum(self.demand_model.predict(future_days), 0)
                    
                    product_forecasts[product] = {
                        'current_avg_daily': product_data['quantity'].mean(),
                        'trend_slope': self.demand_model.coef_[0] if hasattr(self.demand_model, 'coef_') else 0,
                        'predicted_demand_7d': future_demand.tolist(),
                        'total_predicted_7d': future_demand.sum(),
                        'category': product_data['category'].iloc[0]
                    }
            
            # Create summary forecast dataframe
            forecast_summary = []
            for product, forecast in product_forecasts.items():
                forecast_summary.append({
                    'product_name': product,
                    'category': forecast['category'],
                    'current_avg_daily': round(forecast['current_avg_daily'], 2),
                    'trend_slope': round(forecast['trend_slope'], 3),
                    'predicted_7d_total': round(forecast['total_predicted_7d'], 2),
                    'trend_direction': 'Increasing' if forecast['trend_slope'] > 0.1 else 'Decreasing' if forecast['trend_slope'] < -0.1 else 'Stable'
                })
            
            summary_df = pd.DataFrame(forecast_summary)
            
            # Calculate overall demand metrics
            metrics = {
                'total_products_analyzed': len(product_forecasts),
                'products_increasing': sum(1 for f in product_forecasts.values() if f['trend_slope'] > 0.1),
                'products_decreasing': sum(1 for f in product_forecasts.values() if f['trend_slope'] < -0.1),
                'avg_trend_slope': np.mean([f['trend_slope'] for f in product_forecasts.values()])
            }
            
            return summary_df, metrics
            
        except Exception as e:
            return pd.DataFrame(), {'error': f'Demand forecasting error: {str(e)}'}
    
    def seasonal_analysis(self, data):
        """Analyze seasonal patterns in sales data"""
        if data.empty:
            return {}
        
        try:
            data_copy = data.copy()
            data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
            
            # Hour of day patterns
            hourly_patterns = data_copy.groupby(data_copy['timestamp'].dt.hour).agg({
                'total_amount': 'mean',
                'transaction_id': 'count'
            }).round(2)
            
            # Day of week patterns
            daily_patterns = data_copy.groupby(data_copy['timestamp'].dt.day_name()).agg({
                'total_amount': 'mean',
                'transaction_id': 'count'
            }).round(2)
            
            # Category seasonality
            category_hourly = data_copy.groupby(['category', data_copy['timestamp'].dt.hour])['total_amount'].mean().unstack(fill_value=0)
            
            # Peak hours by category
            category_peaks = {}
            for category in category_hourly.index:
                peak_hour = category_hourly.loc[category].idxmax()
                peak_value = category_hourly.loc[category].max()
                category_peaks[category] = {'peak_hour': peak_hour, 'peak_revenue': peak_value}
            
            # Overall insights
            peak_hour_overall = hourly_patterns['total_amount'].idxmax()
            peak_day_overall = daily_patterns['total_amount'].idxmax()
            
            return {
                'hourly_patterns': hourly_patterns.to_dict(),
                'daily_patterns': daily_patterns.to_dict(),
                'category_peaks': category_peaks,
                'overall_peak_hour': peak_hour_overall,
                'overall_peak_day': peak_day_overall,
                'busiest_hours': hourly_patterns.nlargest(3, 'transaction_id').index.tolist(),
                'quietest_hours': hourly_patterns.nsmallest(3, 'transaction_id').index.tolist()
            }
            
        except Exception as e:
            return {'error': f'Seasonal analysis error: {str(e)}'}
    
    def inventory_optimization(self, data):
        """Provide inventory optimization recommendations"""
        if data.empty:
            return {}
        
        try:
            # Calculate inventory metrics
            product_metrics = data.groupby(['product_name', 'category']).agg({
                'quantity': ['sum', 'mean', 'std'],
                'total_amount': 'sum',
                'transaction_id': 'count'
            }).round(2)
            
            product_metrics.columns = ['total_sold', 'avg_per_transaction', 'quantity_std', 'total_revenue', 'transaction_count']
            product_metrics = product_metrics.reset_index()
            
            # Calculate velocity and variability
            product_metrics['velocity'] = product_metrics['total_sold'] / product_metrics['transaction_count']
            product_metrics['variability'] = product_metrics['quantity_std'] / product_metrics['avg_per_transaction']
            product_metrics['variability'] = product_metrics['variability'].fillna(0)
            
            # Classify products using ABC analysis (revenue) and XYZ analysis (variability)
            # ABC Classification
            product_metrics['revenue_cumsum'] = product_metrics.sort_values('total_revenue', ascending=False)['total_revenue'].cumsum()
            total_revenue = product_metrics['total_revenue'].sum()
            
            if total_revenue > 0:
                product_metrics['revenue_percentage'] = product_metrics['revenue_cumsum'] / total_revenue
                product_metrics['abc_class'] = pd.cut(
                    product_metrics['revenue_percentage'],
                    bins=[0, 0.7, 0.9, 1.0],
                    labels=['A', 'B', 'C']
                )
            else:
                product_metrics['abc_class'] = 'C'
            
            # XYZ Classification (variability)
            if product_metrics['variability'].max() > 0:
                product_metrics['xyz_class'] = pd.qcut(
                    product_metrics['variability'],
                    q=3,
                    labels=['X', 'Y', 'Z'],
                    duplicates='drop'
                )
            else:
                product_metrics['xyz_class'] = 'X'
            
            # Generate recommendations
            recommendations = []
            
            for _, row in product_metrics.iterrows():
                abc = row['abc_class']
                xyz = row['xyz_class']
                
                if abc == 'A' and xyz in ['X', 'Y']:
                    rec = "High priority - maintain high stock levels with frequent monitoring"
                elif abc == 'A' and xyz == 'Z':
                    rec = "High revenue but unpredictable - maintain safety stock"
                elif abc == 'B':
                    rec = "Medium priority - moderate stock levels with regular reviews"
                elif abc == 'C' and xyz in ['X', 'Y']:
                    rec = "Low priority but predictable - minimal stock levels"
                else:
                    rec = "Low priority and unpredictable - consider discontinuation"
                
                recommendations.append({
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'abc_class': abc,
                    'xyz_class': xyz,
                    'recommendation': rec,
                    'total_revenue': row['total_revenue'],
                    'velocity': row['velocity'],
                    'variability': row['variability']
                })
            
            recommendations_df = pd.DataFrame(recommendations)
            
            # Summary statistics
            summary = {
                'total_products_analyzed': len(product_metrics),
                'high_priority_products': len(recommendations_df[recommendations_df['abc_class'] == 'A']),
                'medium_priority_products': len(recommendations_df[recommendations_df['abc_class'] == 'B']),
                'low_priority_products': len(recommendations_df[recommendations_df['abc_class'] == 'C']),
                'predictable_products': len(recommendations_df[recommendations_df['xyz_class'] == 'X']),
                'unpredictable_products': len(recommendations_df[recommendations_df['xyz_class'] == 'Z'])
            }
            
            return {
                'recommendations': recommendations_df,
                'summary': summary,
                'top_performers': product_metrics.nlargest(5, 'total_revenue')[['product_name', 'total_revenue', 'abc_class']].to_dict('records'),
                'most_volatile': product_metrics.nlargest(5, 'variability')[['product_name', 'variability', 'xyz_class']].to_dict('records')
            }
            
        except Exception as e:
            return {'error': f'Inventory optimization error: {str(e)}'}