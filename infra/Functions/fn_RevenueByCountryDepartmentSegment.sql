CREATE FUNCTION SupplyChain.fn_RevenueByCountryDepartmentSegment(@Country VARCHAR(200) = NULL, @Year INT = NULL, @Month INT = NULL)
RETURNS TABLE
AS RETURN
(SELECT d.DepartmentName, c.Segment, SUM(o.TotalAfterDiscount) AS TotalRevenue
FROM SupplyChain.DimProducts AS p
JOIN SupplyChain.DimDepartments AS d
    ON p.DepartmentID = d.DepartmentID
JOIN SupplyChain.FactOrders AS o 
    ON p.ProductID = o.ProductID
JOIN DimCustomers AS c
    ON c.CustomerID = o.CustomerID
JOIN DimCountries AS co 
    ON co.CountryID = o.CountryID
WHERE (@Country IS NULL OR co.Country = @Country)
    AND (@Year IS NULL OR YEAR(o.OrderDate) = @Year)
    AND (@Month IS NULL OR  MONTH(o.OrderDate) = @Month)
GROUP BY d.DepartmentName, c.Segment);