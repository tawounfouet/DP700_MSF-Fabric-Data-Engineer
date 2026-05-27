-- Requetes SQL pour le SQL analytics endpoint du lakehouse lh_books_toscrape.
-- Executer apres nb_03_build_books_gold.

-- 1. Apercu du catalogue gold
SELECT TOP 20
    title,
    category,
    price_gbp,
    rating_value,
    is_available
FROM gold_book_catalog
ORDER BY price_gbp DESC;

-- 2. Nombre de livres et prix moyen par categorie
SELECT
    category,
    book_count,
    avg_price_gbp,
    avg_rating,
    available_books,
    availability_rate
FROM gold_category_stats
ORDER BY book_count DESC;

-- 3. Distribution des notes
SELECT
    rating_value,
    COUNT(*) AS book_count,
    CAST(AVG(price_gbp) AS DECIMAL(10,2)) AS avg_price_gbp
FROM gold_book_catalog
GROUP BY rating_value
ORDER BY rating_value;

-- 4. Categories avec note moyenne elevee
SELECT TOP 10
    category,
    book_count,
    avg_rating,
    avg_price_gbp
FROM gold_category_stats
WHERE book_count >= 5
ORDER BY avg_rating DESC, book_count DESC;

-- 5. Livres chers et bien notes
SELECT TOP 20
    title,
    category,
    price_gbp,
    rating_value,
    source_url
FROM gold_book_catalog
WHERE rating_value >= 4
ORDER BY price_gbp DESC;

-- 6. Controle simple de coherence entre silver et gold
SELECT 'silver_books' AS table_name, COUNT(*) AS row_count FROM silver_books
UNION ALL
SELECT 'gold_book_catalog' AS table_name, COUNT(*) AS row_count FROM gold_book_catalog
UNION ALL
SELECT 'fact_books_gold' AS table_name, COUNT(*) AS row_count FROM fact_books_gold;

-- 7. Derniers controles qualite
SELECT TOP 20
    run_ts_utc,
    check_name,
    severity,
    passed,
    metric_value,
    details
FROM dq_results
ORDER BY run_ts_utc DESC, severity, check_name;

