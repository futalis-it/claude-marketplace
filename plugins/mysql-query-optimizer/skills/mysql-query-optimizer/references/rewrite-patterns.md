# MySQL Query Rewrite Patterns

Common query patterns and their optimized alternatives for MySQL 5.7.

## IN Subquery → JOIN

### Problem
IN subqueries often become DEPENDENT SUBQUERY, executing once per outer row.

### Before
```sql
SELECT *
FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE country = 'DE'
);
```

### After
```sql
SELECT o.*
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE c.country = 'DE';
```

### When to use
- Subquery returns multiple rows
- Both tables have indexes on join columns
- Outer table is large

## NOT IN → LEFT JOIN + IS NULL

### Problem
NOT IN cannot use indexes efficiently and has NULL handling issues.

### Before
```sql
SELECT *
FROM products
WHERE id NOT IN (SELECT product_id FROM discontinued);
```

### After
```sql
SELECT p.*
FROM products p
LEFT JOIN discontinued d ON p.id = d.product_id
WHERE d.product_id IS NULL;
```

### Alternative: NOT EXISTS
```sql
SELECT *
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM discontinued d WHERE d.product_id = p.id
);
```

### When to use
- Always prefer LEFT JOIN or NOT EXISTS over NOT IN
- NOT IN fails unexpectedly with NULL values in subquery

## Correlated Subquery → JOIN

### Problem
Correlated subqueries execute once per outer row.

### Before
```sql
SELECT o.*,
    (SELECT SUM(quantity) FROM order_items oi WHERE oi.order_id = o.id) as total_items
FROM orders o;
```

### After
```sql
SELECT o.*, COALESCE(oi_sum.total_items, 0) as total_items
FROM orders o
LEFT JOIN (
    SELECT order_id, SUM(quantity) as total_items
    FROM order_items
    GROUP BY order_id
) oi_sum ON o.id = oi_sum.order_id;
```

### When to use
- Scalar subqueries in SELECT clause
- Multiple references to same correlated data

## OR Conditions → UNION

### Problem
OR on different columns prevents efficient index use.

### Before
```sql
SELECT * FROM products
WHERE category_id = 5 OR supplier_id = 10;
```

### After
```sql
SELECT * FROM products WHERE category_id = 5
UNION
SELECT * FROM products WHERE supplier_id = 10;
```

### For UNION ALL (no deduplication needed)
```sql
SELECT * FROM products WHERE category_id = 5
UNION ALL
SELECT * FROM products WHERE supplier_id = 10 AND category_id != 5;
```

### When to use
- OR between columns with separate indexes
- Each condition is selective
- UNION ALL when results are known to be disjoint

## GROUP BY Optimization

### Problem
GROUP BY creates temporary table if columns aren't indexed properly.

### Before
```sql
SELECT customer_id, COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;
```

### Optimized Index
```sql
-- Index should have: WHERE columns first, then GROUP BY columns
CREATE INDEX idx_orders_status_customer ON orders (status, customer_id);
```

### Covering Index (avoids table lookup)
```sql
CREATE INDEX idx_orders_cover ON orders (status, customer_id, id);
-- Includes id for COUNT(*) to be satisfied from index
```

## LIMIT with Large Offset → Keyset Pagination

### Problem
`LIMIT 1000000, 20` scans and discards 1 million rows.

### Before
```sql
SELECT * FROM logs
ORDER BY id
LIMIT 1000000, 20;
```

### After (Keyset/Cursor Pagination)
```sql
-- Store last_id from previous page
SELECT * FROM logs
WHERE id > :last_id
ORDER BY id
LIMIT 20;
```

### For Non-Sequential Ordering
```sql
-- Before
SELECT * FROM products ORDER BY name LIMIT 10000, 20;

-- After (with covering index on name, id)
SELECT p.*
FROM products p
INNER JOIN (
    SELECT id FROM products ORDER BY name LIMIT 10000, 20
) sub ON p.id = sub.id
ORDER BY p.name;
```

## Derived Table Materialization

### Problem
MySQL 5.7 may re-evaluate derived tables multiple times.

### Before
```sql
SELECT *
FROM (SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id) derived
WHERE total > 1000;
```

### After (with STRAIGHT_JOIN hint for predictable behavior)
```sql
SELECT STRAIGHT_JOIN *
FROM (SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id) derived
WHERE total > 1000;
```

### Alternative: Temporary Table
```sql
CREATE TEMPORARY TABLE tmp_totals AS
SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id;

ALTER TABLE tmp_totals ADD INDEX (total);

SELECT * FROM tmp_totals WHERE total > 1000;
```

## EXISTS vs IN for Large Outer Set

### Problem
IN with large outer set checks all subquery results.

### Before
```sql
SELECT * FROM large_table
WHERE id IN (SELECT foreign_id FROM small_table);
```

### After
```sql
SELECT * FROM large_table lt
WHERE EXISTS (SELECT 1 FROM small_table st WHERE st.foreign_id = lt.id);
```

### When to use
- Outer table is large, subquery result is small: use EXISTS
- Outer table is small, subquery result is large: use IN

## Function on Column → Computed Column

### Problem
Functions prevent index usage.

### Before
```sql
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
```

### After (Range-based)
```sql
SELECT * FROM orders
WHERE created_at >= '2024-01-15 00:00:00'
  AND created_at < '2024-01-16 00:00:00';
```

### Alternative: Generated Column (5.7.6+)
```sql
ALTER TABLE orders
ADD COLUMN created_date DATE GENERATED ALWAYS AS (DATE(created_at)) STORED;

CREATE INDEX idx_orders_created_date ON orders (created_date);

SELECT * FROM orders WHERE created_date = '2024-01-15';
```

## Multiple COUNT with CASE → Single Pass

### Before
```sql
SELECT
    (SELECT COUNT(*) FROM orders WHERE status = 'pending') as pending,
    (SELECT COUNT(*) FROM orders WHERE status = 'shipped') as shipped,
    (SELECT COUNT(*) FROM orders WHERE status = 'delivered') as delivered;
```

### After
```sql
SELECT
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
    SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) as shipped,
    SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered
FROM orders;
```

## Self-Join for Running Totals (No Window Functions in 5.7)

### Cumulative Sum
```sql
SELECT
    o1.id,
    o1.amount,
    (SELECT SUM(o2.amount) FROM orders o2 WHERE o2.id <= o1.id) as running_total
FROM orders o1
ORDER BY o1.id;
```

### Variable-Based (Faster for Large Tables)
```sql
SET @running_total := 0;

SELECT
    id,
    amount,
    (@running_total := @running_total + amount) as running_total
FROM orders
ORDER BY id;
```

### Important
- Variable approach requires ORDER BY in same query
- Reset variable before each execution
- Consider upgrading to MySQL 8.0 for proper window functions
