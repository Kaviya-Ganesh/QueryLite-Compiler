# QueryLite Language Specification

QueryLite is a simple, custom, SQL-inspired query language designed for filtering, projecting, and sorting tabular data.

## Grammar (BNF)

```bnf
<query> ::= "PULL" <columns> "FROM" <identifier> [<filter_clause>] [<arrange_clause>] ";"

<columns> ::= "*" | <column_list>
<column_list> ::= <identifier> | <identifier> "," <column_list>

<filter_clause> ::= "FILTER" <identifier> <operator> <literal>

<arrange_clause> ::= "ARRANGE" "BY" <identifier> [<order>]
<order> ::= "ASC" | "DESC"

<operator> ::= ">" | "<" | "==" | "!=" | ">=" | "<="

<literal> ::= <number> | <string>
<identifier> ::= [a-zA-Z_]\w*
```

## Keywords
- `PULL`: Initiates the query and precedes projection columns.
- `FROM`: Precedes the table name.
- `FILTER`: Precedes the condition clause.
- `ARRANGE BY`: Precedes the sorting column name.
- `ASC`: Sort in ascending order (default).
- `DESC`: Sort in descending order.

## Operators
- `==`: Equals
- `!=`: Not Equal
- `>`: Greater Than
- `<`: Less Than
- `>=`: Greater Than or Equal
- `<=`: Less Than or Equal

## Example Queries

1. Select all columns from products:
   `PULL * FROM products;`

2. Select specific columns with a filter:
   `PULL name, price FROM products FILTER price < 500;`

3. Sort results in descending order:
   `PULL name, age FROM users ARRANGE BY age DESC;`

4. Filter and sort combined:
   `PULL name, age FROM users FILTER age > 21 ARRANGE BY age ASC;`

5. Exact match filter:
   `PULL name FROM users FILTER age == 22;`
