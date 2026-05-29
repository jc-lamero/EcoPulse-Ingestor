{{ config(materialized='table') }}

-- mart_airquality_daily : agrégations quotidiennes de qualité de l'air par ville
-- Matérialisé en TABLE → données pré-calculées

with daily_stats as (
    select
        ingestion_date,
        city,
        country,

        round(avg(pm25_ugm3), 2)  as pm25_avg_ugm3,
        round(avg(pm10_ugm3), 2)  as pm10_avg_ugm3,
        round(avg(no2_ugm3), 2)   as no2_avg_ugm3,
        round(avg(aqi), 1)        as aqi_avg,
        max(aqi)                  as aqi_max,
        count(*)                  as nb_mesures

    from {{ ref('stg_airquality') }}
    group by ingestion_date, city, country
)

select * from daily_stats
order by ingestion_date desc, city

