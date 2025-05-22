CREATE FUNCTION SupplyChain.fn_AverageShippingTimeByCountry(@Country VARCHAR(200))
RETURNS TABLE
AS 
RETURN
(SELECT c.Country,AVG(o.DaysForShipping) AS AverageShippingTime
FROM SupplyChain.FactOrders AS o
JOIN SupplyChain.DimCustomers AS c
    ON o.CustomerID = c.CustomerID
WHERE c.Country = @Country
GROUP BY c.Country);