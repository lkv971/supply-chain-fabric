# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8da37622-ee8b-4e7f-aaa5-cb476238d60f",
# META       "default_lakehouse_name": "LH_SupplyChain",
# META       "default_lakehouse_workspace_id": "1493e9bf-f927-4698-9a67-289c6cecf55a",
# META       "known_lakehouses": [
# META         {
# META           "id": "8da37622-ee8b-4e7f-aaa5-cb476238d60f"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "default_warehouse": "8b54ceb3-9879-a5a0-4a65-e0cf5fb6540a",
# META       "known_warehouses": [
# META         {
# META           "id": "8b54ceb3-9879-a5a0-4a65-e0cf5fb6540a",
# META           "type": "Datawarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import *
from delta.tables import DeltaTable
import json 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

paths = {
   "supply_chain":
        "Files/raw_data/supply_chain_data.csv",
   "countries_es_eng": 
        "Files/raw_data/countries_es_eng.csv"
}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def read_csv(path_key: str):
    try:
        path = paths[path_key]
        df = spark.read.csv(path, header=True, sep = ",", encoding="UTF-8")

        clean_columns = [c.strip().replace("\uFEFF", "") for c in df.columns]
 
        print(f"Successfully read: {path_key}")
        return df
        
    except Exception as e:
        print(f"Error reading {path_key}: {str(e)}")
        raise

df_supply_chain = read_csv("supply_chain")
df_country_translation = read_csv("countries_es_eng")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

start_date = "20150101"
end_date   = "20301231"

df_date_range = spark.createDataFrame([(start_date, end_date)], ["start_date", "end_date"])
df_dates = df_date_range.select(
    explode(sequence(to_date(col("start_date"), "yyyyMMdd"),
                     to_date(col("end_date"), "yyyyMMdd"),
                     expr("interval 1 day"))).alias("Date"))

window_dates = Window.orderBy("Date")

df_dates = df_dates.withColumn("Year", year(col("Date"))) \
                   .withColumn("DateID", row_number().over(window_dates)) \
                   .withColumn("Month", month(col("Date"))) \
                   .withColumn("Day", dayofmonth(col("Date"))) \
                   .withColumn("MonthName", date_format(col("Date"), "MMMM")) \
                   .withColumn("DayName", date_format(col("Date"), "EEEE")) \
                   .select("DateID", "Date", "Year", "Month", "Day", "MonthName", "DayName") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

df_customers = df_supply_chain.withColumnRenamed("Customer Id", "CustomerID") \
                              .withColumnRenamed("Customer Fname", "FirstName") \
                              .withColumnRenamed("Customer Lname", "LastName") \
                              .withColumnRenamed("Customer State", "State") \
                              .withColumnRenamed("Customer Country", "Country") \
                              .withColumnRenamed("Customer Segment", "Segment")  \
                              .withColumn("Country", regexp_replace(col("Country"), "EE. UU.", "USA")) \
                              .withColumn("State", when(col("State") == 91732, "OR").otherwise(col("State"))) \
                              .withColumn("State", when(col("State") == 95758, "CA").otherwise(col("State"))) \
                              .withColumn("UniqueCustomerKey", concat(col("FirstName"), lit(" "), col("LastName"), lit(" "), col("CustomerID"))) \
                              .select(col("CustomerID").cast(IntegerType()),
                                      "FirstName", 
                                      "LastName", 
                                      "State", 
                                      "Country", 
                                      "Segment",
                                      "UniqueCustomerKey").distinct()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_departments = df_supply_chain.withColumnRenamed("Department Id", "DepartmentID") \
                                .withColumnRenamed("Department Name", "DepartmentName") \
                                .select(col("DepartmentID").cast(IntegerType()), 
                                        "DepartmentName").distinct()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_categories = df_supply_chain.withColumnRenamed("Category Id", "CategoryID") \
                               .withColumnRenamed("Category Name", "CategoryName") \
                               .withColumn("CategoryName", regexp_replace(col("CategoryName"), "!", "")) \
                               .select(col("CategoryID").cast(IntegerType()), 
                                       "CategoryName").distinct()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_products = df_supply_chain.withColumnRenamed("Product Card Id", "ProductID") \
                             .withColumnRenamed("Product Name", "ProductName") \
                             .withColumnRenamed("Category Id", "CategoryID") \
                             .withColumnRenamed("Department Id", "DepartmentID") \
                             .withColumnRenamed("Product Price", "Price") \
                             .select(col("ProductID").cast(IntegerType()),
                                     "ProductName",
                                     col("CategoryID").cast(IntegerType()),
                                     col("DepartmentID").cast(IntegerType()), 
                                     col("Price").cast(FloatType())).distinct()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_countries = df_supply_chain.withColumn("Order Country", translate(col("Order Country"), "áéíóúñàÁÉÍÓÚÑÀ", "aeiounaAEIOUNA")) \
                              .join(broadcast(df_country_translation), col("Order Country") == col("Spanish"), "left") \
                              .withColumn("Country", coalesce(col("English"), col("Order Country"))) \
                              .withColumn("Country", trim(col("Country"))) \
                              .withColumn("Region", trim(col("Order Region"))).withColumn("Market", trim(col("Market"))) \
                              .select("Country", "Region", "Market") \
                              .distinct() \
                              .withColumn("CountryID", row_number().over(Window.orderBy("Country", "Region", "Market")))

