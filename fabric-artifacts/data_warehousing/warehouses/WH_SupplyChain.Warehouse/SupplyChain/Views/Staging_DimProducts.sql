-- Auto Generated (Do not modify) FF8F1C9B70D45E61CE3E09517B7C7D1CEC072E1A217EFFC7FE5146B569D51129
CREATE VIEW SupplyChain.Staging_DimProducts
AS
SELECT DISTINCT ProductID, ProductName, CategoryID, DepartmentID, Price
FROM LH_SupplyChain.dbo.dimproducts;