CREATE TABLE [SupplyChain].[IngestionLogs] (

	[PipelineName] varchar(100) NULL, 
	[ProcessedTime] datetime2(3) NULL, 
	[Status] varchar(100) NULL, 
	[RowsProcessed] int NULL
);