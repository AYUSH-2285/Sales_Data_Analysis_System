# ============================================
# Visualization Module
# Chart generation and insight visualization
# ============================================

import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from config import CHARTS_DIR, CHART_FORMAT, CHART_DPI

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class Visualizer:
    """Generates visualizations from analysis results."""
    
    def __init__(self, charts_dir=None):
        self.charts_dir = Path(charts_dir or CHARTS_DIR)
        self.charts_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_monthly_sales(self, df, filename='monthly_sales'):
        """Create line chart for monthly sales trend."""
        if df.empty or 'month' not in df.columns:
            logger.warning("⚠️  Cannot plot monthly sales: missing data")
            return None
        
        plt.figure(figsize=(14, 6))
        plt.plot(df['month'], df['total_sales'], marker='o', linewidth=2, markersize=6, color='#2185ba')
        plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=11)
        plt.ylabel('Total Sales (₹)', fontsize=11)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def plot_top_products(self, df, filename='top_products'):
        """Create bar chart for top products."""
        if df.empty or 'product_name' not in df.columns:
            logger.warning("⚠️  Cannot plot top products: missing data")
            return None
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['total_units'], color='#40a68f')
        plt.title('Top Selling Products by Quantity', fontsize=14, fontweight='bold')
        plt.xlabel('Product', fontsize=11)
        plt.ylabel('Units Sold', fontsize=11)
        plt.xticks(range(len(df)), df['product_name'], rotation=45, ha='right')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def plot_top_customers(self, df, filename='top_customers'):
        """Create horizontal bar chart for top customers."""
        if df.empty or 'customer_name' not in df.columns:
            logger.warning("⚠️  Cannot plot top customers: missing data")
            return None
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(df)), df['total_spent'], color='#f6a042')
        plt.title('Top Customers by Spending', fontsize=14, fontweight='bold')
        plt.ylabel('Customer', fontsize=11)
        plt.xlabel('Amount Spent (₹)', fontsize=11)
        plt.yticks(range(len(df)), df['customer_name'])
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'₹{width:,.0f}',
                    ha='left', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def plot_sales_by_city(self, df, filename='sales_by_city'):
        """Create pie chart for sales distribution by city."""
        if df.empty or 'city' not in df.columns:
            logger.warning("⚠️  Cannot plot city sales: missing data")
            return None
        
        plt.figure(figsize=(10, 8))
        colors = sns.color_palette("husl", len(df))
        plt.pie(df['total_sales'], labels=df['city'], autopct='%1.1f%%',
               colors=colors, startangle=90, textprops={'fontsize': 10})
        plt.title('Sales Distribution by City', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def plot_category_analysis(self, df, filename='category_revenue'):
        """Create bar chart for category revenue."""
        if df.empty or 'category' not in df.columns:
            logger.warning("⚠️  Cannot plot category analysis: missing data")
            return None
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(df)), df['total_revenue'], color='#6c757d')
        plt.title('Revenue by Product Category', fontsize=14, fontweight='bold')
        plt.xlabel('Category', fontsize=11)
        plt.ylabel('Total Revenue (₹)', fontsize=11)
        plt.xticks(range(len(df)), df['category'], rotation=45, ha='right')
        
        # Add value labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}',
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def plot_daily_trend(self, df, filename='daily_sales_trend'):
        """Create area chart for daily sales trend."""
        if df.empty or 'order_date' not in df.columns:
            logger.warning("⚠️  Cannot plot daily trend: missing data")
            return None
        
        plt.figure(figsize=(14, 6))
        plt.fill_between(range(len(df)), df['sales_amount'], alpha=0.4, color='#2185ba')
        plt.plot(range(len(df)), df['sales_amount'], linewidth=2, color='#2185ba')
        plt.title('Daily Sales Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=11)
        plt.ylabel('Sales Amount (₹)', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filepath = self._save_chart(filename)
        logger.info(f"✓ Chart saved: {filepath}")
        plt.close()
        
        return filepath
    
    def _save_chart(self, filename):
        """Save chart to file."""
        filepath = self.charts_dir / f"{filename}.{CHART_FORMAT}"
        plt.savefig(filepath, dpi=CHART_DPI, bbox_inches='tight')
        return filepath
    
    def create_summary_stats_table(self, title, data_dict):
        """Create a text-based summary statistics display."""
        summary = f"\n{'='*50}\n{title}\n{'='*50}\n"
        for key, value in data_dict.items():
            summary += f"{key}: {value}\n"
        summary += f"{'='*50}\n"
        return summary


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("✓ Visualization module loaded")