df_countries = df_countries["CountryID", "Country", "Region", "Market"] 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_orders = df_supply_chain.withColumn("Order Country", translate(col("Order Country"), "áéíóúñàÁÉÍÓÚÑÀ", "aeiounaAEIOUNA")) \
                   .join(broadcast(df_country_translation), col("Order Country") == col("Spanish"), "left") \
                   .withColumn("Country", coalesce(col("English"), col("Order Country"))) \
                   .withColumn("Country", trim(col("Country"))) \
                   .withColumn("Region", trim(col("Order Region"))) \
                   .withColumn("Market", trim(col("Market"))) \
                   .join(broadcast(df_countries.select("CountryID", "Country", "Region", "Market")),["Country", "Region", "Market"], "left") \
                   .withColumnRenamed("Order Id", "OrderID") \
                   .withColumnRenamed("Order Customer Id", "CustomerID") \
                   .withColumnRenamed("Order Item Cardprod Id", "ProductID") \
                   .withColumnRenamed("Order Item Discount", "Discount") \
                   .withColumnRenamed("Order Item Product Price", "Price") \
                   .withColumnRenamed("Order Item Quantity", "Quantity") \
                   .withColumnRenamed("Sales", "Total") \
                   .withColumnRenamed("Order Item Total", "TotalAfterDiscount") \
                   .withColumnRenamed("Order Profit Per Order", "Profit") \
                   .withColumnRenamed("Order Status", "OrderStatus") \
                   .withColumnRenamed("Days for shipping (real)", "DaysForShipping") \
                   .withColumnRenamed("Days for shipment (scheduled)", "DaysForShipment") \
                   .withColumnRenamed("Shipping Mode", "ShippingMode")\
                   .withColumnRenamed("Late_delivery_risk", "LateDeliveryRisk") \
                   .withColumnRenamed("Delivery Status", "DeliveryStatus")\
                   .withColumnRenamed("shipping date (DateOrders)", "ShippingDate") \
                   .withColumnRenamed("order date (DateOrders)", "OrderDate") \
                   .withColumnRenamed("Type", "PaymentType") \
                   .withColumn("OnTimeShippingTarget", lit(0.85)) \
                   .withColumn("ShippingDate", split(col("ShippingDate"), " ")[0]) \
                   .withColumn("OrderDate", split(col("Orderdate")," ")[0]) \
                   .withColumn("ShippingDate", to_date(col("ShippingDate"), "M/d/yyyy")) \
                   .withColumn("OrderDate", to_date(col("OrderDate"), "M/d/yyyy")) \
                   .filter(col("OrderStatus") == "COMPLETE") \
                   .select(col("OrderID").cast(IntegerType()),
                           "OrderDate", 
                           col("CustomerID").cast(IntegerType()), 
                           col("ProductID").cast(IntegerType()), 
                           col("CountryID").cast(IntegerType()), 
                           col("Discount").cast(DoubleType()), 
                           col("Price").cast(DoubleType()), 
                           col("Quantity").cast(IntegerType()), 
                           col("Total").cast(DoubleType()),
                           col("TotalAfterDiscount").cast(DoubleType()), 
                           col("Profit").cast(DoubleType()), 
                           "PaymentType", 
                           col("DaysForShipping").cast(IntegerType()), 
                           col("DaysForShipment").cast(IntegerType()), 
                           "ShippingMode",
                           col("LateDeliveryRisk").cast(IntegerType()), 
                           "DeliveryStatus", 
                           "ShippingDate", 
                            col("OnTimeShippingTarget").cast(DoubleType())) \
                 .filter(col("OrderStatus") == "COMPLETE") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customers = df_customers.dropDuplicates(subset=["CustomerID"])
df_products = df_products.dropDuplicates(subset=["ProductID"])
df_categories = df_categories.dropDuplicates(subset=["CategoryID"])
df_departments = df_departments.dropDuplicates(subset=["DepartmentID"])
df_countries = df_countries.dropDuplicates(subset=["CountryID"])
df_orders = df_orders.dropDuplicates()
df_dates = df_dates.dropDuplicates(subset=["DateID"])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

rows_processed = {
    "dimcustomers": df_customers.count(),
    "dimproducts": df_products.count(),
    "dimcategories": df_categories.count(),
    "dimdepartments": df_departments.count(),
    "dim_countries" : df_countries.count(),
    "dim_dates": df_dates.count(),
    "fact_orders": df_orders.count()
    }

total_rows_processed = __builtins__.sum(rows_processed.values())
print(f"Total Rows Processed: {total_rows_processed}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

append_tables = {
    "factorders": df_orders
}
overwrite_tables = {
    "dimcustomers": df_customers,
    "dimproducts": df_products,
    "dimcategories": df_categories,
    "dimdepartments": df_departments,
    "dimcountries": df_countries,
    "dimdates": df_dates
}

key_cols = ["OrderDate", "ShippingDate", "CustomerID", "ProductID", "CountryID"]

def make_merge_condition(keys):
    return " AND ".join([f"t.{c} = s.{c}" for c in keys])

for table_name, append_df in append_tables.items():
    try:
        target = DeltaTable.forName(spark, table_name)
        condition = make_merge_condition(key_cols)
        (target.alias("t").merge(append_df.alias("s"), condition).whenNotMatchedInsertAll().execute())
        print(f"Table {table_name} upserted successfully using key: {key_cols}")
    except Exception as e:
        if "is not a Delta table" in e.desc:
            append_df.write.mode("overwrite").saveAsTable(f"{table_name}")
            print(f"Created new Delta table {table_name}")
        else:
            print(f"Error upserting '{table_name}': {e}")
            
for table_name, overwrite_df in overwrite_tables.items():
    try:
        overwrite_df.write.mode("overwrite").saveAsTable(f"{table_name}")
        print(f"Tables {table_name} overwritten successfully")
    except Exception as e:
        print(f"Overwritting error at {table_name}:{e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

mssparkutils.notebook.exit(json.dumps({
    "status": "succeeded",
    "RowsProcessed": total_rows_processed
}))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }
