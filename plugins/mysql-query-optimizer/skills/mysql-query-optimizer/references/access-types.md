# MySQL 5.7 Access Types Reference

Detailed explanation of each access type in EXPLAIN output, from worst to best performance.

## ALL (Full Table Scan)

**What it means:** MySQL reads every row in the table to find matches.

**When MySQL chooses it:**
- No usable index exists for the query conditions
- Index exists but optimizer estimates full scan is faster (small table or high selectivity)
- Using functions on indexed columns: `WHERE YEAR(date_col) = 2024`
- Implicit type conversion: `WHERE varchar_col = 12345`
- LIKE with leading wildcard: `WHERE name LIKE '%smith'`

**How to fix:**
```sql
-- Add appropriate index
CREATE INDEX idx_table_column ON table_name (column_name);

-- For function-wrapped columns, use generated columns (5.7.6+)
ALTER TABLE t ADD COLUMN date_year INT GENERATED ALWAYS AS (YEAR(date_col)) STORED;
CREATE INDEX idx_date_year ON t (date_year);

-- Fix type mismatches
WHERE varchar_col = '12345'  -- Use correct type
```

## index (Full Index Scan)

**What it means:** MySQL scans the entire index tree (better than ALL, but still reads all entries).

**When MySQL chooses it:**
- Query can be satisfied entirely from index (covering index)
- ORDER BY matches index order, no WHERE clause
- COUNT(*) on indexed column

**How to fix:**
```sql
-- Add WHERE condition to enable range scan
SELECT * FROM users ORDER BY created_at;          -- index scan
SELECT * FROM users WHERE created_at > NOW() - INTERVAL 7 DAY ORDER BY created_at;  -- range

-- For COUNT, consider summary tables if called frequently
```

## range (Index Range Scan)

**What it means:** MySQL uses an index to retrieve rows within a specific range.

**When MySQL chooses it:**
- `=`, `<>`, `>`, `>=`, `<`, `<=`, `IS NULL`, `<=>`, `BETWEEN`, `LIKE 'prefix%'`, `IN()`
- Conditions that allow identifying a contiguous range in the index

**Performance characteristics:**
- Generally good performance
- Efficiency depends on range selectivity
- Multiple ranges (IN, OR) may be less efficient

**Optimization opportunities:**
```sql
-- Narrow the range if possible
WHERE created_at > '2024-01-01'  -- Wide range
WHERE created_at > '2024-06-01'  -- Narrower, faster

-- For IN with many values, consider temp table + JOIN
WHERE id IN (1,2,3,...100 values)  -- Many index lookups
-- vs
CREATE TEMPORARY TABLE tmp_ids (id INT PRIMARY KEY);
INSERT INTO tmp_ids VALUES (1),(2),(3)...;
SELECT t.* FROM target t JOIN tmp_ids i ON t.id = i.id;
```

## index_subquery

**What it means:** Similar to ref, but for IN subqueries that return non-unique values.

**Example triggering this:**
```sql
SELECT * FROM t1 WHERE col IN (SELECT col FROM t2 WHERE condition);
```

**Optimization:** Often better rewritten as JOIN. See rewrite-patterns.md.

## unique_subquery

**What it means:** Similar to eq_ref, but for IN subqueries that return unique values.

**Example triggering this:**
```sql
SELECT * FROM t1 WHERE pk IN (SELECT pk FROM t2 WHERE condition);
```

**Performance:** Usually acceptable, but JOIN may still be faster.

## index_merge

**What it means:** MySQL uses multiple indexes and merges results.

**Types:**
- `intersect`: AND conditions on different indexes
- `union`: OR conditions on different indexes
- `sort_union`: OR with range conditions

**Example:**
```sql
-- Uses both idx_a and idx_b
SELECT * FROM t WHERE a = 1 OR b = 2;
```

**Optimization:**
```sql
-- Often better with composite index
CREATE INDEX idx_a_b ON t (a, b);

-- Or explicit UNION for OR conditions
SELECT * FROM t WHERE a = 1
UNION ALL
SELECT * FROM t WHERE b = 2 AND a != 1;
```

## ref_or_null

**What it means:** Like ref, but also searches for NULL values.

**Example triggering this:**
```sql
SELECT * FROM t WHERE key_col = 'value' OR key_col IS NULL;
```

**Performance:** Usually acceptable. Consider if NULL check is necessary.

## ref (Non-Unique Index Lookup)

**What it means:** MySQL uses a non-unique index to find matching rows.

**When MySQL chooses it:**
- Equality comparison on non-unique index
- Leftmost prefix of composite index

**Performance:** Good. This is typically acceptable for most queries.

**Example:**
```sql
-- With index on customer_id (non-unique)
SELECT * FROM orders WHERE customer_id = 123;  -- ref access
```

## eq_ref (Unique Index Lookup)

**What it means:** MySQL uses a unique or primary key index, returning at most one row.

**When MySQL chooses it:**
- JOIN on primary key or unique index
- All parts of unique index are used with equality

**Performance:** Excellent. Optimal for joins.

**Example:**
```sql
-- Joining on primary key
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;  -- eq_ref on customers
```

## const (Single Row)

**What it means:** The table has at most one matching row, read at optimization time.

**When MySQL chooses it:**
- Primary key or unique index with constant values
- Query can be resolved during optimization

**Example:**
```sql
SELECT * FROM users WHERE id = 1;  -- const (if id is PK)
SELECT * FROM config WHERE key = 'setting' AND env = 'prod';  -- const (if unique on key+env)
```

## system

**What it means:** Table has exactly one row (system table).

**Performance:** Best possible - value is effectively a constant.

## NULL

**What it means:** Query doesn't need to access the table.

**When it appears:**
- Impossible WHERE condition: `WHERE 1 = 0`
- Query on empty table with `MIN()`/`MAX()`
- Subquery optimized away

## Access Type Improvement Strategies

| Current | Target | Strategy |
|---------|--------|----------|
| ALL → range | Add index on WHERE columns |
| ALL → ref | Add index, ensure equality comparison |
| index → range | Add WHERE clause using indexed columns |
| range → ref | Use equality instead of range when possible |
| ref → eq_ref | Use unique index or primary key |
| index_merge → ref | Create composite index |
