-- Auto Generated (Do not modify) D9844A10B0DC02CA4EEE17E139077CCE9AAD75D4A5D04146612914BF87E0B273
CREATE VIEW SupplyChain.Staging_DimCategories
AS 
SELECT DISTINCT CategoryID, CategoryName
FROM LH_SupplyChain.dbo.dimcategories;