-- Auto Generated (Do not modify) 59CEECABE8562FF842B118CADC3B12B55A7239144D071C73439DFE67DAA0A608
CREATE VIEW SupplyChain.Staging_DimDates
AS 
SELECT DISTINCT DateID, Date, Year, Month, Day, MonthName, DayName
FROM LH_SupplyChain.dbo.dimdates;