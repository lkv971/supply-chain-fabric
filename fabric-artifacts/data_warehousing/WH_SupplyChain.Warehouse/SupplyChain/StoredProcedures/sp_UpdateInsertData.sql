CREATE PROCEDURE SupplyChain.sp_UpdateInsertData 
AS
BEGIN
    UPDATE SCA
    SET
       SCA.CategoryName = SSCA.CategoryName
    FROM SupplyChain.DimCategories AS SCA
    INNER JOIN SupplyChain.Staging_DimCategories AS SSCA 
        ON SCA.CategoryID = SSCA.CategoryID
    WHERE SCA.CategoryName <> SSCA.CategoryName
    ;

    INSERT INTO SupplyChain.DimCategories (
            CategoryID, CategoryName)
    SELECT SSCA.CategoryID, SSCA.CategoryName 
    FROM SupplyChain.Staging_DimCategories AS SSCA 
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimCategories AS SCA 
        WHERE SCA.CategoryID = SSCA.CategoryID
    );


    UPDATE SD 
    SET
        SD.DepartmentName = SSD.DepartmentName
    FROM SupplyChain.DimDepartments AS SD
    INNER JOIN SupplyChain.Staging_DimDepartments AS SSD
        ON SD.DepartmentID = SSD.DepartmentID
    WHERE SD.DepartmentName <> SSD.DepartmentName
    ;

    INSERT INTO SupplyChain.DimDepartments (
            DepartmentID, DepartmentName)
    SELECT SSD.DepartmentID, SSD.DepartmentName
    FROM SupplyChain.Staging_DimDepartments AS SSD
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimDepartments AS SD
        WHERE SD.DepartmentID = SSD.DepartmentID
    );
        
    
    UPDATE SC
    SET 
        SC.FirstName = SSC.FirstName,
        SC.LastName = SSC.LastName,
        SC.State = SSC.State,
        SC.Country = SSC.Country,
        SC.Segment = SSC.Segment,
        SC.UniqueCustomerKey = SSC.UniqueCustomerKey
    FROM SupplyChain.DimCustomers AS SC
    INNER JOIN SupplyChain.Staging_DimCustomers AS SSC
        ON SC.CustomerID = SSC.CustomerID
    WHERE SC.FirstName <> SSC.FirstName
         OR SC.LastName <> SSC.LastName
         OR SC.State <> SSC.State
         OR SC.Country <> SSC.Country
         OR SC.Segment <> SSC.Segment
         OR SC.UniqueCustomerKey <> SSC.UniqueCustomerKey
    ;

    INSERT INTO SupplyChain.DimCustomers (
          CustomerID, FirstName, LastName, State, Country, Segment, UniqueCustomerKey)
    SELECT SSC.CustomerID, SSC.FirstName, SSC.LastName, SSC.State, SSC.Country, SSC.Segment, SSC.UniqueCustomerKey
    FROM SupplyChain.Staging_DimCustomers AS SSC
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimCustomers AS SC
        WHERE SC.CustomerID = SSC.CustomerID
     );


    UPDATE SP
    SET
        SP.ProductName = SSP.ProductName,
        SP.CategoryID = SSP.CategoryID,
        SP.DepartmentID = SSP.DepartmentID
    FROM SupplyChain.DimProducts AS SP
    INNER JOIN SupplyChain.Staging_DimProducts AS SSP
        ON SP.ProductID = SSP.ProductID
    WHERE SP.ProductName <> SSP.ProductName
          OR SP.CategoryID <> SSP.CategoryID
          OR SP.DepartmentID <> SSP.DepartmentID
     ;

    INSERT INTO SupplyChain.DimProducts (
           ProductID, ProductName, CategoryID, DepartmentID, Price)
    SELECT SSP.ProductID, SSP.ProductName, SSP.CategoryID, SSP.DepartmentID, SSP.Price
    FROM SupplyChain.Staging_DimProducts AS SSP
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimProducts AS SP
        WHERE SP.ProductID = SSP.ProductID
    );

    
    UPDATE SCO
    SET
        SCO.Country = SSCO.Country,
        SCO.Region = SSCO.Region,
        SCO.Market = SSCO.Market
    FROM SupplyChain.DimCountries AS SCO
    INNER JOIN SupplyChain.Staging_DimCountries AS SSCO
        ON SCO.CountryID = SSCO.CountryID
    WHERE  SCO.Country <> SSCO.Country
        OR SCO.Region <> SSCO.Region
        OR SCO.Market <> SSCO.Market
    ;

    INSERT INTO SupplyChain.DimCountries (
           CountryID, Country, Region, Market)
    SELECT SSCO.CountryID, SSCO.Country, SSCO.Region, SSCO.Market
    FROM SupplyChain.Staging_DimCountries AS SSCO
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimCountries AS SCO
        WHERE SCO.CountryID = SSCO.CountryID
    );


    INSERT INTO SupplyChain.DimDates (DateID, Date, Year, Month, Day, MonthName, DayName)
    SELECT SSD.DateID, SSD.Date, SSD.Year, SSD.Month, SSD.Day, SSD.MonthName, SSD.DayName
    FROM SupplyChain.Staging_DimDates AS SSD
    WHERE NOT EXISTS (
        SELECT 1
        FROM SupplyChain.DimDates AS SD
        WHERE SD.DateID = SSD.DateID
        );

   
    INSERT INTO SupplyChain.FactOrders (
           OrderID, OrderDate, CustomerID, ProductID, CountryID, Discount, Price, Quantity, Total, TotalAfterDiscount, Profit, PaymentType,
           DaysForShipping, DaysForShipment, ShippingMode, LateDeliveryRisk, DeliveryStatus, ShippingDate, OnTimeShippingTarget)
    SELECT SSO.OrderID, SSO.OrderDate, SSO.CustomerID, SSO.ProductID, SSO.CountryID, SSO.Discount, SSO.Price, SSO.Quantity, SSO.Total, SSO.TotalAfterDiscount, SSO.Profit, SSO.PaymentType,
           SSO.DaysForShipping, SSO.DaysForShipment, SSO.ShippingMode, SSO.LateDeliveryRisk, SSO.DeliveryStatus, SSO.ShippingDate, SSO.OnTimeShippingTarget
    FROM SupplyChain.Staging_FactOrders AS SSO
    WHERE NOT EXISTS (
            SELECT 1
            FROM SupplyChain.FactOrders AS SO
            WHERE SO.OrderID = SSO.OrderID
                AND SO.OrderDate = SSO.OrderDate
                AND SO.CustomerID = SSO.CustomerID
                AND SO.ProductID = SSO.ProductID
                AND SO.CountryID = SSO.CountryID
                AND SO.ShippingDate = SSO.ShippingDate
        );
    
END;