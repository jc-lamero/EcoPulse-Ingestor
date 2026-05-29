-- stg_weather : nettoyage des données météo brutes
-- Matérialisé en VIEW → recalculé à chaque requête

with source as (
    select * from {{ source('ecopulse_raw', 'weather') }}
),

renamed as (
    select
        city,
        country,
        cast(timestamp as timestamp)      as measured_at,
        cast(temperature_c as float64)    as temperature_celsius,
        cast(humidity_pct as float64)     as humidity_percent,
        cast(wind_speed_kmh as float64)   as wind_speed_kmh,
        cast(precipitation_mm as float64) as precipitation_mm,
        cast(weather_code as int64)       as weather_code,
        date(cast(timestamp as timestamp)) as ingestion_date
    from source
    where
        city is not null
        and temperature_c is not null
)

select * from renamed
