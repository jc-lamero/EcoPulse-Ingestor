-- stg_airquality : nettoyage des données de qualité de l'air brutes
-- Matérialisé en VIEW → recalculé à chaque requête

with source as (
    select * from {{ source('ecopulse_raw', 'airquality') }}
),

renamed as (
    select
        city,
        country,
        cast(timestamp as timestamp)   as measured_at,
        cast(pm25 as float64)          as pm25_ugm3,
        cast(pm10 as float64)          as pm10_ugm3,
        cast(no2 as float64)           as no2_ugm3,
        cast(o3 as float64)            as o3_ugm3,
        cast(aqi as int64)             as aqi,
        date(cast(timestamp as timestamp)) as ingestion_date
    from source
    where
        city is not null
        and pm25 is not null
)

select * from renamed
