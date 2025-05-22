CREATE FUNCTION SupplyChain.fn_CustomerInfoData (@customerid INT)
RETURNS TABLE
AS RETURN
SELECT * FROM SupplyChain.DimCustomers 
WHERE CustomerID = @customerid
;