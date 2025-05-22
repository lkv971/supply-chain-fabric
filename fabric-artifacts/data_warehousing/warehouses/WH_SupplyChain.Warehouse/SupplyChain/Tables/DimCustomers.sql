CREATE TABLE [SupplyChain].[DimCustomers] (

	[CustomerID] int NULL, 
	[FirstName] varchar(200) NULL, 
	[LastName] varchar(200) NULL, 
	[State] varchar(10) NULL, 
	[Country] varchar(100) NULL, 
	[Segment] varchar(100) NULL, 
	[UniqueCustomerKey] varchar(200) NULL
);