-- Requetes SQL pour le SQL analytics endpoint du lakehouse lh_sales_medallion.

-- 1. Chiffre d'affaires par an
SELECT
    d.Year,
    CAST(SUM(f.LineAmount) AS DECIMAL(14,2)) AS TotalRevenue,
    SUM(f.Quantity) AS TotalQuantity,
    COUNT(DISTINCT f.SalesOrderNumber) AS OrderCount
FROM factsales_gold AS f
JOIN dimdate_gold AS d
    ON f.DateKey = d.DateKey
GROUP BY d.Year
ORDER BY d.Year;

-- 2. Chiffre d'affaires par mois
SELECT
    d.YearMonth,
    CAST(SUM(f.LineAmount) AS DECIMAL(14,2)) AS TotalRevenue,
    SUM(f.Quantity) AS TotalQuantity
FROM factsales_gold AS f
JOIN dimdate_gold AS d
    ON f.DateKey = d.DateKey
GROUP BY d.YearMonth
ORDER BY d.YearMonth;

-- 3. Top produits
SELECT TOP 20
    p.ProductName,
    p.ProductVariant,
    CAST(SUM(f.LineAmount) AS DECIMAL(14,2)) AS TotalRevenue,
    SUM(f.Quantity) AS TotalQuantity
FROM factsales_gold AS f
JOIN dimproduct_gold AS p
    ON f.ProductID = p.ProductID
GROUP BY p.ProductName, p.ProductVariant
ORDER BY TotalRevenue DESC;

-- 4. Top clients
SELECT TOP 20
    c.CustomerName,
    c.Email,
    CAST(SUM(f.LineAmount) AS DECIMAL(14,2)) AS TotalRevenue,
    COUNT(DISTINCT f.SalesOrderNumber) AS OrderCount
FROM factsales_gold AS f
JOIN dimcustomer_gold AS c
    ON f.CustomerID = c.CustomerID
GROUP BY c.CustomerName, c.Email
ORDER BY TotalRevenue DESC;

-- 5. Controle de volumes
SELECT 'bronze_sales_orders' AS table_name, COUNT(*) AS row_count FROM bronze_sales_orders
UNION ALL
SELECT 'silver_sales_orders' AS table_name, COUNT(*) AS row_count FROM silver_sales_orders
UNION ALL
SELECT 'factsales_gold' AS table_name, COUNT(*) AS row_count FROM factsales_gold;

-- 6. Derniers controles qualite
SELECT TOP 20
    run_ts_utc,
    check_name,
    severity,
    passed,
    metric_value,
    details
FROM dq_sales_results
ORDER BY run_ts_utc DESC, severity, check_name;

