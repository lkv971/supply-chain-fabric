-- Auto Generated (Do not modify) D574B94C2A1A98CEB5192DF2C04FB29C930CC8FAB6862B9E2590093CEE9241AF
CREATE VIEW SupplyChain.Staging_DimCustomers
AS
SELECT DISTINCT CustomerID, FirstName, LastName, State, Country, Segment, UniqueCustomerKey
FROM LH_SupplyChain.dbo.dimcustomers;