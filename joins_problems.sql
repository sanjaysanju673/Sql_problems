
---@Author: v sanjay kumar
---@Date: 2024-08-25 10:00:30
---@Last Modified by: v sanjay kumar
---@Last Modified time: 2024-08-25 10:00:30
---@Title :JOins problems

use Covid_Test;

---1. To find out the population vs the number of people vaccinated


SELECT ROUND(
    (cv.Total_Doses_Administered * 100.0) / wd.MaxPopulation, 
    2
) AS vacine_percentage
FROM 
    (SELECT MAX(Population) AS MaxPopulation
     FROM worldometer_data 
     WHERE Continent = 'Asia') wd
join 
    (SELECT Total_Doses_Administered
     FROM covid_vaccine_statewisenew 
     WHERE STATE = 'India' 
     and Updated_On = (
         SELECT max(Updated_On)
         FROM covid_vaccine_statewisenew
         WHERE STATE = 'India' 
         and Total_Doses_Administered is not null
     )
     and Total_Doses_Administered is not null) cv
on 1=1;


---2. To find out the percentage of different vaccine taken by people in a country

select
    Updated_On as Date,
    State,
    Covaxin_Doses_Administered * 100.0 / Total_Doses_Administered as Covaxin_Percentage,
    CoviShield_Doses_Administered * 100.0 / Total_Doses_Administered as CoviShield_Percentage,
    Sputnik_V_Doses_Administered * 100.0 / Total_Doses_Administered as Sputnik_V_Percentage
from 
   covid_vaccine_statewisenew
order by date asc;


---3. To find out percentage of people who took both the doses

select
    covid_1.Updated_On as Date,
    covid_1.State,
    coalesce(covid_2.Second_Dose_Administered, 0) * 100.0 / coalesce(covid_1.First_Dose_Administered, 1) as Percentage_Both_Doses
from 
    covid_vaccine_statewisenew covid_1
join 
    covid_vaccine_statewisenew covid_2
on 
    covid_1.State = covid_2.State
    and covid_1.Updated_On = covid_2.Updated_On  
order by 
    covid_1.Updated_On asc;
