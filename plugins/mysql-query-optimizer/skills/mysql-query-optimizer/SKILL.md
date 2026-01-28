---
name: mysql-explain-optimizer
description: Analyzes MySQL 5.7 EXPLAIN FORMAT=JSON output to identify performance issues and provide optimization recommendations with rewritten queries. Use when user provides EXPLAIN JSON output or asks about slow MySQL queries.
---

# MySQL 5.7 EXPLAIN Optimizer

Analyze EXPLAIN FORMAT=JSON output to identify performance issues and provide actionable optimization recommendations.

## Quick Analysis Checklist

Check these red flags in order of severity:

| Priority | Check | Threshold | Severity |
|----------|-------|-----------|----------|
| 1 | `access_type` = "ALL" | rows > 1000 | CRITICAL |
| 2 | `using_filesort` = true | rows > 10000 | HIGH |
| 3 | `using_temporary_table` = true | any | HIGH |
| 4 | `access_type` = "index" | rows > 10000 | MEDIUM |
| 5 | `rows_examined_per_scan` >> `rows_produced_per_join` | ratio > 100 | MEDIUM |
| 6 | No `key` when `possible_keys` exists | any | MEDIUM |
| 7 | Suboptimal join order | large table first | MEDIUM |
| 8 | `select_type` = "DEPENDENT SUBQUERY" | any | HIGH |
| 9 | `materialized_from_subquery` present | large dataset | MEDIUM |
| 10 | Missing covering index | frequent query | LOW |

## Critical JSON Fields to Extract

### Query Block Level
```
query_block.select_id
query_block.cost_info.query_cost
query_block.ordering_operation.using_filesort
query_block.grouping_operation.using_temporary_table
```

### Table Level (nested_loop or table)
```
table.table_name
table.access_type          # THE most important field
table.possible_keys
table.key                  # Actually used index
table.key_length           # How much of index is used
table.rows_examined_per_scan
table.rows_produced_per_join
table.filtered             # Percentage of rows remaining after WHERE
table.cost_info.read_cost
table.cost_info.eval_cost
table.used_key_parts       # Which columns of index are used
table.attached_condition   # WHERE clause for this table
```

### Subquery Level
```
query_block.optimized_away
query_block.subqueries[].query_block
query_block.materialized_from_subquery
```

## Access Type Severity Scale

From worst to best performance:

| Access Type | Severity | Description | Action Required |
|-------------|----------|-------------|-----------------|
| `ALL` | CRITICAL | Full table scan | Add index immediately |
| `index` | HIGH | Full index scan | Narrow index usage or add better index |
| `range` | MEDIUM | Index range scan | Acceptable, can sometimes improve |
| `index_subquery` | MEDIUM | Subquery uses index | Consider JOIN rewrite |
| `unique_subquery` | LOW | Subquery on unique index | Usually acceptable |
| `index_merge` | LOW | Multiple indexes merged | Consider composite index |
| `ref_or_null` | LOW | Index + NULL check | Usually acceptable |
| `ref` | OK | Non-unique index lookup | Good performance |
| `eq_ref` | GOOD | Unique index lookup | Optimal for joins |
| `const` | OPTIMAL | Single row (constant) | Best possible |
| `system` | OPTIMAL | System table | Best possible |

See `references/access-types.md` for detailed explanations.

## Issue Detection Rules

### 1. Missing Index (CRITICAL)

**Detect when:**
```
access_type = "ALL" AND rows_examined_per_scan > 1000
```

**Recommendation:**
- Identify columns in `attached_condition`
- Create index on filtered columns
- Consider composite index for multiple conditions

**Index suggestion format:**
```sql
CREATE INDEX idx_{table}_{columns} ON {table} ({columns});
```

### 2. Suboptimal Index Choice (HIGH)

**Detect when:**
```
key != best candidate from possible_keys
OR key_length < optimal_length
OR used_key_parts < available_key_parts
```

**Recommendation:**
- Analyze why optimizer chose current index
- Check if statistics are outdated: `ANALYZE TABLE {table}`
- Consider index hints if optimizer consistently wrong
- Verify column order in composite indexes

### 3. Filesort Operation (HIGH)

**Detect when:**
```
ordering_operation.using_filesort = true AND rows > 10000
```

**Recommendation:**
- Add ORDER BY columns to index
- For composite index: WHERE columns first, then ORDER BY columns
- Check if ORDER BY matches index order (ASC/DESC)

**Pattern:**
```sql
-- Before: separate index for WHERE and ORDER BY
SELECT * FROM orders WHERE customer_id = 1 ORDER BY created_at;

-- After: composite index
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at);
```

### 4. Temporary Table (HIGH)

**Detect when:**
```
grouping_operation.using_temporary_table = true
OR using_temporary_table = true
```

**Common causes:**
- GROUP BY on columns not in index
- DISTINCT on large result sets
- UNION operations
- ORDER BY and GROUP BY on different columns

**Recommendation:**
- Ensure GROUP BY columns are leftmost in an index
- Consider covering index for SELECT columns
- Evaluate if DISTINCT is necessary

### 5. Poor Join Order (MEDIUM)

**Detect when:**
```
First table in nested_loop has highest rows_examined_per_scan
AND subsequent tables have smaller row counts
```

