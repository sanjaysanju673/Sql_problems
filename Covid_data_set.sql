
---@Author: v sanjay kumar
---@Date: 2024-08-24 10:00:30
---@Last Modified by: v sanjay kumar
---@Last Modified time: 2024-08-24 10:00:30
---@Title :Covid problems


use Covid_Test;

---globaly death percentage

SELECT [Country Region], 
       ROUND((SUM(CAST(Deaths AS INT)) * 100.0) / SUM(CAST(Confirmed AS INT)), 4,2) AS Death_percentage
FROM country_wise_latest
GROUP BY [Country Region];


---locally death percentage

SELECT [State UnionTerritory], 
       ROUND((SUM(CAST(Deaths AS INT)) * 100.0) / SUM(CAST(Confirmed AS INT)), 4,2) AS Death_percentage
FROM covid_19_india
GROUP BY [State UnionTerritory]
ORDER BY [State UnionTerritory];



---the countries with the highest infection rates

SELECT [Country Region], 
       ROUND((CAST([Confirmed] AS FLOAT) / (SELECT SUM(CAST([Confirmed] AS FLOAT)) FROM country_wise_latest)) * 100, 2) AS Infection_Rate_Percentage
FROM country_wise_latest
GROUP BY [Country Region], [Confirmed], [Deaths], [Recovered], [Active], [New cases], [New deaths], [New recovered], [Deaths   100 Cases], [Recovered   100 Cases], [Deaths   100 Recovered], [Confirmed last week], [1 week change], [1 week % increase], [WHO Region]
ORDER BY Infection_Rate_Percentage DESC;


---The countries and continents with the highest death counts
SELECT [Country Region],[WHO Region], Deaths
FROM country_wise_latest
ORDER BY CAST(Deaths AS INT) DESC;




---5. Average number of deaths by day (Continents and Countries) 


SELECT [Country Region],[WHO Region],AVG(cast(deaths as int)) AS avg_daily_deaths
FROM full_grouped
GROUP BY [Country Region],[WHO Region];



---6. Average of cases divided by the number of population of each country (TOP 10)
SELECT TOP 10
    [Country_Region],
    CAST(Population AS FLOAT) AS Population,
    CAST(TotalCases AS FLOAT) AS TotalCases,
    CASE 
        WHEN CAST(Population AS FLOAT) = 0 THEN NULL
        ELSE CAST(TotalCases AS FLOAT) / CAST(Population AS FLOAT)
    END AS CasesPerPopulation
FROM
    worldometer_data
WHERE
    ISNUMERIC(Population) = 1
    AND ISNUMERIC(TotalCases) = 1
    AND CAST(Population AS FLOAT) <> 0
ORDER BY
    CasesPerPopulation DESC;



---7. Considering the highest value of total cases, which countries have the highest rate of infection in relation to population?
SELECT 
    [Country_Region],
    CAST(Population AS FLOAT) AS Population,
    CAST(TotalCases AS FLOAT) AS TotalCases,
    CASE 
        WHEN CAST(Population AS FLOAT) = 0 THEN NULL
        ELSE (CAST(TotalCases AS FLOAT)*10000)/ CAST(Population AS FLOAT)
    END AS infliation_rate
FROM
    worldometer_data
WHERE
    ISNUMERIC(Population) = 1
    and ISNUMERIC(TotalCases) = 1
    AND CAST(Population AS FLOAT) <> 0
ORDER BY
    infliation_rate DESC;




