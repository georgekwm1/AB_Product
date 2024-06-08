import sqlite3 as sql
import csv
import os

class SQLiteEngine():
    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name
        

    # Connect to the database
        try:
            self.conn = sql.connect(self.db_name)
            print("Opened database successfully")
        except sql.Error as e:
            print(e)
     
    #Methods  
    def listtables(self):
        """Lists the tables  in the currently opened database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_schema WHERE type='table'")
        rows = cursor.fetchall()
        print("Tables in Database : ") 
        for row in rows:
            print (row[0])

    def listcolumns(self):
        """Lists the columns in the table passed as argument"""
        prompt = input("Enter the table name: ")
        query = f"PRAGMA table_info({prompt})"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row[1])
        
    def search(self, output):
        """Searches a given term within all columns of all tables"""
        cursor = self.conn.cursor()
        #output = input("Type your search query: ")
        if output == "":
            print("\nPlease enter a valid product")
        elif output.isdigit():
            query = f"""SELECT * FROM customer WHERE (main_features || resolution || model ||
                    specification || usd_per_set || unit_cost_in_naira || unit_shipment_cost || total_cost_in_naira ||
                    reseller_markup15 || tsi_markup15 || end_user_markup35 || t_19rs || t_21rs || t_23rs ||
                    sunday_onu_silver || silver_dp || bronze_dp || platinum_dp || reseller_p || tsi_p || seven7dot4ns_rp || eu_price)
                    LIKE '%{output}%'
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                values = [row for row in results]
                return (values)
            else:
                return ("No match found")
        else:
            query = f"""SELECT * FROM customer WHERE (main_features || resolution || model ||
                    specification || usd_per_set || unit_cost_in_naira || unit_shipment_cost || total_cost_in_naira ||
                    reseller_markup15 || tsi_markup15 || end_user_markup35 || t_19rs || t_21rs || t_23rs ||
                    sunday_onu_silver || silver_dp || bronze_dp || platinum_dp || reseller_p || tsi_p || seven7dot4ns_rp || eu_price)
                    LIKE '%{output}%'
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                values = [row for row in results]
                return (values)
            else:
                return ("No match found")

    def recreate_table(self):
        """Deletes the existing table and recreates it"""
        try:
            cursor = self.conn.cursor()
        except sql.Error as e:
            print(f"The error '{e}' occurred")

        #Deletes the existing table
        print("Deleting Existing Table")
        cursor.execute("DROP TABLE IF EXISTS customer")
        cursor.execute("DROP TABLE IF EXISTS temp_customer")

        print("Deletion Successful")
        # Create temporary  table to hold data before creating new table
        create_sql_table = """
        CREATE TABLE temp_customer (
            main_features VARCHAR(300),
            resolution VARCHAR(50),
            model VARCHAR(20),
            specification VARCHAR(300),
            usd_per_set FLOAT,
            unit_cost_in_naira FLOAT,
            unit_shipment_cost FLOAT,
            total_cost_in_naira FLOAT,
            reseller_markup15 FLOAT,
            tsi_markup15 FLOAT,
            end_user_markup35 FLOAT,
            t_19rs FLOAT,
            t_21rs FLOAT,
            t_23rs FLOAT,
            sunday_onu_silver FLOAT,
            silver_dp FLOAT,
            bronze_dp FLOAT,
            platinum_dp FLOAT,
            reseller_p FLOAT,
            tsi_p FLOAT,
            seven7dot4ns_rp FLOAT,
            eu_price FLOAT
        )
        """
        cursor.execute(create_sql_table)

        # Read data from CSV and insert into SQLite database
        print("Inserting data from csv file into database")
        with open('JIREH_PRODUCT_PRICE_LIST.csv', 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                cursor.execute("INSERT INTO temp_customer VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                row)
        #Create a new table to hold the data transfered from the temporary table
        create_new_sql_table = """
        CREATE TABLE customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            main_features VARCHAR(300),
            resolution VARCHAR(50),
            model VARCHAR(20),
            specification VARCHAR(300),
            usd_per_set FLOAT,
            unit_cost_in_naira FLOAT,
            unit_shipment_cost FLOAT,
            total_cost_in_naira FLOAT,
            reseller_markup15 FLOAT,
            tsi_markup15 FLOAT,
            end_user_markup35 FLOAT,
            t_19rs FLOAT,
            t_21rs FLOAT,
            t_23rs FLOAT,
            sunday_onu_silver FLOAT,
            silver_dp FLOAT,
            bronze_dp FLOAT,
            platinum_dp FLOAT,
            reseller_p FLOAT,
            tsi_p FLOAT,
            seven7dot4ns_rp FLOAT,
            eu_price FLOAT
        )
        """
        cursor.execute(create_new_sql_table)
        # Transfers data from temporary table into new table
        cursor.execute("INSERT INTO customer\
                       (main_features, resolution, model, specification, usd_per_set, unit_cost_in_naira,\
                        unit_shipment_cost, total_cost_in_naira, reseller_markup15, tsi_markup15, end_user_markup35,\
                          t_19rs, t_21rs, t_23rs, sunday_onu_silver, silver_dp, bronze_dp, platinum_dp, reseller_p,\
                            tsi_p, seven7dot4ns_rp, eu_price)\
                        SELECT main_features, resolution, model, specification, usd_per_set, unit_cost_in_naira,\
                        unit_shipment_cost, total_cost_in_naira, reseller_markup15, tsi_markup15, end_user_markup35,\
                          t_19rs, t_21rs, t_23rs, sunday_onu_silver, silver_dp, bronze_dp, platinum_dp, reseller_p,\
                            tsi_p, seven7dot4ns_rp, eu_price FROM temp_customer;")
        #Drop(delete) the temporary table
        cursor.execute("DROP TABLE temp_customer;")
        # Commit changes and close connection
        self.conn.commit()
        cursor.close()
        print("Table Recreation Successful")


    def update_rate(self, rate, conn):
        """
        This function updates the exchange rate in the database.
        """
        query = f"""
    UPDATE customer SET unit_cost_in_naira = usd_per_set * {rate};
    UPDATE customer SET unit_shipment_cost = unit_cost_in_naira * 3; 
    UPDATE customer SET total_cost_in_naira  = unit_shipment_cost + unit_cost_in_naira; 
    UPDATE customer SET reseller_markup15 = total_cost_in_naira * 0.15; 
    UPDATE customer SET tsi_markup15 = total_cost_in_naira  * 0.25; 
    UPDATE customer SET end_user_markup35 = total_cost_in_naira  * 0.35; 
    UPDATE customer SET t_19rs = total_cost_in_naira * 0.16; 
    UPDATE customer SET t_21rs = total_cost_in_naira * 0.14; 
    UPDATE customer SET t_23rs = total_cost_in_naira * 0.12; 
    UPDATE customer SET sunday_onu_silver =  total_cost_in_naira + t_19rs; 
    UPDATE customer SET eu_price = total_cost_in_naira + end_user_markup35; 
    UPDATE customer SET silver_dp = eu_price * 0.92; 
    UPDATE customer SET bronze_dp  = eu_price * 0.88; 
    UPDATE customer SET platinum_dp = eu_price * 0.85; 
    UPDATE customer SET seven7dot4ns_rp = eu_price * 0.927;
    """
        
        cursor = conn.cursor()
        cursor.executescript(query, )
        conn.commit()

        cursor.execute("SELECT * FROM customer")
        rows = cursor.fetchall()

        cursor.close()

        print("Data Updated Successfully")

        print("Inserting data from csv file into database")

        

        # Create a directory named "new_folder" in the current working directory
        try:
            os.mkdir("./export")
            print("Directory created successfully")
        except FileExistsError:
            print("Directory already exists")

        if rows:
            with open('./export/JIREH_PRODUCT_PRICE_LIST.csv', 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    csv_writer.writerow([description[0] for description in cursor.description])

                    csv_writer.writerows(rows)
            print("Data has been written to CSV")
        else:
            print("No data available to write to CSV")

        
        