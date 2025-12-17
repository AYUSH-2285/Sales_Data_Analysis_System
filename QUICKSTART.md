# 🚀 Sales Data Analysis System - Quick Start Guide

## Step 1: Create Project Structure

```bash
mkdir Sales_Data_Analysis_System
cd Sales_Data_Analysis_System

# Create subdirectories
mkdir -p data queries python insights/charts output
```

## Step 2: Download All Files

Place the downloaded files in the correct locations:

```
Sales_Data_Analysis_System/
├── schema.sql                    # Database schema
├── requirements.txt              # Python dependencies
├── README.md                     # Full documentation
├── .gitignore                    # Git ignore rules
├── data/
│   └── raw_sales_data.csv       # Sample data (provided)
├── queries/
│   └── queries.json             # SQL queries config
└── python/
    ├── __init__.py
    ├── config.py                # Database credentials
    ├── db.py                    # Database manager
    ├── query_loader.py          # Query loader
    ├── query_executor.py        # Query executor
    ├── analysis.py              # Analysis engine
    ├── visualization.py         # Visualization
    └── main.py                  # Main app
```

## Step 3: Set Up MySQL Database

### Option A: Command Line (Recommended)

```bash
# Login to MySQL and run schema
mysql -u root -p < schema.sql
```

### Option B: MySQL Workbench

1. Open MySQL Workbench
2. Create new query tab
3. Copy contents of `schema.sql`
4. Execute (Ctrl+Enter)

### Verify Setup

```sql
USE sales_analytics;
SHOW TABLES;
-- Should show: customers, products, sales
```

## Step 4: Update Database Credentials

Edit `python/config.py`:

```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_mysql_password'  # ← CHANGE THIS
DB_NAME = 'sales_analytics'
DB_PORT = 3306
```

## Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed mysql-connector-python pandas numpy matplotlib seaborn python-dotenv
```

## Step 6: Load Sample Data

```bash
cd python
python main.py --load-sample-data
```

**Expected output:**
```
✓ Connected to MySQL database: sales_analytics
📥 Loading sample data...
  Loading customers...
✓ Inserted 50 rows into customers
  Loading products...
✓ Inserted 20 rows into products
  Loading sales transactions...
✓ Inserted 300 rows into sales
✓ Sample data loaded successfully!
```

## Step 7: Run Complete Analysis

```bash
python main.py
```

**Expected output:**
```
============================================================
🚀 Starting Sales Data Analysis
============================================================

▶️  Running: monthly_sales
✓ CSV saved: monthly_sales.csv
  month    total_sales
0  2024-01  245633.24
1  2024-02  278444.32
...

▶️  Running: top_products
✓ CSV saved: top_products.csv
  product_name  total_units
0  Laptop Pro        28
1  Monitor 4K        24
...

[More analyses...]

✓ Analysis Complete!

📊 Output Location: /path/to/output
📈 Charts Location: /path/to/insights/charts
📄 Insights Location: /path/to/insights/insights.md
```

## Step 8: View Results

### CSV Reports
```bash
open output/monthly_sales.csv
open output/top_products.csv
# ... other CSV files
```

### Charts
```bash
open insights/charts/monthly_sales.png
open insights/charts/top_products.png
# ... other PNG files
```

### Insights Document
```bash
open insights/insights.md
```

---

## 🔧 Running Specific Queries

### Run Single Query (from python directory)

```bash
python main.py --query monthly_sales
python main.py --query top_products
python main.py --query sales_by_city
```

### Run Custom Query in Python

```python
from query_executor import QueryExecutor

executor = QueryExecutor()

# Without parameters
df = executor.execute('monthly_sales')
print(df)

