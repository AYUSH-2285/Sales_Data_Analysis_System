# ============================================
# Analysis Module
# Business logic and semantic analysis functions
# ============================================

import logging
from query_executor import QueryExecutor

logger = logging.getLogger(__name__)

class AnalysisEngine:
    """Semantic layer for business analytics."""
    
    def __init__(self):
        self.executor = QueryExecutor()
    
    # ============================================
    # Sales Analysis Functions
    # ============================================
    
    def get_monthly_sales(self):
        """Get total sales per month."""
        logger.info("📊 Analyzing: Monthly Sales Trend")
        df = self.executor.execute('monthly_sales')
        return df
    
    def get_top_products(self, limit=10):
        """Get top selling products."""
        logger.info(f"📊 Analyzing: Top {limit} Products")
        df = self.executor.execute('top_products', params={'limit': limit})
        return df
    
    def get_top_customers(self, limit=10):
        """Get top customers by spending."""
        logger.info(f"📊 Analyzing: Top {limit} Customers")
        df = self.executor.execute('top_customers', params={'limit': limit})
        return df
    
    def get_sales_by_city(self):
        """Get sales distribution by city."""
        logger.info("📊 Analyzing: Sales by City Distribution")
        df = self.executor.execute('sales_by_city')
        return df
    
    def get_category_analysis(self):
        """Get revenue analysis by product category."""
        logger.info("📊 Analyzing: Product Category Performance")
        df = self.executor.execute('product_category_analysis')
        return df
    
    def get_daily_sales_trend(self):
        """Get daily sales trend."""
        logger.info("📊 Analyzing: Daily Sales Trend")
        df = self.executor.execute('daily_sales_trend')
        return df
    
    def get_customer_frequency(self):
        """Get customer purchase frequency analysis."""
        logger.info("📊 Analyzing: Customer Purchase Frequency")
        df = self.executor.execute('customer_purchase_frequency')
        return df
    
    def get_product_revenue_ranking(self, limit=10):
        """Get products ranked by revenue."""
        logger.info(f"📊 Analyzing: Top {limit} Products by Revenue")
        df = self.executor.execute('product_revenue_ranking', params={'limit': limit})
        return df
    
    # ============================================
    # Insight Generation Functions
    # ============================================
    
    def generate_monthly_insights(self, df):
        """Generate insights from monthly sales data."""
        if df.empty:
            return "No data available for monthly analysis."
        
        insights = []
        insights.append(f"📅 **Monthly Sales Summary**")
        insights.append(f"- Total records: {len(df)}")
        
        if 'total_sales' in df.columns:
            max_month = df.loc[df['total_sales'].idxmax()] if len(df) > 0 else None
            min_month = df.loc[df['total_sales'].idxmin()] if len(df) > 0 else None
            avg_sales = df['total_sales'].mean()
            
            insights.append(f"- Average monthly sales: ₹{avg_sales:,.2f}")
            if max_month is not None:
                insights.append(f"- Peak month: {max_month.get('month', 'N/A')} (₹{max_month.get('total_sales', 0):,.2f})")
            if min_month is not None:
                insights.append(f"- Lowest month: {min_month.get('month', 'N/A')} (₹{min_month.get('total_sales', 0):,.2f})")
        
        return "\n".join(insights)
    
    def generate_product_insights(self, df):
        """Generate insights from product analysis."""
        if df.empty:
            return "No data available for product analysis."
        
        insights = []
        insights.append(f"🛍️ **Top Products Summary**")
        insights.append(f"- Products analyzed: {len(df)}")
        
        if 'total_units' in df.columns:
            total_units = df['total_units'].sum()
            insights.append(f"- Total units sold: {total_units}")
        
        if len(df) > 0:
            top_product = df.iloc[0]
            insights.append(f"- Best performer: {top_product.get('product_name', 'N/A')}")
        
        return "\n".join(insights)
    
    def generate_customer_insights(self, df):
        """Generate insights from customer analysis."""
        if df.empty:
            return "No data available for customer analysis."
        
        insights = []
        insights.append(f"👥 **Top Customers Summary**")
        insights.append(f"- Top customers analyzed: {len(df)}")
        
        if 'total_spent' in df.columns:
            total_revenue = df['total_spent'].sum()
            avg_spend = df['total_spent'].mean()
            insights.append(f"- Combined spend (top {len(df)}): ₹{total_revenue:,.2f}")
            insights.append(f"- Average spend per customer: ₹{avg_spend:,.2f}")
        
        return "\n".join(insights)
    
    def generate_city_insights(self, df):
        """Generate insights from city distribution."""
        if df.empty:
            return "No data available for city analysis."
        
        insights = []
        insights.append(f"🏙️ **Sales by City Summary**")
        insights.append(f"- Cities with sales: {len(df)}")
        
        if 'total_sales' in df.columns:
            top_city = df.loc[df['total_sales'].idxmax()] if len(df) > 0 else None
            if top_city is not None:
                insights.append(f"- Leading city: {top_city.get('city', 'N/A')} (₹{top_city.get('total_sales', 0):,.2f})")
        
        return "\n".join(insights)
    
    def generate_category_insights(self, df):
        """Generate insights from category analysis."""
        if df.empty:
            return "No data available for category analysis."
        
        insights = []
        insights.append(f"📈 **Product Category Performance**")
        insights.append(f"- Categories: {len(df)}")
        
        if 'total_revenue' in df.columns:
            total_revenue = df['total_revenue'].sum()
            insights.append(f"- Total category revenue: ₹{total_revenue:,.2f}")
        
        return "\n".join(insights)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    engine = AnalysisEngine()
    
    try:
        print("\n🔄 Running sample analysis...")
        df = engine.get_monthly_sales()
        print(df)
    except Exception as e:
        print(f"Note: Database must be populated first. Error: {e}")