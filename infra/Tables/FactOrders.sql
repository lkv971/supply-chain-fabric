CREATE TABLE [SupplyChain].[FactOrders] (

	[OrderID] int NULL, 
	[OrderDate] date NULL, 
	[CustomerID] int NULL, 
	[ProductID] int NULL, 
	[CountryID] int NULL, 
	[Discount] float NULL, 
	[Price] float NULL, 
	[Quantity] int NULL, 
	[Total] float NULL, 
	[TotalAfterDiscount] float NULL, 
	[Profit] float NULL, 
	[PaymentType] varchar(100) NULL, 
	[DaysForShipping] int NULL, 
	[DaysForShipment] int NULL, 
	[ShippingMode] varchar(100) NULL, 
	[LateDeliveryRisk] int NULL, 
	[DeliveryStatus] varchar(100) NULL, 
	[ShippingDate] date NULL, 
	[OnTimeShippingTarget] float NULL
);