# With parameters
df = executor.execute('top_products', params={'limit': 5})
print(df)
```

---

## 📚 Available Queries

| Query Name | Description | Parameters |
|-----------|-------------|-----------|
| `monthly_sales` | Total sales per month | None |
| `top_products` | Top selling products | `limit` (default: 10) |
| `top_customers` | Top customers by spending | `limit` (default: 10) |
| `sales_by_city` | Sales distribution by city | None |
| `product_category_analysis` | Revenue by category | None |
| `daily_sales_trend` | Daily sales trend | None |
| `customer_purchase_frequency` | Customer purchase segments | None |
| `product_revenue_ranking` | Products by revenue | `limit` (default: 10) |
| `customer_segment_analysis` | Detailed customer segments | None |
| `quarterly_sales_comparison` | Quarterly analysis | None |
| `product_performance_metrics` | Performance KPIs | None |
| `customer_city_insights` | Customer and city insights | None |

---

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"

**Solution:**
1. Verify MySQL is running: `mysql -u root -p`
2. Check credentials in `config.py`
3. Ensure database `sales_analytics` exists: `SHOW DATABASES;`

### Error: "Queries file not found"

**Solution:**
1. Verify `queries/queries.json` exists
2. Check file path in `config.py`: `QUERIES_FILE = ...`
3. Ensure JSON is valid: `python -m json.tool queries/queries.json`

### Error: "Permission denied" for output files

**Solution:**
```bash
chmod -R 755 output/
chmod -R 755 insights/
```

### No data appears in charts

**Solution:**
1. Verify data is loaded: `SELECT COUNT(*) FROM sales;` in MySQL
2. Check if analysis queries return results
3. Run: `python main.py --load-sample-data` again

---

## 📊 Project Architecture

```
┌──────────────────────────────────┐
│      main.py (Entry Point)       │
│   Orchestrates all operations    │
└─────────────────┬────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│analysis.py │visualization│ query_executor
│          │ │   .py      │ │              │
└──────────┘ └──────────┘ └─────┬────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌─────────┐ ┌────────┐
              │db.py     │ │queries. │ │config  │
              │          │ │json     │ │.py     │
              └────┬─────┘ └─────────┘ └────────┘
                   │
                   ▼
            ┌─────────────────┐
            │ MySQL Database  │
            │sales_analytics  │
            └─────────────────┘
```

---

## 🎓 Learning Points

### 1. **Config-Driven Architecture**
- SQL queries stored as JSON (not hardcoded)
- Easy to add/modify analyses without touching Python code
- Mirrors real-world analytics systems

### 2. **Safe Parameter Injection**
- Uses `%(param_name)s` placeholder syntax
- Prevents SQL injection attacks
- Supports dynamic query parameters

### 3. **Modular Design**
- Separation of concerns (DB, queries, analysis, visualization)
- Each module has single responsibility
- Easy to extend and test

### 4. **Professional Outputs**
- CSV exports for data sharing
- PNG charts for presentations
- Markdown reports for documentation

### 5. **Scalability**
- Adding new analysis: 1 query in `queries.json` + 1 function in `analysis.py`
- Supports multiple databases with config changes
- Ready for production deployment

---

## 📝 Interview Talking Points

**"I built a config-driven sales analytics engine where SQL queries are stored as JSON metadata. This architecture allows Python to dynamically load and execute queries without hard-coding, making the system maintainable and scalable. The system demonstrates:**

1. **SQL proficiency** - Complex joins, aggregations, date functions
2. **Python skills** - OOP, module design, error handling
3. **Data analysis** - Trend analysis, segmentation, KPI tracking
4. **Software architecture** - Separation of concerns, config-driven design
5. **Automation** - End-to-end pipeline from query to visualization"

---

## 🚀 Next Steps

1. ✅ Setup complete database and load data
2. 📊 Explore generated CSV and chart files
3. 🔍 Modify `queries.json` to add custom analyses
4. 📈 Create additional visualizations
5. 🌐 (Optional) Build Flask web dashboard
6. 📤 (Optional) Add email report delivery

---

**Last Updated**: December 2024
**Status**: Production Ready ✓