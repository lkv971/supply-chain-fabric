-- Auto Generated (Do not modify) B9E77B8449EE289EF25CD73B2AB27D5AFB2736629B1A4C41CCE08FDB790D5560
CREATE VIEW SupplyChain.Staging_FactShipments
AS 
SELECT DISTINCT ShipmentID, OrderID, ShippingDate, DaysForShipment, DaysForShipping, DeliveryStatus, LateDeliveryRisk, ShippingMode
FROM LH_SupplyChain.dbo.factshipments;