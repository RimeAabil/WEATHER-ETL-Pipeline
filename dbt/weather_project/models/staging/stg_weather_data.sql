/*
Staging = The first layer of data transformation where you clean and standardize raw data.
Raw Data (messy)  →  Staging (cleaned)  →  Marts (business ready)
*/

{{
    config(
        materialized='table',
        unique_key='id',
        schema='staging'
    )
}}

with source as (
    select * 
    from {{ source('raw', 'raw_weather_data') }}
),

de_dup as (
    select * ,
        row_number() over (
            partition by time 
            order by inserted_at desc
        ) as rn
    from source
)


select 
    id,
    city,
    temperature,
    weather_descriptions,
    wind_speed,
    time as weather_time_local,
    inserted_at,
    utc_offset,
    -- Convert inserted_at to local time using utc_offset (fixed typo)
    -- Note: utc_offset is stored as text like '+01:00', we need to handle it properly
    case 
        when utc_offset is not null 
        then inserted_at + (utc_offset || '')::interval
        else inserted_at
    end as inserted_at_local
from de_dup
where time is not null  and rn = 1  -- Data quality: exclude records without timestamps and keep only the most recent record for each time value