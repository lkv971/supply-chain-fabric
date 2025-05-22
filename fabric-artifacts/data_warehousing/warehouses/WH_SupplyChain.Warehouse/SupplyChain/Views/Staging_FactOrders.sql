-- Auto Generated (Do not modify) F5F1FD5DA2FA6C4BD6C0FB788407E4C879AF7565B7C7796EA9FE6D69E1B526DE
CREATE VIEW SupplyChain.Staging_FactOrders
AS 
SELECT DISTINCT OrderID, OrderDate, CustomerID, ProductID, CountryID, Discount, Price, Quantity, Total, TotalAfterDiscount, Profit, PaymentType,
DaysForShipping, DaysForShipment, ShippingMode, LateDeliveryRisk, DeliveryStatus, ShippingDate, OnTimeShippingTarget
FROM LH_SupplyChain.dbo.factorders;