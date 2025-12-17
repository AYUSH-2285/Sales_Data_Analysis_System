# Sales Data Analysis System

## Project Setup & Configuration

### Prerequisites
- **MySQL**: 8.0+ (installed and running)
- **Python**: 3.8+
- **pip**: For package management

### Installation Steps

#### 1. Create Project Directory
```bash
mkdir Sales_Data_Analysis_System
cd Sales_Data_Analysis_System
```

#### 2. Clone/Download Project Files
Extract all project files into the directory structure shown below.

#### 3. Create MySQL Database
```bash
mysql -u root -p < schema.sql
```
Enter your MySQL password when prompted. This creates the `sales_analytics` database with tables: `customers`, `products`, and `sales`.

#### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Configure Database Credentials
Edit `python/config.py` and update:
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_mysql_password'  # Change this
DB_NAME = 'sales_analytics'
```

#### 6. Load Sample Data
```bash
python python/main.py --load-sample-data
```
This populates the database with 50 customers, 20 products, and 300 sales transactions.

#### 7. Run Analytics
```bash
python python/main.py
```

---

## Project Structure

```
Sales_Data_Analysis_System/
│
├── data/
│   └── raw_sales_data.csv              # Sample data (generated)
│
├── queries/
│   └── queries.json                    # All SQL queries as config
│
├── python/
│   ├── __init__.py
│   ├── config.py                       # Database credentials & config
│   ├── db.py                           # MySQL connection manager
│   ├── query_loader.py                 # Load queries from JSON
│   ├── query_executor.py               # Safe query execution engine
│   ├── analysis.py                     # Business logic & analytics
│   ├── visualization.py                # Chart generation
│   └── main.py                         # Application entry point
│
├── insights/
│   ├── insights.md                     # Generated business insights
│   └── charts/                         # PNG/SVG visualizations
│
├── output/
│   └── *.csv                           # Generated reports
│
├── schema.sql                          # Database schema
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── .gitignore                          # Git ignore rules

```

---

## Module Responsibilities

### `config.py`
- Database credentials
- Paths for outputs
- Environment variables

### `db.py`
- MySQL connection management
- Connection pooling (optional)
- Connection cleanup

### `query_loader.py`
- Reads `queries.json`
- Validates query structure
- Provides query metadata

### `query_executor.py`
- Selects query by name
- Injects parameters safely
- Executes using pandas
- Returns DataFrames

### `analysis.py`
- High-level business logic
- Semantic layer over queries
- Defines analysis functions

### `visualization.py`
- Converts DataFrames to charts
- Saves as PNG/SVG
- Generates chart metadata

### `main.py`
- Application entry point
- Orchestrates workflow
- Generates all outputs

---

## Usage Examples

### Run All Analyses
```bash
python python/main.py
```

### Load Sample Data
```bash
python python/main.py --load-sample-data
```

### Run Specific Query
```python
from python.query_executor import QueryExecutor
executor = QueryExecutor()
result = executor.execute('monthly_sales')
print(result)
```

### Add Custom Query
Edit `queries/queries.json`:
```json
{
  "my_custom_query": {
    "description": "My analysis",
    "sql": "SELECT * FROM sales WHERE ...",
    "params": []
  }
}
```

Then call it:
```python
executor.execute('my_custom_query')
```

---

## Pre-Built Queries

### 1. `monthly_sales`
- **Description**: Total sales per month
- **Parameters**: None
- **Output**: Month, Total Sales

### 2. `top_products`
- **Description**: Top 10 selling products by quantity
- **Parameters**: `limit` (default: 10)
- **Output**: Product Name, Total Units Sold

### 3. `top_customers`
- **Description**: Top 10 customers by spending
- **Parameters**: `limit` (default: 10)
- **Output**: Customer Name, Total Spent

### 4. `sales_by_city`
- **Description**: Sales distribution by city
- **Parameters**: None
- **Output**: City, Total Sales, Order Count

### 5. `product_category_analysis`
- **Description**: Revenue by product category
- **Parameters**: None
- **Output**: Category, Total Revenue, Total Units, Avg Price

### 6. `daily_sales_trend`
- **Description**: Daily sales trend over time
- **Parameters**: None
- **Output**: Date, Sales Amount, Order Count

### 7. `customer_purchase_frequency`
- **Description**: Customer segments by purchase frequency
- **Parameters**: None
- **Output**: Customer ID, Customer Name, Purchase Count, Total Spent

### 8. `product_revenue_ranking`
- **Description**: Products ranked by revenue generation
- **Parameters**: `limit` (default: 10)
- **Output**: Product Name, Revenue, Units Sold

---

## Output Artifacts

### CSV Reports (`output/`)
- `monthly_sales.csv`
- `top_products.csv`
- `top_customers.csv`
- `sales_by_city.csv`
- `product_category_analysis.csv`
- `daily_sales_trend.csv`
- `customer_purchase_frequency.csv`
- `product_revenue_ranking.csv`

### Visualizations (`insights/charts/`)
- Monthly sales trend (line chart)
- Top 10 products (bar chart)
- Top 10 customers (horizontal bar)
- Sales by city distribution (pie chart)
- Category revenue breakdown (bar chart)
- Daily sales trend (area chart)

### Insights Document (`insights/insights.md`)
- Executive summary
- Key findings from each analysis
- Business recommendations
- Data quality notes

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         main.py                         │
│    (Application Entry Point)            │
└────────────────┬────────────────────────┘
                 │
     ┌───────────┴───────────┐
     ▼                       ▼
┌──────────────┐    ┌────────────────┐
│ analysis.py  │    │ visualization  │
│ (Business    │    │ .py (Charts)   │
│  Logic)      │    └────────────────┘
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ query_executor.py        │
│ (Query Execution Engine) │
└──────┬───────────────────┘
       │
  ┌────┴──────┐
  ▼           ▼
┌──────────────────┐  ┌──────────────────┐
│ query_loader.py  │  │ db.py            │
│ (Load from JSON) │  │ (MySQL Manager)  │
└──────────────────┘  └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │   MySQL Database │
                      │  (sales_analytics)
                      └──────────────────┘

┌──────────────────────────────────────────┐
│ queries.json (Query Registry)            │
│ {"query_name": {...}, ...}               │
└──────────────────────────────────────────┘
```

