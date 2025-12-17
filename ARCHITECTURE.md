# 🏗️ System Architecture & Design Patterns

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   USER / DEVELOPER                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ╔════════════════════════════════════╗
        ║      main.py (Entry Point)         ║
        ║   Orchestrates entire workflow     ║
        ╚════════════╤═══════════════════════╝
                     │
     ┌───────────────┼───────────────┬─────────────────┐
     │               │               │                 │
     ▼               ▼               ▼                 ▼
┌──────────┐  ┌──────────┐  ┌───────────────┐  ┌──────────────┐
│analysis. │  │visualiz- │  │query_executor │  │config.py     │
│py        │  │ation.py  │  │              │  │(Environment) │
│          │  │          │  │              │  │              │
│- Analysis│  │- Charts  │  │- Param Safety│  │- DB Creds    │
│- Insights│  │- PNG/SVG │  │- Execution   │  │- Paths       │
└────┬─────┘  └────┬─────┘  └───────┬──────┘  └──────────────┘
     │             │                │
     │             └────────┬───────┘
     │                      │
     └──────────┬───────────┘
                │
     ┌──────────▼──────────┐
     │ query_loader.py     │
     │  (Query Registry)   │
     │                     │
     │ - Load queries.json │
     │ - Validate syntax   │
     │ - Provide metadata  │
     └──────────┬──────────┘
                │
     ┌──────────▼──────────┐
     │  queries.json       │
     │  (Config File)      │
     │                     │
     │ 12 pre-built        │
     │ analytics queries   │
     └──────────┬──────────┘
                │
     ┌──────────▼──────────┐
     │      db.py          │
     │  (DB Manager)       │
     │                     │
     │- Connection Pool    │
     │- Query Execution    │
     │- Error Handling     │
     └──────────┬──────────┘
                │
                ▼
        ╔═══════════════════╗
        ║ MySQL Database    ║
        ║  sales_analytics  ║
        ║                   ║
        ║ - customers       ║
        ║ - products        ║
        ║ - sales (facts)   ║
        ╚═══════════════════╝
```

---

## Module Interaction Flow

```
User Command: python main.py
              │
              ▼
         ┌─────────────┐
         │ main.py     │ ← Load config.py (creds, paths)
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
LOAD_DATA  ANALYZE    (Repeat for each analysis)
    │       (8x)          │
    │           │         │
    │           ▼         │
    │     AnalysisEngine  │
    │           │         │
    │           ▼         │
    │   get_monthly_sales()
    │   get_top_products()
    │        ... (8 more)
    │           │
    │           ▼
    │  QueryExecutor.execute()
    │           │
    │           ├─► query_loader.py (Get SQL from JSON)
    │           │
    │           ▼
    │     ✓ Load "monthly_sales" query
    │     ✓ Validate parameters
    │     ✓ Pass SQL to db.py
    │
    │           ▼
    │      db.py (DatabaseManager)
    │           │
    │           ├─► Check connection
    │           ├─► Execute SQL
    │           ├─► Fetch results
    │           ▼
    │      MySQL Database
    │      (Execute & Return)
    │           │
    │           ▼
    │      Pandas DataFrame
    │           │
    ├──────┬────┼──────┬────────┐
    │      │    │      │        │
    ▼      ▼    ▼      ▼        ▼
  SAVE  GEN    VIZ   INSIGHT  RETURN
  CSV   PLOT   CHT   TEXT      DF
  │      │     │     │         │
  └──────┴─────┴─────┴─────────┘
         │
    ┌────▼─────┐
    │  OUTPUT  │
    │  /       │
    │├─ .csv   │
    │├─ .png   │
    │└─ .md    │
    └──────────┘
