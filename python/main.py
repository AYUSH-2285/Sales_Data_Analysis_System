# ============================================
# Main Application Module
# Application entry point and orchestration
# ============================================

import sys
import os
import logging
from pathlib import Path
import pandas as pd
import argparse

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from db import DatabaseManager
from query_executor import QueryExecutor
from analysis import AnalysisEngine
from visualization import Visualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SalesAnalyticsApp:
    """Main application class."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.executor = QueryExecutor()
        self.analyzer = AnalysisEngine()
        self.visualizer = Visualizer()
    
    def load_sample_data(self):
        """Load sample data from CSV into database."""
        logger.info("📥 Loading sample data...")
        
        try:
            # Connect to database
            self.db.connect()
            
            # Read sample data file
            sample_file = config.SAMPLE_DATA_FILE
            if not sample_file.exists():
                logger.error(f"✗ Sample data file not found: {sample_file}")
                return False
            
            # Load customers
            logger.info("  Loading customers...")
            customers_data = [
                {'customer_name': f'Customer_{i}', 'city': city, 'country': 'India'}
                for i, city in enumerate(
                    ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'] * 10,
                    start=1
                )
            ]
            self.db.execute_insert_bulk('customers', customers_data)
            
            # Load products
            logger.info("  Loading products...")
            products_data = [
                {'product_name': name, 'category': cat, 'price': price}
                for name, cat, price in [
                    ('Laptop Pro', 'Electronics', 85000),
                    ('Desktop PC', 'Electronics', 55000),
                    ('Monitor 4K', 'Electronics', 25000),
                    ('Mechanical Keyboard', 'Accessories', 8000),
                    ('Gaming Mouse', 'Accessories', 3000),
                    ('Webcam HD', 'Peripherals', 4500),
                    ('USB Hub', 'Accessories', 1500),
                    ('Phone Stand', 'Accessories', 800),
                    ('Desk Lamp', 'Accessories', 2000),
                    ('Cable Organizer', 'Accessories', 500),
                    ('SSD 1TB', 'Components', 8000),
                    ('RAM 16GB', 'Components', 5000),
                    ('Graphics Card', 'Components', 35000),
                    ('Power Supply', 'Components', 6000),
                    ('Cooling Fan', 'Components', 2500),
                    ('Monitor Stand', 'Accessories', 1200),
                    ('Wireless Charger', 'Accessories', 2500),
                    ('Screen Protector', 'Accessories', 300),
                    ('Case Cover', 'Accessories', 400),
                    ('Speaker', 'Peripherals', 5000),
                ]
            ]
            self.db.execute_insert_bulk('products', products_data)
            
            # Load sales data from CSV if it exists
            if sample_file.exists():
                df_sales = pd.read_csv(sample_file)
                sales_data = df_sales.to_dict('records')
                self.db.execute_insert_bulk('sales', sales_data)
                logger.info(f"  ✓ Loaded {len(sales_data)} sales transactions")
            
            logger.info("✓ Sample data loaded successfully!")
            return True
        
        except Exception as e:
            logger.error(f"✗ Error loading sample data: {e}")
            return False
        
        finally:
            self.db.disconnect()
    
    def run_all_analyses(self):
        """Run all analyses and generate outputs."""
        logger.info("\n" + "="*60)
        logger.info("🚀 Starting Sales Data Analysis")
        logger.info("="*60 + "\n")
        
        try:
            self.db.connect()
            
            analyses = [
                ('monthly_sales', self.analyzer.get_monthly_sales, None),
                ('top_products', self.analyzer.get_top_products, {'limit': 10}),
                ('top_customers', self.analyzer.get_top_customers, {'limit': 10}),
                ('sales_by_city', self.analyzer.get_sales_by_city, None),
                ('product_category_analysis', self.analyzer.get_category_analysis, None),
                ('daily_sales_trend', self.analyzer.get_daily_sales_trend, None),
                ('customer_purchase_frequency', self.analyzer.get_customer_frequency, None),
                ('product_revenue_ranking', self.analyzer.get_product_revenue_ranking, {'limit': 10}),
            ]
            
            insights_content = "# 📊 Sales Data Analysis Report\n\n"
            insights_content += f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for analysis_name, analysis_func, params in analyses:
                try:
                    logger.info(f"\n▶️  Running: {analysis_name}")
                    
                    if params:
                        df_result = analysis_func(**params)
                    else:
                        df_result = analysis_func()
                    
                    if df_result is not None and not df_result.empty:
                        # Save to CSV
                        csv_file = config.OUTPUT_DIR / f"{analysis_name}.csv"
                        df_result.to_csv(csv_file, index=False)
                        logger.info(f"  ✓ CSV saved: {csv_file.name}")
                        
                        # Display data
                        logger.info(f"\n{df_result.to_string()}\n")
                        
                        # Generate visualization
                        self._generate_visualization(analysis_name, df_result)
                        
                        # Generate insights
                        insight_text = self._get_insight_text(analysis_name, df_result)
                        insights_content += f"\n## {analysis_name}\n{insight_text}\n"
                    
                except Exception as e:
                    logger.error(f"  ✗ Error in {analysis_name}: {e}")
            
            # Save insights to markdown
            insights_file = config.INSIGHTS_FILE
            with open(insights_file, 'w') as f:
                f.write(insights_content)
            logger.info(f"\n✓ Insights saved: {insights_file.name}")
            
            logger.info("\n" + "="*60)
            logger.info("✓ Analysis Complete!")
            logger.info("="*60)
            logger.info(f"\n📊 Output Location: {config.OUTPUT_DIR}")
            logger.info(f"📈 Charts Location: {config.CHARTS_DIR}")
            logger.info(f"📄 Insights Location: {insights_file}\n")
            
        except Exception as e:
            logger.error(f"✗ Analysis failed: {e}")
            raise
        
        finally:
            self.db.disconnect()
    
    def _generate_visualization(self, analysis_name, df):
        """Generate appropriate visualization for analysis."""
        try:
            if analysis_name == 'monthly_sales':
                self.visualizer.plot_monthly_sales(df)
            elif analysis_name == 'top_products':
                self.visualizer.plot_top_products(df)
            elif analysis_name == 'top_customers':
                self.visualizer.plot_top_customers(df)
            elif analysis_name == 'sales_by_city':
                self.visualizer.plot_sales_by_city(df)
            elif analysis_name == 'product_category_analysis':
                self.visualizer.plot_category_analysis(df)
            elif analysis_name == 'daily_sales_trend':
                self.visualizer.plot_daily_trend(df)
        except Exception as e:
            logger.warning(f"⚠️  Could not generate visualization: {e}")
    
    def _get_insight_text(self, analysis_name, df):
        """Generate insight text for analysis."""
        if analysis_name == 'monthly_sales':
            return self.analyzer.generate_monthly_insights(df)
        elif analysis_name == 'top_products':
            return self.analyzer.generate_product_insights(df)
        elif analysis_name == 'top_customers':
            return self.analyzer.generate_customer_insights(df)
        elif analysis_name == 'sales_by_city':
            return self.analyzer.generate_city_insights(df)
        elif analysis_name == 'product_category_analysis':
            return self.analyzer.generate_category_insights(df)
        else:
            return "Analysis completed successfully."


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Sales Data Analysis System - Config-Driven SQL Analytics Engine'
    )
    parser.add_argument(
        '--load-sample-data',
        action='store_true',
        help='Load sample data into database'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Run a specific query by name'
    )
    
    args = parser.parse_args()
    
    app = SalesAnalyticsApp()
    
    try:
        if args.load_sample_data:
            app.load_sample_data()
        elif args.query:
            logger.info(f"🔄 Executing query: {args.query}")
            df = app.executor.execute(args.query)
            print(df)
        else:
            app.run_all_analyses()
    
    except Exception as e:
        logger.error(f"✗ Application error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()