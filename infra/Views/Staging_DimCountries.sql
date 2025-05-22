-- Auto Generated (Do not modify) 413A03AB624D2541818E40DAD7903027B11AF8D7526967648BB771E1F1A7157D
CREATE VIEW SupplyChain.Staging_DimCountries
AS
SELECT DISTINCT CountryID, Country, Region, Market
FROM LH_SupplyChain.dbo.dimcountries;