```

---

## Data Model (Database Schema)

```
                    CUSTOMERS
                    ┌────────────────────────┐
                    │ customer_id (PK)       │
                    │ customer_name          │
                    │ city                   │
                    │ country                │
                    │ created_at             │
                    └────┬───────────────────┘
                         │
                         │ 1:M
                         │
                         ▼
                       SALES (Fact Table)
                    ┌────────────────────────┐
                    │ order_id (PK)          │
                    │ customer_id (FK) ──────┼──► CUSTOMERS
                    │ product_id (FK) ───────┼──► PRODUCTS
                    │ order_date             │
                    │ quantity               │
                    │ total_amount           │
                    │ created_at             │
                    └────────────────────────┘
                         ▲
                         │
                         │ 1:M
                         │
                    ┌────┴───────────────────┐
                    │ PRODUCTS               │
                    ├────────────────────────┤
                    │ product_id (PK)        │
                    │ product_name           │
                    │ category               │
                    │ price                  │
                    │ created_at             │
                    └────────────────────────┘

Star Schema:
  CUSTOMERS ──┐
              ├──► SALES ◄──┐
  PRODUCTS ───┘              │
              (FACT TABLE)   │
                  ▲          │
                  │    One query joins
                  │    all three tables
                  └──────────────────
```

---

## Design Patterns Used

### 1. **Config-Driven Pattern**
```
Traditional:
  SQL queries → Hard-coded in .sql files → Difficult to modify
  
Our Approach:
  SQL queries → Stored in queries.json → Easy to modify, extend
  
Benefit: Non-technical users can modify queries without code changes
```

### 2. **Repository Pattern**
```
DatabaseManager (Repository)
├── connect()
├── disconnect()
├── execute_query()
├── execute_insert_bulk()
└── is_connected()

Benefit: Abstracts database operations from business logic
```

### 3. **Singleton Pattern**
```
Global Instance Management:

get_db_manager()     ← Returns single DatabaseManager instance
get_query_loader()   ← Returns single QueryLoader instance

Benefit: Prevents multiple database connections, efficient resource use
```

### 4. **Semantic Layer Pattern**
```
Raw SQL ──────► Query Executor ──────► Analysis Engine
  │                    │                     │
  └─ Complex          └─ Parameter    └─ High-level
    joins               injection         functions
    aggregations        validation        (business logic)
```

### 5. **Pipeline/Orchestration Pattern**
```
main.py orchestrates:

Load Data → Analyze → Visualize → Export → Document
   │           │          │         │         │
   └───────────┴──────────┴─────────┴─────────┘
        (All in sequence, with error handling)
```

---

## Query Execution Flow (Detailed)

```
Step 1: Query Request
  executor.execute('monthly_sales', params={'limit': 10})
  
Step 2: Query Loader
  query_loader.get_query('monthly_sales')
  Returns:
  {
    'description': 'Total sales per month',
    'sql': 'SELECT DATE_FORMAT(...)',
    'params': []
  }
  
Step 3: Parameter Validation
  validate_params(provided_params, required_params)
  ✓ All required params provided
  ✓ No extra params passed
  
Step 4: Database Manager
  db.connect()
  ✓ Establish connection to MySQL
  
Step 5: Execute SQL
  cursor.execute(sql, params)
  ✓ Use parameterized placeholders: %(param_name)s
  ✓ Prevents SQL injection
  
Step 6: Fetch Results
  results = cursor.fetchall()
  Returns: [
    {'month': '2024-01', 'total_sales': 245633.24},
    {'month': '2024-02', 'total_sales': 278444.32},
    ...
  ]
  
Step 7: Convert to DataFrame
  df = pd.DataFrame(results)
  More convenient for analysis
  
Step 8: Return
  return df  ← Ready for visualization/export
```

---

## Error Handling Strategy

```
Try/Catch Hierarchy:

┌─ main.py (Top-level)
│  └─ try:
│     ├─ AnalysisEngine
│     │  └─ try:
│     │     ├─ QueryExecutor
│     │     │  └─ try:
│     │     │     ├─ QueryLoader
│     │     │     └─ DatabaseManager
│     │     │        └─ MySQL
│     │     └─ catch: Log & continue
│     │
│     ├─ Visualizer
│     │  └─ try/catch: Log chart errors
│     │
│     └─ File I/O
│        └─ try/catch: Log export errors
│
│  └─ catch: Exit with error code
└─

