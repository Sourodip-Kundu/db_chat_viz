# example = [
# {
#     "input": "What is the average price per commodity over the last 10 days?",
#     "query": "SELECT source_commodity_name, AVG(value) as average_price \
#                 FROM lighthouse.lighthouse_last ll \
#                 WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' \
#                 GROUP BY source_commodity_name;"
# },

# {
#     "input": "What are the daily price movements for Benzene in the last 10 days?",
#     "query": "SELECT date, value FROM data_table WHERE source_commodity_name LIKE '%Benzene%' AND date >= CURDATE() - INTERVAL 10 DAY ORDER BY date;"
# },

# {
#     "input": "What is the most recent price of each commodity?",
#     "query": "SELECT source_commodity_name, value FROM data_table WHERE (source_commodity_name, update_datetime) IN (SELECT source_commodity_name, MAX(update_datetime) FROM data_table GROUP BY source_commodity_name);"
# },

# {
#     "input": "How do prices compare across different benchmarks?",
#     "query": "SELECT benchmark, source_commodity_name, AVG(value) as average_price FROM data_table GROUP BY benchmark, source_commodity_name;"
# },

# {
#     "input": "How frequently are prices updated per month for each commodity?",
#     "query": "SELECT source_commodity_name, COUNT(*) as update_count FROM data_table WHERE frequency='monthly' GROUP BY source_commodity_name;"
# },

# {
#     "input": "What are the price trends for commodities reported from the web?",
#     "query": "SELECT date, source_commodity_name, value FROM data_table WHERE source='WEB' ORDER BY date, source_commodity_name;"
# },

# {
#     "input": "Show me the last 10 days data trend",
#     "query": "SELECT date, source_commodity_name, value FROM data_table WHERE date >= CURDATE() - INTERVAL 10 DAY ORDER BY date, source_commodity_name;"
# },

# {
#     "input": "What are the maximum and minimum price fluctuations for each commodity over the last 10 days?",
#     "query": "SELECT source_commodity_name, MAX(value) as max_price, MIN(value) as min_price FROM data_table WHERE date >= CURDATE() - INTERVAL 10 DAY GROUP BY source_commodity_name;"
# },

# {
#     "input": "Which commodities have shown the highest price volatility over the last 10 days?",
#     "query": "SELECT source_commodity_name, (MAX(value) - MIN(value)) as price_volatility FROM data_table WHERE date >= CURDATE() - INTERVAL 10 DAY GROUP BY source_commodity_name ORDER BY price_volatility DESC;"
# },

# {
#     "input": "Compare the daily average prices between the first and last 10 days of the dataset.",
#     "query": "WITH First_Period AS (SELECT source_commodity_name, AVG(value) as avg_price FROM data_table WHERE date <= (SELECT MIN(date) FROM data_table) + INTERVAL 9 DAY GROUP BY source_commodity_name), Last_Period AS (SELECT source_commodity_name, AVG(value) as avg_price FROM data_table WHERE date >= (SELECT MAX(date) FROM data_table) - INTERVAL 9 DAY GROUP BY source_commodity_name) SELECT a.source_commodity_name, a.avg_price as First_Period_Avg, b.avg_price as Last_Period_Avg FROM First_Period a JOIN Last_Period b ON a.source_commodity_name = b.source_commodity_name;"
# },

# {
#     "input": "How many price updates have there been for each benchmark?",
#     "query": "SELECT benchmark, COUNT(*) as updates_count FROM data_table GROUP BY benchmark;"
# },

# {
#     "input": "Identify any outlier prices for commodities over the last 10 days.",
#     "query": "SELECT source_commodity_name, date, value \
#                 FROM lighthouse.lighthouse_last ll\
#                 WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' \
#                 AND (\
#                     value > (\
#                         SELECT AVG(value) + 3 * STDDEV(value) \
#                         FROM lighthouse.lighthouse_last \
#                         WHERE source_commodity_name = ll.source_commodity_name\
#                     ) \
#                     OR \
#                     value < (\
#                         SELECT AVG(value) - 3 * STDDEV(value) \
#                         FROM lighthouse.lighthouse_last \
#                         WHERE source_commodity_name = ll.source_commodity_name\
#                     )\
#                 );\
#                 "
# }
# ]

