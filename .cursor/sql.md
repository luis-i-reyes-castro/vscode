# SQL Code Style Guidelines

These rules apply to SQL files in any project unless a project-specific rule
overrides them.

## Project Structure

* Keep table definitions, functions, triggers, seed data, and feature queries
  in clearly named locations.
* Keep one focused query or DDL object per file unless the existing directory
  already groups related setup statements together.
* Preserve the current file organization. Add new query files near the code or
  feature area that will use them.
* Follow the migration policy of the current project. Do not assume direct DDL
  edits are acceptable unless the project explicitly allows rebuilds.

## Safety

* Do not invent tables, columns, enum values, functions, triggers, or workflows.
  Inspect existing schema files and calling code first.
* If a change needs a new table, column, enum, trigger, function, API route, or
  environment variable, propose the structure and ask before implementing.
* Prefer the smallest SQL change that preserves readability and existing
  behavior.
* Keep SQL and application parameter names in sync. If a SQL parameter changes,
  check the caller.
* Do not add broad data cleanup, destructive statements, or ad hoc migrations
  unless explicitly requested.

## Formatting

* Max line length: **92 characters** where practical.
* Prefer vertical readability over horizontal density.
* Use uppercase SQL keywords:
  `SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, `DELETE`, `RETURNING`,
  `UPSERT`, `CASE`, `WHEN`, `ELSE`, `END`.
* Put major clauses on their own lines.
* Put one selected column, inserted column, value, condition group, or returned
  column per line when there is more than one item.
* Align aliases, assignment operators, and related values when it improves scan
  speed.
* End executable statements with semicolons.
* Preserve blank lines and indentation that support vertical readability.
* Follow the repository trailing-whitespace rule:
  * trim non-empty edited lines;
  * leave whitespace-only blank lines untouched.

Example:

```sql
SELECT
  inv.id           AS id,
  inv.doc_type     AS doc_type,
  inv.sequence_num AS sequence_num,
  inv.access_key   AS access_key
FROM
  invoices AS inv
WHERE
  ( inv.business_id = @business_id ) AND
  ( inv.doc_type    = @doc_type    )
ORDER BY
  inv.branch_id    DESC,
  inv.terminal_id  DESC,
  inv.sequence_num ASC;
```

## Parameters

* Query files used by application code should start with a `-- PARAMS:` block.
* List every external parameter in that block.
* Use the same parameter names as the caller.
* Document the expected application/domain type, not only the SQL type.
* Use the placeholder syntax already used by the project:
  `@param_name`, `:param_name`, `?`, `$1`, or the local equivalent.
* Cast or convert parameters explicitly where the target SQL type matters and
  the current dialect supports it.
* Use project domain types when they exist.
* For optional text-like inputs that may arrive as empty strings, normalize
  with the dialect's `NULLIF` or equivalent before type conversion.

Example:

```sql
-- PARAMS:
  -- id_user      : UUID | None
  -- business_id  : str
  -- doc_type     : str
  -- sequence_num : str | None
```

## Query Style

* Prefer explicit table aliases for multi-table queries.
* Use short aliases that reflect the table name or existing convention.
* Qualify selected columns and `WHERE` columns when more than one table is
  involved.
* Prefer explicit `JOIN ... ON ...` over implicit joins.
* For double and triple joins, keep the table aliases and `ON` clauses aligned
  when the join condition fits on one line:

```sql
FROM
  orders         AS ord
JOIN
  customers      AS cus ON ord.customer_id = cus.id
LEFT JOIN
  reward_totals  AS rew ON rew.order_id    = ord.id
LEFT JOIN
  payment_totals AS pay ON pay.order_id    = ord.id
```

* Group boolean predicates with parentheses when combining `AND` and `OR`.
* Keep optional filters readable:

```sql
WHERE
  ( inv.business_id = @business_id ) AND
  (
    ( NULLIF( @status, '') IS NULL ) OR
    ( inv.status = NULLIF( @status, '') )
  )
```

* Prefer `RETURNING` for insert/update queries when the caller needs generated
  IDs or updated values and the dialect supports it.
* In upsert statements, keep update assignments in a vertical `SET` block.
* Use the dialect's inserted-row reference when the new value should come from
  the attempted insert.
* Use `COALESCE( @param, table.column )` only when `NULL` means "keep existing
  value"; do not use it when `NULL` is a meaningful update.

## DDL Style

* Keep standard row metadata near the top when the table has it:
  `id`, `created_at`, `updated_at`, `id_user`, or the local equivalent.
* Group related columns with short block comments when that improves scanning.
* Prefer project domain types, enums, or constrained types over raw strings when
  the current database supports them and they already exist.
* Name constraints explicitly and consistently:
  `table_pkey`, `table_fkey_column`, `table_unique`.
* Put primary keys, foreign keys, uniqueness, and check constraints in the table
  definition when practical.
* For foreign keys, specify `ON UPDATE` and `ON DELETE` behavior deliberately.
* Enable row-level security only for projects and tables that follow an existing
  RLS pattern.
* Keep triggers and functions in their existing project locations unless the
  surrounding DDL already uses a different local pattern.

## Stored Routines

* Keep function, procedure, and trigger declarations vertically expanded.
* Use clear prefixes for local variables, usually `v_` or the local convention.
* Prefer early explicit error checks for invalid state.
* Keep recursive CTEs and validation logic readable over compact.
* Return or mutate trigger rows explicitly according to the current dialect.

## Comments

* Use comments to explain business rules, state-dependent columns, or
  non-obvious constraints.
* Do not add comments that simply restate SQL syntax.
* Keep domain-specific names as-is when they match existing table, column, or
  business terminology.
