import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    """Detect anomalies in retail transaction data"""
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.05,  # Expect 5% of data to be anomalous
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def detect_anomalies(self, data, method='isolation_forest'):
        """
        Detect anomalies in transaction data
        
        Args:
            data: DataFrame with transaction data
            method: 'isolation_forest', 'statistical', or 'combined'
        
        Returns:
            DataFrame with anomalous transactions and scores
        """
        if data.empty:
            return pd.DataFrame()
        
        # Prepare features for anomaly detection
        features_df = self._prepare_features(data)
        
        if features_df.empty:
            return pd.DataFrame()
        
        if method == 'isolation_forest':
            anomalies = self._isolation_forest_detection(data, features_df)
        elif method == 'statistical':
            anomalies = self._statistical_detection(data)
        elif method == 'combined':
            iso_anomalies = self._isolation_forest_detection(data, features_df)
            stat_anomalies = self._statistical_detection(data)
            # Combine results - transaction is anomaly if detected by either method
            combined_indices = set(iso_anomalies.index).union(set(stat_anomalies.index))
            anomalies = data.loc[list(combined_indices)].copy()
            if not anomalies.empty:
                anomalies['anomaly_score'] = 0.8  # Combined detection score
        else:
            raise ValueError("Method must be 'isolation_forest', 'statistical', or 'combined'")
        
        return anomalies
    
    def _prepare_features(self, data):
        """Prepare numerical features for anomaly detection"""
        try:
            data = data.copy()
            
            # Convert timestamp to numerical features
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data['hour'] = data['timestamp'].dt.hour
            data['day_of_week'] = data['timestamp'].dt.dayofweek
            data['minute'] = data['timestamp'].dt.minute
            
            # Encode categorical variables
            category_encoded = pd.get_dummies(data['category'], prefix='cat')
            store_encoded = pd.get_dummies(data['store_id'], prefix='store')
            payment_encoded = pd.get_dummies(data['payment_method'], prefix='pay')
            
            # Select numerical features
            numerical_features = [
                'total_amount', 'quantity', 'unit_price', 
                'subtotal', 'tax_amount', 'hour', 'day_of_week', 'minute'
            ]
            
            # Combine all features
            features = data[numerical_features].copy()
            
            # Add encoded categorical features (limit to prevent too many features)
            if category_encoded.shape[1] <= 10:
                features = pd.concat([features, category_encoded], axis=1)
            if store_encoded.shape[1] <= 20:
                features = pd.concat([features, store_encoded], axis=1)
            if payment_encoded.shape[1] <= 10:
                features = pd.concat([features, payment_encoded], axis=1)
            
            # Remove any infinite or NaN values
            features = features.replace([np.inf, -np.inf], np.nan)
            features = features.fillna(features.median())
            
            return features
            
        except Exception as e:
            print(f"Error in feature preparation: {e}")
            return pd.DataFrame()
    
    def _isolation_forest_detection(self, data, features_df):
        """Detect anomalies using Isolation Forest"""
        try:
            if len(features_df) < 10:  # Need minimum samples
                return pd.DataFrame()
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features_df)
            
            # Fit and predict
            anomaly_labels = self.isolation_forest.fit_predict(features_scaled)
            anomaly_scores = self.isolation_forest.decision_function(features_scaled)
            
            # Get anomalous transactions (label = -1)
            anomaly_indices = np.where(anomaly_labels == -1)[0]
            
            if len(anomaly_indices) == 0:
                return pd.DataFrame()
            
            anomalies = data.iloc[anomaly_indices].copy()
            anomalies['anomaly_score'] = np.abs(anomaly_scores[anomaly_indices])
            
            # Sort by anomaly score (higher scores are more anomalous)
            anomalies = anomalies.sort_values('anomaly_score', ascending=False)
            
            return anomalies
            
        except Exception as e:
            print(f"Error in isolation forest detection: {e}")
            return pd.DataFrame()
    
    def _statistical_detection(self, data):
        """Detect anomalies using statistical methods"""
        try:
            anomalies_list = []
            data = data.copy()
            
            # Z-score method for transaction amounts
            amount_mean = data['total_amount'].mean()
            amount_std = data['total_amount'].std()
            
            if amount_std > 0:
                data['amount_zscore'] = np.abs((data['total_amount'] - amount_mean) / amount_std)
                amount_anomalies = data[data['amount_zscore'] > 3]  # 3 standard deviations
                if not amount_anomalies.empty:
                    anomalies_list.append(amount_anomalies.index)
            
            # IQR method for transaction amounts
            Q1 = data['total_amount'].quantile(0.25)
            Q3 = data['total_amount'].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:
                lower_bound = Q1 - 3 * IQR  # More aggressive threshold
                upper_bound = Q3 + 3 * IQR
                
                iqr_anomalies = data[
                    (data['total_amount'] < lower_bound) | 
                    (data['total_amount'] > upper_bound)
                ]
                if not iqr_anomalies.empty:
                    anomalies_list.append(iqr_anomalies.index)
            
            # Quantity-based anomalies
            quantity_mean = data['quantity'].mean()
            quantity_std = data['quantity'].std()
            
            if quantity_std > 0:
                data['quantity_zscore'] = np.abs((data['quantity'] - quantity_mean) / quantity_std)
                quantity_anomalies = data[data['quantity_zscore'] > 3]
                if not quantity_anomalies.empty:
                    anomalies_list.append(quantity_anomalies.index)
            
            # Time-based anomalies (transactions at unusual hours)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data['hour'] = data['timestamp'].dt.hour
            
            # Consider transactions outside 6 AM - 11 PM as potentially anomalous
            time_anomalies = data[(data['hour'] < 6) | (data['hour'] > 23)]
            if not time_anomalies.empty:
                anomalies_list.append(time_anomalies.index)
            
            # Combine all anomaly indices
            if anomalies_list:
                all_anomaly_indices = set().union(*anomalies_list)
                anomalies = data.loc[list(all_anomaly_indices)].copy()
                
                # Calculate composite anomaly score
                if 'amount_zscore' in anomalies.columns:
                    anomalies['anomaly_score'] = anomalies['amount_zscore']
                else:
                    anomalies['anomaly_score'] = 1.0
                
                return anomalies.sort_values('anomaly_score', ascending=False)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error in statistical detection: {e}")
            return pd.DataFrame()
    
    def get_anomaly_summary(self, data):
        """Get summary of anomaly detection results"""
        if data.empty:
            return {}
        
        anomalies = self.detect_anomalies(data, method='combined')
        
        if anomalies.empty:
            return {
                'total_transactions': len(data),
                'anomalous_transactions': 0,
                'anomaly_rate': 0.0,
                'total_anomalous_revenue': 0.0,
                'avg_anomaly_amount': 0.0,
                'anomaly_categories': {},
                'anomaly_stores': {}
            }
        
        return {
            'total_transactions': len(data),
            'anomalous_transactions': len(anomalies),
            'anomaly_rate': len(anomalies) / len(data) * 100,
            'total_anomalous_revenue': anomalies['total_amount'].sum(),
            'avg_anomaly_amount': anomalies['total_amount'].mean(),
            'max_anomaly_amount': anomalies['total_amount'].max(),
            'anomaly_categories': anomalies['category'].value_counts().to_dict(),
            'anomaly_stores': anomalies['store_id'].value_counts().to_dict(),
            'anomaly_hours': anomalies['timestamp'].dt.hour.value_counts().to_dict() if 'timestamp' in anomalies.columns else {}
        }
    
    def detect_real_time_anomalies(self, new_transaction, historical_data, threshold_std=2):
        """
        Detect if a new transaction is anomalous based on historical data
        
        Args:
            new_transaction: Single transaction (dict or Series)
            historical_data: Historical transaction data (DataFrame)
            threshold_std: Standard deviation threshold for anomaly detection
        
        Returns:
            dict with anomaly status and details
        """
        if historical_data.empty:
            return {'is_anomaly': False, 'reason': 'No historical data'}
        
        try:
            # Convert single transaction to comparable format
            if isinstance(new_transaction, dict):
                amount = new_transaction.get('total_amount', 0)
                quantity = new_transaction.get('quantity', 0)
                category = new_transaction.get('category', '')
            else:
                amount = new_transaction['total_amount']
                quantity = new_transaction['quantity']
                category = new_transaction['category']
            
            # Check amount anomaly
            hist_amounts = historical_data['total_amount']
            amount_mean = hist_amounts.mean()
            amount_std = hist_amounts.std()
            
            amount_zscore = abs((amount - amount_mean) / amount_std) if amount_std > 0 else 0
            
            # Check quantity anomaly
            hist_quantities = historical_data['quantity']
            quantity_mean = hist_quantities.mean()
            quantity_std = hist_quantities.std()
            
            quantity_zscore = abs((quantity - quantity_mean) / quantity_std) if quantity_std > 0 else 0
            
            # Check category-specific anomaly
            category_data = historical_data[historical_data['category'] == category]
            category_anomaly = False
            category_zscore = 0
            
            if not category_data.empty:
                cat_amounts = category_data['total_amount']
                cat_mean = cat_amounts.mean()
                cat_std = cat_amounts.std()
                category_zscore = abs((amount - cat_mean) / cat_std) if cat_std > 0 else 0
                category_anomaly = category_zscore > threshold_std
            
            # Determine if anomalous
            is_anomaly = (amount_zscore > threshold_std or 
                         quantity_zscore > threshold_std or 
                         category_anomaly)
            
            # Determine primary reason
            reasons = []
            if amount_zscore > threshold_std:
                reasons.append(f"Unusual amount (z-score: {amount_zscore:.2f})")
            if quantity_zscore > threshold_std:
                reasons.append(f"Unusual quantity (z-score: {quantity_zscore:.2f})")
            if category_anomaly:
                reasons.append(f"Unusual for category (z-score: {category_zscore:.2f})")
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': max(amount_zscore, quantity_zscore, category_zscore),
                'reasons': reasons,
                'amount_zscore': amount_zscore,
                'quantity_zscore': quantity_zscore,
                'category_zscore': category_zscore
            }
            
        except Exception as e:
            return {'is_anomaly': False, 'reason': f'Error in detection: {str(e)}'}
