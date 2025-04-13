-- Views for Metabase dashboards
-- View for ticket statistics by product
CREATE OR REPLACE VIEW ticket_stats_by_product AS
SELECT
    product_purchased,
    COUNT(*) AS total_tickets,
    SUM(
        CASE WHEN ticket_status = 'Closed' THEN
            1
        ELSE
            0
        END) AS closed_tickets,
    SUM(
        CASE WHEN ticket_status = 'Open' THEN
            1
        ELSE
            0
        END) AS open_tickets,
    SUM(
        CASE WHEN ticket_status = 'Pending Customer Response' THEN
            1
        ELSE
            0
        END) AS pending_tickets,
    AVG(
        CASE WHEN customer_satisfaction_rating IS NOT NULL THEN
            customer_satisfaction_rating
        ELSE
            NULL
        END) AS avg_satisfaction,
    COUNT(
        CASE WHEN customer_satisfaction_rating IS NOT NULL THEN
            1
        ELSE
            NULL
        END) AS rated_tickets
FROM
    customer_tickets
GROUP BY
    product_purchased
ORDER BY
    total_tickets DESC;

-- View for ticket statistics by channel
CREATE OR REPLACE VIEW ticket_stats_by_channel AS
SELECT
    ticket_channel,
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT customer_email) AS unique_customers,
    SUM(
        CASE WHEN ticket_status = 'Closed' THEN
            1
        ELSE
            0
        END) AS closed_tickets,
    AVG(
        CASE WHEN customer_satisfaction_rating IS NOT NULL THEN
            customer_satisfaction_rating
        ELSE
            NULL
        END) AS avg_satisfaction
FROM
    customer_tickets
GROUP BY
    ticket_channel
ORDER BY
    total_tickets DESC;

-- View for ticket priority distribution
CREATE OR REPLACE VIEW ticket_priority_distribution AS
SELECT
    ticket_priority,
    COUNT(*) AS ticket_count,
    ROUND((COUNT(*) * 100.0 / (
            SELECT
                COUNT(*)
            FROM customer_tickets)), 2) AS percentage
FROM
    customer_tickets
GROUP BY
    ticket_priority
ORDER BY
    ticket_count DESC;

-- View for ticket age (open tickets)
CREATE OR REPLACE VIEW open_ticket_age AS
SELECT
    ticket_id,
    customer_name,
    product_purchased,
    ticket_subject,
    ticket_priority,
    ticket_channel,
    first_response_time,
    CURRENT_TIMESTAMP - first_response_time AS ticket_age,
    ticket_status
FROM
    customer_tickets
WHERE
    ticket_status IN ('Open', 'Pending Customer Response')
ORDER BY
    ticket_age DESC;

CREATE OR REPLACE VIEW resolution_time_stats AS
SELECT
    ticket_priority,
    COUNT(*) AS closed_tickets,
    AVG(EXTRACT(EPOCH FROM (time_to_resolution - first_response_time)) / 3600) FILTER (WHERE time_to_resolution > first_response_time) AS avg_hours_to_resolve,
    MIN(EXTRACT(EPOCH FROM (time_to_resolution - first_response_time)) / 3600) FILTER (WHERE time_to_resolution > first_response_time) AS min_hours_to_resolve,
    MAX(EXTRACT(EPOCH FROM (time_to_resolution - first_response_time)) / 3600) FILTER (WHERE time_to_resolution > first_response_time) AS max_hours_to_resolve,
    COUNT(*) FILTER (WHERE time_to_resolution <= first_response_time) AS invalid_time_entries
FROM
    customer_tickets
WHERE
    ticket_status = 'Closed'
    AND first_response_time IS NOT NULL
    AND time_to_resolution IS NOT NULL
GROUP BY
    ticket_priority
ORDER BY
    ticket_priority;

-- View for customer demographics
CREATE OR REPLACE VIEW customer_demographics AS
SELECT
    CASE WHEN customer_age < 25 THEN
        '18-24'
    WHEN customer_age BETWEEN 25 AND 34 THEN
        '25-34'
    WHEN customer_age BETWEEN 35 AND 44 THEN
        '35-44'
    WHEN customer_age BETWEEN 45 AND 54 THEN
        '45-54'
    WHEN customer_age BETWEEN 55 AND 64 THEN
        '55-64'
    ELSE
        '65+'
    END AS age_group,
    customer_gender,
    COUNT(*) AS customer_count,
    AVG(
        CASE WHEN customer_satisfaction_rating IS NOT NULL THEN
            customer_satisfaction_rating
        ELSE
            NULL
        END) AS avg_satisfaction
FROM
    customer_tickets
GROUP BY
    age_group,
    customer_gender
ORDER BY
    age_group,
    customer_gender;

-- View for monthly ticket trends
CREATE OR REPLACE VIEW monthly_ticket_trends AS
SELECT
    DATE_TRUNC('month', first_response_time) AS month,
    COUNT(*) AS total_tickets,
    SUM(
        CASE WHEN ticket_status = 'Closed' THEN
            1
        ELSE
            0
        END) AS closed_tickets,
    AVG(
        CASE WHEN customer_satisfaction_rating IS NOT NULL THEN
            customer_satisfaction_rating
        ELSE
            NULL
        END) AS avg_satisfaction,
    COUNT(DISTINCT customer_email) AS unique_customers
FROM
    customer_tickets
WHERE
    first_response_time IS NOT NULL
GROUP BY
    month
ORDER BY
    month;

-- View for product purchase dates vs. ticket creation
CREATE OR REPLACE VIEW product_age_at_ticket AS
SELECT
    ticket_id,
    product_purchased,
    date_of_purchase,
    first_response_time::date AS ticket_date,
    first_response_time::date - date_of_purchase AS days_since_purchase
FROM
    customer_tickets
WHERE
    date_of_purchase IS NOT NULL
    AND first_response_time IS NOT NULL
ORDER BY
    days_since_purchase DESC;

-- View for ticket text analysis - common words in descriptions
CREATE OR REPLACE VIEW ticket_description_keywords AS
WITH words AS (
    SELECT
        ticket_id,
        regexp_split_to_table(lower(ticket_description), '\s+') AS word
    FROM
        customer_tickets
    WHERE
        ticket_description IS NOT NULL
),
filtered_words AS (
    SELECT
        word
    FROM
        words
    WHERE
        length(word) > 3
        AND word !~ '^[0-9]+$' 
        AND word NOT IN ('this', 'that', 'with', 'from', 'have', 'will', 'your', 'been', 'they', 'their', 'what', 'when', 'where', 'which', 'would', 'could', 'should'))
SELECT
    word,
    COUNT(*) AS frequency
FROM
    filtered_words
GROUP BY
    word
ORDER BY
    frequency DESC
LIMIT 50;