Every layer:
  1. Logs errors with context
  2. Provides user-friendly messages
  3. Continues processing when safe
  4. Fails gracefully with rollback
```

---

## File Organization Logic

```
Sales_Data_Analysis_System/
│
├── python/                   ◄─ Core application code
│   ├── config.py            ◄─ Environment & paths
│   ├── db.py                ◄─ Database operations
│   ├── query_loader.py      ◄─ Query config management
│   ├── query_executor.py    ◄─ Safe query execution
│   ├── analysis.py          ◄─ Business logic
│   ├── visualization.py     ◄─ Charting
│   └── main.py              ◄─ Entry point
│
├── queries/                 ◄─ Configuration layer
│   └── queries.json        ◄─ SQL stored as data
│
├── data/                    ◄─ Raw input data
│   └── raw_sales_data.csv
│
├── output/                  ◄─ Generated CSV reports
│   ├── monthly_sales.csv
│   ├── top_products.csv
│   └── ...
│
├── insights/                ◄─ Generated outputs
│   ├── insights.md         ◄─ Report document
│   └── charts/             ◄─ Visualizations
│       ├── monthly_sales.png
│       ├── top_products.png
│       └── ...
│
├── schema.sql              ◄─ Database schema
├── requirements.txt        ◄─ Dependencies
├── README.md               ◄─ Full documentation
├── QUICKSTART.md           ◄─ Quick start guide
├── FILES_SUMMARY.md        ◄─ This file
└── .gitignore
```

---

## Scalability Considerations

### Adding a New Analysis

**Step 1: Add Query to queries.json**
```json
{
  "my_new_analysis": {
    "description": "What this analyzes",
    "sql": "SELECT ... FROM ...",
    "params": ["param1", "param2"]
  }
}
```

**Step 2: Add Function to analysis.py**
```python
def get_my_analysis(self, param1=None):
    logger.info("Analyzing...")
    df = self.executor.execute('my_new_analysis', 
                               params={'param1': param1})
    return df
```

**Step 3: Add Visualization to visualization.py**
```python
def plot_my_analysis(self, df, filename='my_analysis'):
    plt.figure(figsize=(12, 6))
    # Your chart code
    self._save_chart(filename)
```

**Step 4: Add to main.py's run_all_analyses()**
```python
('my_new_analysis', self.analyzer.get_my_analysis, {'param1': value}),
```

**Result**: New analysis integrated without modifying core logic

---

## Performance Optimization Strategies

### 1. **Database Level**
- Indexes on frequently queried columns (order_date, customer_id)
- Foreign key relationships for integrity
- GROUP BY on indexed columns

### 2. **Python Level**
- Singleton pattern prevents multiple connections
- Batch insert operations for bulk data
- DataFrame operations vectorized (pandas)

### 3. **Architecture Level**
- Query validation before execution
- Parameter bounds checking
- Optional caching layer (future enhancement)

### 4. **Visualization Level**
- SVG option for web (smaller file size)
- Chart generation only for needed analyses
- DPI configurable

---

## Security Measures

```
1. Parameterized Queries
   SQL: "SELECT * FROM sales WHERE customer_id = %(id)s"
   Prevents: SQL injection attacks

2. Input Validation
   - Check parameter types
   - Validate ranges
   - Whitelist query names

3. Credential Management
   - Store in config.py (local development)
   - Use environment variables (production)
   - Never commit passwords to git

4. Error Handling
   - Log errors securely (no sensitive data)
   - User-friendly error messages
   - Stack traces only in debug mode
```

---

## Testing Strategy (Future Enhancement)

```python
# Unit Tests
test_db.py           ← Test database operations
test_query_loader.py ← Test query loading
test_executor.py     ← Test query execution
test_analysis.py     ← Test analysis logic

# Integration Tests
test_end_to_end.py   ← Full workflow

# Run Tests
pytest tests/
```

---

**Architecture Version**: 1.0.0
**Last Updated**: December 2024
**Status**: Production Ready ✓