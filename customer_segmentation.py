import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class CustomerSegmentation:
    """Advanced customer segmentation and analysis"""
    
    def __init__(self):
        self.kmeans_model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.is_fitted = False
        
    def calculate_rfm_metrics(self, data):
        """Calculate RFM (Recency, Frequency, Monetary) metrics for customers"""
        if data.empty:
            return pd.DataFrame()
        
        # Convert timestamp to datetime
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        current_date = data['timestamp'].max()
        
        # Calculate RFM metrics
        rfm = data.groupby('customer_id').agg({
            'timestamp': lambda x: (current_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).round(2)
        
        rfm.columns = ['recency', 'frequency', 'monetary']
        rfm = rfm.reset_index()
        
        # Add RFM scores (1-5 scale)
        rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
        rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
        rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
        
        # Calculate RFM combined score
        rfm['rfm_score'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str)
        
        return rfm
    
    def segment_customers(self, data, n_clusters=4):
        """Segment customers using K-means clustering"""
        if data.empty:
            return pd.DataFrame(), {}
        
        # Calculate RFM metrics
        rfm = self.calculate_rfm_metrics(data)
        
        if rfm.empty or len(rfm) < n_clusters:
            return pd.DataFrame(), {}
        
        # Prepare features for clustering
        features = rfm[['recency', 'frequency', 'monetary']].fillna(0)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Apply K-means clustering
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans_model.fit_predict(features_scaled)
        
        # Add cluster labels
        rfm['cluster'] = cluster_labels
        
        # Define segment names based on RFM characteristics
        cluster_summary = rfm.groupby('cluster').agg({
            'recency': 'mean',
            'frequency': 'mean', 
            'monetary': 'mean',
            'customer_id': 'count'
        }).round(2)
        
        # Assign meaningful names to segments
        segment_names = self._assign_segment_names(cluster_summary)
        rfm['segment_name'] = rfm['cluster'].map(segment_names)
        
        # Calculate segment statistics
        segment_stats = self._calculate_segment_stats(rfm, data)
        
        self.is_fitted = True
        return rfm, segment_stats
    
    def _assign_segment_names(self, cluster_summary):
        """Assign meaningful names to customer segments"""
        segment_names = {}
        
        for cluster in cluster_summary.index:
            recency = cluster_summary.loc[cluster, 'recency']
            frequency = cluster_summary.loc[cluster, 'frequency']
            monetary = cluster_summary.loc[cluster, 'monetary']
            
            if frequency >= cluster_summary['frequency'].median() and monetary >= cluster_summary['monetary'].median():
                if recency <= cluster_summary['recency'].median():
                    segment_names[cluster] = "Champions"
                else:
                    segment_names[cluster] = "Loyal Customers"
            elif frequency >= cluster_summary['frequency'].median():
                if recency <= cluster_summary['recency'].median():
                    segment_names[cluster] = "Potential Loyalists"
                else:
                    segment_names[cluster] = "At Risk"
            elif monetary >= cluster_summary['monetary'].median():
                if recency <= cluster_summary['recency'].median():
                    segment_names[cluster] = "New Customers"
                else:
                    segment_names[cluster] = "Hibernating"
            else:
                if recency <= cluster_summary['recency'].median():
                    segment_names[cluster] = "Promising"
                else:
                    segment_names[cluster] = "Lost Customers"
        
        return segment_names
    
    def _calculate_segment_stats(self, rfm, original_data):
        """Calculate detailed statistics for each segment"""
        if original_data.empty:
            return {}
        
        segment_stats = {}
        
        for segment in rfm['segment_name'].unique():
            if pd.isna(segment):
                continue
                
            segment_customers = rfm[rfm['segment_name'] == segment]['customer_id'].tolist()
            segment_data = original_data[original_data['customer_id'].isin(segment_customers)]
            
            if not segment_data.empty:
                # Calculate category preferences
                category_prefs = segment_data.groupby('category')['total_amount'].sum().sort_values(ascending=False)
                
                # Calculate preferred shopping times
                segment_data_copy = segment_data.copy()
                segment_data_copy['hour'] = pd.to_datetime(segment_data_copy['timestamp']).dt.hour
                popular_hours = segment_data_copy['hour'].value_counts().head(3).index.tolist()
                
                # Calculate average metrics
                stats = {
                    'customer_count': len(segment_customers),
                    'avg_recency': rfm[rfm['segment_name'] == segment]['recency'].mean(),
                    'avg_frequency': rfm[rfm['segment_name'] == segment]['frequency'].mean(),
                    'avg_monetary': rfm[rfm['segment_name'] == segment]['monetary'].mean(),
                    'total_revenue': segment_data['total_amount'].sum(),
                    'avg_transaction_value': segment_data['total_amount'].mean(),
                    'preferred_categories': category_prefs.head(3).to_dict(),
                    'popular_shopping_hours': popular_hours,
                    'total_transactions': len(segment_data)
                }
                
                segment_stats[segment] = stats
        
        return segment_stats
    
    def get_customer_lifetime_value(self, data):
        """Calculate Customer Lifetime Value (CLV) predictions"""
        if data.empty:
            return pd.DataFrame()
        
        # Calculate basic CLV metrics
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        
        clv_data = data_copy.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'timestamp': ['min', 'max']
        })
        
        clv_data.columns = ['total_spent', 'avg_order_value', 'frequency', 'first_purchase', 'last_purchase']
        
        # Calculate customer lifespan in days
        clv_data['lifespan_days'] = (clv_data['last_purchase'] - clv_data['first_purchase']).dt.days
        clv_data['lifespan_days'] = clv_data['lifespan_days'].fillna(1)  # Handle single-purchase customers
        
        # Calculate purchase frequency (orders per day)
        clv_data['purchase_frequency'] = clv_data['frequency'] / (clv_data['lifespan_days'] + 1)
        
        # Simple CLV calculation: avg_order_value * purchase_frequency * predicted_lifespan
        predicted_lifespan = 365  # Assume 1 year
        clv_data['predicted_clv'] = clv_data['avg_order_value'] * clv_data['purchase_frequency'] * predicted_lifespan
        
        # Add CLV segments
        clv_data['clv_quartile'] = pd.qcut(clv_data['predicted_clv'], 4, labels=['Low', 'Medium', 'High', 'Premium'], duplicates='drop')
        
        return clv_data.reset_index().round(2)
    
    def analyze_customer_journey(self, data):
        """Analyze customer purchase journey and behavior patterns"""
        if data.empty:
            return {}
        
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        data_copy = data_copy.sort_values(['customer_id', 'timestamp'])
        
        journey_stats = {}
        
        # New vs Returning customer analysis
        first_purchases = data_copy.groupby('customer_id')['timestamp'].min()
        data_copy['is_first_purchase'] = data_copy.apply(
            lambda x: x['timestamp'] == first_purchases[x['customer_id']], axis=1
        )
        
        new_customers = data_copy[data_copy['is_first_purchase']]['customer_id'].nunique()
        returning_customers = data_copy[~data_copy['is_first_purchase']]['customer_id'].nunique()
        
        # Category progression analysis
        customer_category_progression = data_copy.groupby('customer_id')['category'].apply(list)
        
        # Popular first categories
        first_categories = data_copy[data_copy['is_first_purchase']]['category'].value_counts()
        
        # Cross-selling analysis
        customers_multi_category = data_copy.groupby('customer_id')['category'].nunique()
        cross_sell_rate = (customers_multi_category > 1).mean()
        
        journey_stats = {
            'new_customers': new_customers,
            'returning_customers': returning_customers,
            'retention_rate': returning_customers / (new_customers + returning_customers) if (new_customers + returning_customers) > 0 else 0,
            'cross_sell_rate': cross_sell_rate,
            'avg_categories_per_customer': customers_multi_category.mean(),
            'popular_first_categories': first_categories.head(5).to_dict()
        }
        
        return journey_stats
    
    def get_churn_risk_analysis(self, data):
        """Identify customers at risk of churning"""
        if data.empty:
            return pd.DataFrame()
        
        data_copy = data.copy()
        data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
        current_date = data_copy['timestamp'].max()
        
        # Calculate days since last purchase for each customer
        customer_last_purchase = data_copy.groupby('customer_id')['timestamp'].max()
        days_since_last = (current_date - customer_last_purchase).dt.days
        
        # Calculate customer purchase patterns
        customer_stats = data_copy.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'timestamp': ['min', 'max']
        })
        
        customer_stats.columns = ['total_spent', 'avg_transaction', 'frequency', 'first_purchase', 'last_purchase']
        customer_stats['days_since_last'] = days_since_last
        customer_stats['days_active'] = (customer_stats['last_purchase'] - customer_stats['first_purchase']).dt.days + 1
        
        # Calculate average days between purchases
        customer_stats['avg_days_between_purchases'] = customer_stats['days_active'] / customer_stats['frequency']
        
        # Define churn risk levels
        def get_churn_risk(row):
            days_since = row['days_since_last']
            avg_gap = row['avg_days_between_purchases']
            
            if pd.isna(avg_gap) or avg_gap == 0:
                avg_gap = 30  # Default assumption
            
            if days_since > avg_gap * 3:
                return 'High Risk'
            elif days_since > avg_gap * 2:
                return 'Medium Risk'
            elif days_since > avg_gap:
                return 'Low Risk'
            else:
                return 'Active'
        
        customer_stats['churn_risk'] = customer_stats.apply(get_churn_risk, axis=1)
        
        return customer_stats.reset_index().round(2)