---

## Key Design Principles

### 1. **Config-Driven**
SQL queries are stored as JSON, not hard-coded in Python.

### 2. **Separation of Concerns**
- Query definition (JSON)
- Query execution (Python)
- Analysis logic (Python)
- Visualization (Python)

### 3. **Parameterized Queries**
All queries use `%(param_name)s` syntax for safe parameter injection.

### 4. **No ORM**
Raw SQL with pandas for maximum control and SQL learning.

### 5. **Reproducible**
Same query always produces same results; all outputs are saved.

---

## Troubleshooting

### MySQL Connection Error
```
Error: Can't connect to MySQL server
```
**Solution**: Ensure MySQL is running and credentials in `config.py` are correct.

### Query Not Found
```
Error: Query 'my_query' not found in queries.json
```
**Solution**: Check `queries/queries.json` for correct query name.

### Missing Dependencies
```
ModuleNotFoundError: No module named 'mysql'
```
**Solution**: Run `pip install -r requirements.txt`

### Permission Denied
```
PermissionError: [Errno 13] Permission denied: '/output'
```
**Solution**: Ensure `output/` and `insights/charts/` directories have write permissions.

---

## Interview-Ready Talking Points

1. **Config-driven architecture**: "I externalized SQL as JSON, allowing Python to dynamically load and execute queries without hard-coding."

2. **Parameterized execution**: "All queries use safe parameter injection to prevent SQL injection attacks."

3. **Separation of concerns**: "Queries, execution, analysis, and visualization are in separate modules for maintainability."

4. **Reproducible analytics**: "Every analysis generates CSV exports and charts, making insights audit-able and shareable."

5. **Scalability**: "Adding new analyses requires only a new entry in `queries.json` and a function in `analysis.py`."

---

## Future Enhancements

- [ ] Web dashboard with Flask/FastAPI
- [ ] Scheduled report generation (cron jobs)
- [ ] Email report delivery
- [ ] Query performance monitoring
- [ ] Data validation and quality checks
- [ ] Multi-database support
- [ ] REST API for query execution
- [ ] Interactive chart generation (Plotly)

---

## License
This is a portfolio project. Feel free to use and modify.

---

## Contact
For questions or suggestions, reach out to the project maintainer.

---

**Last Updated**: December 2024
**Version**: 1.0.0