example = [
    {
        "input": "What is the average price per commodity over the last 10 days?",
        "query": "SELECT source_commodity_name, AVG(value) as average_price FROM lighthouse.lighthouse_last ll WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' GROUP BY source_commodity_name;"
    },
    {
        "input": "What are the daily price movements for Benzene in the last 10 days?",
        "query": "SELECT date, value FROM lighthouse.lighthouse_last WHERE source_commodity_name LIKE '%Benzene%' AND date::date >= CURRENT_DATE - INTERVAL '10 days' ORDER BY date::date;"
    },
    {
        "input": "What is the most recent price of each commodity?",
        "query": "SELECT source_commodity_name, value FROM lighthouse.lighthouse_last WHERE (source_commodity_name, update_datetime) IN (SELECT source_commodity_name, MAX(update_datetime) FROM lighthouse.lighthouse_last GROUP BY source_commodity_name);"
    },
    {
        "input": "How do prices compare across different benchmarks?",
        "query": "SELECT benchmark, source_commodity_name, AVG(value) as average_price FROM lighthouse.lighthouse_last GROUP BY benchmark, source_commodity_name;"
    },
    {
        "input": "How frequently are prices updated per month for each commodity?",
        "query": "SELECT source_commodity_name, COUNT(*) as update_count FROM lighthouse.lighthouse_last WHERE frequency='monthly' GROUP BY source_commodity_name;"
    },
    {
        "input": "What are the price trends for commodities reported from the web?",
        "query": "SELECT date, source_commodity_name, value FROM lighthouse.lighthouse_last WHERE source='WEB' ORDER BY date::date, source_commodity_name;"
    },
    {
        "input": "Show me the last 10 days data trend",
        "query": "SELECT date, source_commodity_name, value FROM lighthouse.lighthouse_last WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' ORDER BY date::date, source_commodity_name;"
    },
    {
        "input": "What are the maximum and minimum price fluctuations for each commodity over the last 10 days?",
        "query": "SELECT source_commodity_name, MAX(value) as max_price, MIN(value) as min_price FROM lighthouse.lighthouse_last WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' GROUP BY source_commodity_name;"
    },
    {
        "input": "Which commodities have shown the highest price volatility over the last 10 days?",
        "query": "SELECT source_commodity_name, (MAX(value) - MIN(value)) as price_volatility FROM lighthouse.lighthouse_last WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' GROUP BY source_commodity_name ORDER BY price_volatility DESC;"
    },
    {
        "input": "Compare the daily average prices between the first and last 10 days of the dataset.",
        "query": "WITH First_Period AS (SELECT source_commodity_name, AVG(value) as avg_price FROM lighthouse.lighthouse_last WHERE date::date <= (SELECT MIN(date::date) FROM lighthouse.lighthouse_last) + INTERVAL '9 days' GROUP BY source_commodity_name), Last_Period AS (SELECT source_commodity_name, AVG(value) as avg_price FROM lighthouse.lighthouse_last WHERE date::date >= (SELECT MAX(date::date) FROM lighthouse.lighthouse_last) - INTERVAL '9 days' GROUP BY source_commodity_name) SELECT a.source_commodity_name, a.avg_price as First_Period_Avg, b.avg_price as Last_Period_Avg FROM First_Period a JOIN Last_Period b ON a.source_commodity_name = b.source_commodity_name;"
    },
    {
        "input": "How many price updates have there been for each benchmark?",
        "query": "SELECT benchmark, COUNT(*) as updates_count FROM lighthouse.lighthouse_last GROUP BY benchmark;"
    },
    {
        "input": "Identify any outlier prices for commodities over the last 10 days.",
        "query": "SELECT source_commodity_name, date, value FROM lighthouse.lighthouse_last ll WHERE date::date >= CURRENT_DATE - INTERVAL '10 days' AND (value > (SELECT AVG(value) + 3 * STDDEV(value) FROM lighthouse.lighthouse_last WHERE source_commodity_name = ll.source_commodity_name) OR value < (SELECT AVG(value) - 3 * STDDEV(value) FROM lighthouse.lighthouse_last WHERE source_commodity_name = ll.source_commodity_name));"
    }
]

