{{ config(materialized='table') }}

-- mart_weather_daily : agrégations météo journalières par ville
-- Matérialisé en TABLE → données pré-calculées

with daily_stats as (
    select
        ingestion_date,
        city,
        country,

        round(avg(temperature_celsius), 2)  as temp_avg_c,
        round(min(temperature_celsius), 2)  as temp_min_c,
        round(max(temperature_celsius), 2)  as temp_max_c,
        round(avg(humidity_percent), 1)     as humidity_avg_pct,
        round(avg(wind_speed_kmh), 1)       as wind_avg_kmh,
        round(sum(precipitation_mm), 2)     as precipitation_total_mm,
        count(*)                            as nb_mesures

    from {{ ref('stg_weather') }}
    group by 1, 2, 3
)

select * from daily_stats
order by ingestion_date desc, city