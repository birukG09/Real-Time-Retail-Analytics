import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

class RetailDataGenerator:
    """Generate synthetic retail sales data for analytics dashboard"""
    
    def __init__(self):
        self.fake = Faker()
        
        # Product categories and their typical price ranges
        self.categories = {
            'Electronics': {'min_price': 50, 'max_price': 2000, 'weight': 0.15},
            'Clothing': {'min_price': 10, 'max_price': 200, 'weight': 0.25},
            'Food & Beverages': {'min_price': 1, 'max_price': 50, 'weight': 0.30},
            'Home & Garden': {'min_price': 5, 'max_price': 500, 'weight': 0.15},
            'Books & Media': {'min_price': 5, 'max_price': 100, 'weight': 0.10},
            'Toys & Games': {'min_price': 5, 'max_price': 150, 'weight': 0.05}
        }
        
        # Store locations
        self.stores = [f"STORE_{i:03d}" for i in range(1, 21)]  # 20 stores
        
        # Product names by category
        self.products = {
            'Electronics': [
                'Smartphone X1', 'Laptop Pro', 'Wireless Headphones', 'Tablet Plus', 
                'Smart Watch', 'Gaming Console', 'Bluetooth Speaker', 'Digital Camera',
                'USB Cable', 'Power Bank', 'Monitor 24"', 'Keyboard Wireless'
            ],
            'Clothing': [
                'Cotton T-Shirt', 'Denim Jeans', 'Running Shoes', 'Casual Dress',
                'Winter Jacket', 'Sports Shorts', 'Polo Shirt', 'Sneakers',
                'Hoodie', 'Business Suit', 'Summer Hat', 'Leather Belt'
            ],
            'Food & Beverages': [
                'Premium Coffee', 'Organic Juice', 'Energy Drink', 'Protein Bar',
                'Chocolate Cookies', 'Fresh Bread', 'Mineral Water', 'Green Tea',
                'Instant Noodles', 'Fruit Salad', 'Yogurt Cup', 'Energy Smoothie'
            ],
            'Home & Garden': [
                'LED Light Bulb', 'Plant Pot', 'Kitchen Utensils', 'Bathroom Towel',
                'Garden Hose', 'Storage Box', 'Picture Frame', 'Cleaning Spray',
                'Candle Set', 'Door Mat', 'Wall Clock', 'Flower Vase'
            ],
            'Books & Media': [
                'Best Seller Novel', 'Programming Guide', 'Cookbook', 'Art Magazine',
                'Children Book', 'Biography', 'Science Journal', 'Travel Guide',
                'Music CD', 'Documentary DVD', 'Comic Book', 'Poetry Collection'
            ],
            'Toys & Games': [
                'Board Game Classic', 'Action Figure', 'Puzzle 1000pc', 'RC Car',
                'Building Blocks', 'Doll House', 'Educational Toy', 'Card Game',
                'Stuffed Animal', 'Art Supplies', 'Musical Instrument', 'Sports Ball'
            ]
        }
        
        # Initialize random seed for consistent but varied data
        random.seed(42)
        np.random.seed(42)
        
    def _get_weighted_category(self):
        """Select a category based on weights"""
        categories = list(self.categories.keys())
        weights = [self.categories[cat]['weight'] for cat in categories]
        return np.random.choice(categories, p=weights)
    
    def _generate_transaction(self, timestamp=None):
        """Generate a single transaction"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Select category and product
        category = self._get_weighted_category()
        product_name = random.choice(self.products[category])
        
        # Generate price based on category
        min_price = self.categories[category]['min_price']
        max_price = self.categories[category]['max_price']
        unit_price = round(random.uniform(min_price, max_price), 2)
        
        # Generate quantity (most transactions are single items)
        quantity_weights = [0.6, 0.25, 0.1, 0.04, 0.01]  # Weights for 1, 2, 3, 4, 5+ items
        quantity = np.random.choice([1, 2, 3, 4, random.randint(5, 10)], p=quantity_weights)
        
        # Calculate totals
        subtotal = round(unit_price * quantity, 2)
        tax_rate = 0.08  # 8% tax
        tax_amount = round(subtotal * tax_rate, 2)
        total_amount = round(subtotal + tax_amount, 2)
        
        # Occasionally generate anomalous transactions
        anomaly_chance = 0.02  # 2% chance of anomaly
        if random.random() < anomaly_chance:
            # Create anomalies by multiplying price or quantity
            anomaly_type = random.choice(['high_price', 'high_quantity'])
            if anomaly_type == 'high_price':
                multiplier = random.uniform(5, 20)
                unit_price *= multiplier
                subtotal = round(unit_price * quantity, 2)
                tax_amount = round(subtotal * tax_rate, 2)
                total_amount = round(subtotal + tax_amount, 2)
            elif anomaly_type == 'high_quantity':
                quantity *= random.randint(10, 50)
                subtotal = round(unit_price * quantity, 2)
                tax_amount = round(subtotal * tax_rate, 2)
                total_amount = round(subtotal + tax_amount, 2)
        
        return {
            'transaction_id': f"TXN_{random.randint(100000, 999999)}",
            'timestamp': timestamp,
            'store_id': random.choice(self.stores),
            'product_name': product_name,
            'category': category,
            'unit_price': unit_price,
            'quantity': quantity,
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']),
            'customer_id': f"CUST_{random.randint(1000, 9999)}"
        }
    
    def generate_batch(self, batch_size=10, start_time=None):
        """Generate a batch of transactions"""
        if start_time is None:
            start_time = datetime.now()
        
        transactions = []
        for i in range(batch_size):
            # Spread transactions over the last few minutes
            time_offset = random.uniform(-300, 0)  # Last 5 minutes
            transaction_time = start_time + timedelta(seconds=time_offset)
            
            transaction = self._generate_transaction(transaction_time)
            transactions.append(transaction)
        
        return pd.DataFrame(transactions)
    
    def generate_historical_data(self, days=7, transactions_per_day=100):
        """Generate historical data for testing"""
        all_transactions = []
        end_time = datetime.now()
        
        for day in range(days):
            day_start = end_time - timedelta(days=day+1)
            
            # Generate transactions throughout the day
            for _ in range(transactions_per_day):
                # Random time during business hours (8 AM to 10 PM)
                hour_offset = random.uniform(8, 22)
                minute_offset = random.uniform(0, 59)
                
                transaction_time = day_start.replace(
                    hour=int(hour_offset),
                    minute=int(minute_offset),
                    second=random.randint(0, 59),
                    microsecond=0
                )
                
                transaction = self._generate_transaction(transaction_time)
                all_transactions.append(transaction)
        
        return pd.DataFrame(all_transactions)
    
    def get_summary_stats(self, data):
        """Get summary statistics for generated data"""
        if data.empty:
            return {}
        
        return {
            'total_transactions': len(data),
            'total_revenue': data['total_amount'].sum(),
            'avg_transaction_value': data['total_amount'].mean(),
            'unique_products': data['product_name'].nunique(),
            'unique_stores': data['store_id'].nunique(),
            'date_range': {
                'start': data['timestamp'].min(),
                'end': data['timestamp'].max()
            },
            'category_breakdown': data.groupby('category')['total_amount'].sum().to_dict()
        }