**Recommendation:**
- Optimizer usually correct, but check statistics
- Use `STRAIGHT_JOIN` to force order (test first!)
- Ensure proper indexes on join columns

### 6. Dependent Subquery (HIGH)

**Detect when:**
```
select_type = "DEPENDENT SUBQUERY"
OR query re-executed for each outer row
```

**Recommendation:**
- Rewrite as JOIN
- Use EXISTS instead of IN for large outer sets
- Consider CTE (MySQL 8.0+) or temp table

See `references/rewrite-patterns.md` for examples.

### 7. Full Index Scan (MEDIUM)

**Detect when:**
```
access_type = "index" AND rows_examined_per_scan > 10000
```

**Recommendation:**
- Add WHERE conditions to enable range scan
- Create more selective index
- Consider query reformulation

### 8. Low Filtered Percentage (MEDIUM)

**Detect when:**
```
filtered < 10 (meaning >90% of rows discarded after fetch)
```

**Recommendation:**
- Add filtered columns to index
- Consider composite index with high-selectivity column first
- Review if condition can be pushed into index lookup

## Output Format

Structure your analysis response as follows:

```markdown
## Query Analysis Summary

**Overall Cost:** {query_cost}
**Primary Issue:** {most severe issue}
**Severity:** CRITICAL | HIGH | MEDIUM | LOW

## Issues Found

### 1. {Issue Title} ({Severity})

**Location:** `{table_name}` table
**Evidence:**
- access_type: {value}
- rows_examined: {value}
- {other relevant metrics}

**Impact:** {explanation of performance impact}

**Recommendation:** {specific action to take}

### 2. {Next Issue}...

## Recommended Indexes

```sql
-- For {issue description}
CREATE INDEX idx_name ON table (col1, col2);

-- For {another issue}
CREATE INDEX idx_name2 ON table (col3);
```

## Query Rewrite Suggestion

**Original pattern detected:** {pattern name}

**Suggested rewrite:**
```sql
-- Your optimized query here
```

**Expected improvement:** {explanation}
```

## Common Patterns Quick Reference

### Pattern: IN with Subquery → JOIN
```sql
-- Before (triggers DEPENDENT SUBQUERY)
SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE status = 'active');

-- After
SELECT o.* FROM orders o INNER JOIN customers c ON o.customer_id = c.id WHERE c.status = 'active';
```

### Pattern: NOT IN → NOT EXISTS / LEFT JOIN
```sql
-- Before (can't use index effectively)
SELECT * FROM orders WHERE customer_id NOT IN (SELECT id FROM blacklist);

-- After (uses index)
SELECT o.* FROM orders o LEFT JOIN blacklist b ON o.customer_id = b.id WHERE b.id IS NULL;
```

### Pattern: OR Conditions → UNION
```sql
-- Before (may cause full scan)
SELECT * FROM products WHERE category_id = 5 OR supplier_id = 10;

-- After (uses indexes on both columns)
SELECT * FROM products WHERE category_id = 5
UNION
SELECT * FROM products WHERE supplier_id = 10;
```

### Pattern: LIMIT with Large Offset → Keyset Pagination
```sql
-- Before (scans offset rows)
SELECT * FROM logs ORDER BY id LIMIT 1000000, 20;

-- After (uses index directly)
SELECT * FROM logs WHERE id > {last_seen_id} ORDER BY id LIMIT 20;
```

### Pattern: COUNT(*) with Conditions → Summary Table
```sql
-- Before (scans matching rows)
SELECT COUNT(*) FROM orders WHERE status = 'pending';

-- After (if frequently needed)
-- Maintain a summary table with triggers or application logic
SELECT pending_count FROM order_summary WHERE id = 1;
```

## Cost Analysis Guidelines

### Reading Cost Values
- `query_cost`: Total estimated cost (relative units)
- `read_cost`: I/O cost for reading rows
- `eval_cost`: CPU cost for evaluating conditions

### Cost Interpretation
| Cost Range | Interpretation |
|------------|----------------|
| < 100 | Excellent, likely uses indexes well |
| 100-1000 | Good for small-medium tables |
| 1000-10000 | Review for optimization opportunities |
| > 10000 | Likely needs index or query optimization |

### Cost Caveats
- Costs are estimates, not actual execution time
- Compare costs between query variations
- High cost on small result set = inefficient access path

## Verification Steps

After implementing optimizations:

1. **Recreate EXPLAIN** - Verify access_type improved
2. **Check key usage** - Confirm new index is used
3. **Compare costs** - Query cost should decrease
4. **Test with real data** - Run with `SET profiling = 1`
5. **Monitor production** - Use slow query log

```sql
-- Enable profiling for current session
SET profiling = 1;

-- Run your query
SELECT ...;

-- View execution details
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;
```

## MySQL 5.7 Specific Notes

- No window functions (use variables or subqueries)
- No CTEs (use derived tables or temp tables)
- JSON functions available but limited
- Consider upgrading path to 8.0 for chronic optimization issues
- `optimizer_switch` settings can affect plan choices

## References

- `references/access-types.md` - Detailed access type explanations
- `references/rewrite-patterns.md` - Complete query rewrite examples
