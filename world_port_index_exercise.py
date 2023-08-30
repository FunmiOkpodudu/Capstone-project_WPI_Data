#!/usr/bin/env python
# coding: utf-8

# #

# # <center>DATA ENGINEERING CAPSTONE PROJECT 2 (World Port Index Data Migration)</center>

# ## EXTRACTION PROCESS

# ### STEP 1 - Connecting to Access Database

# ### STEP 1a - Install Required Libraries
# 
# 
#     Python libraries needed are (1) pyodbc library is used to connect to other databases and (2) pandas 
#     
# 
# 

# In[1]:


pip install pyodbc


# In[2]:


pip install pandas


# ### STEP 1b- Import Required Libraries

# In[3]:


import pyodbc
import pandas as pd


# ### STEP 1c Connection Setup Function
# 
# This function, connect_to_database, takes a single argument database_path, which is the path to the Microsoft Access database file. The function then constructs a connection string using the provided path and the Microsoft Access ODBC driver. The pyodbc.connect() function is used to establish the database connection, and the connection object is returned.

# In[4]:


import pyodbc

def connect_to_database(database_path):
    # Open a connection to the Access database using the provided database_path
    conn = pyodbc.connect(fr'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={database_path};')
    return conn

# Provide the path to the Access database
database_path = r'C:\Users\JOHNNY\Desktop\WPI.mdb'

# Call the function to establish a connection
connection = connect_to_database(database_path)


# ### STEP 2 - Retrieving Table Names Function:
# 
# 
# This function, get_table_names, takes a single argument connection, which is a valid database connection object. The function retrieves the names of tables from the database using a list comprehension and the tables() method of the cursor. It filters the tables by specifying tableType="TABLE"
# 

# In[5]:


def get_table_names(connection):
    # Get the table names using a list comprehension and the tables() method
    cursor = connection.cursor()
    table_names = [table.table_name for table in cursor.tables(tableType="TABLE")]
    return table_names

# Call the function to retrieve table names
table_names = get_table_names(connection)

# Close the connection
#connection.close()

# Iterate through table names and print each name
for name in table_names:
    print(name)


# ### STEP 3 -Fetching the table data ('Wpi Data)

# In[ ]:





# In[15]:


#assigning a SQL query string to the variable named query, its a select statement that retrieves all column from a table named "Wpi Data"
query = '''    
SELECT * FROM "Wpi Data"
'''

# Fetch table data as a pandas DataFrame, it fetches the data from the database using the read_sql function. 
table_data = pd.read_sql(query, connection)


# Print the first few rows of the DataFrame
print(table_data.head())



# In[16]:


table_data


# In[17]:


table_data.info()


# ## LOADING PROCESS

# ### STEP 4 - Loading the table data 'Wpi' Data into DB

# In[21]:


pip install psycopg2


# In[22]:


pip install sqlalchemy


# In[19]:


from sqlalchemy import create_engine


# In[20]:


engine = create_engine("postgresql://postgres:pw@localhost:5432/world_port_index")
connection = engine.connect()
table_data.to_sql ("Wpi Data", con=engine, if_exists='replace', index=False)


# ### STEP 5 - Retreiving the data from DB

# In[2]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[3]:


Password_DB = "pw"


# In[4]:


from urllib.parse import quote
password = quote("pw")
connection_url = f"postgresql://postgres:{password}@localhost:5432/world_port_index"


# In[5]:


get_ipython().run_line_magic('sql', '$connection_url')


# In[5]:


get_ipython().run_cell_magic('sql', '', '\nSELECT * FROM "Wpi Data";\n')


# ### STEP 6 - Solving SQL Queries

# ### 1. What are the 5 nearest ports to Singapore's JURONG ISLAND port? (country = 'SG',port_name = 'JURONG ISLAND').Your answer should include the columns port_name and distance_in_meters only.

# In[28]:


get_ipython().run_cell_magic('sql', '', '\nSELECT * FROM "Wpi Data" WHERE "Main_port_name" = \'JURONG ISLAND\';\n')


# In[31]:


get_ipython().run_cell_magic('sql', '', '--This expression calculates the distance using the haversine formula, \n--which calculates distances between two points on a sphere given their latitudes and longitudes.\nSELECT "Main_port_name",\n    6371000 * ACOS(\n        SIN(RADIANS(1)) * SIN(RADIANS("Latitude_degrees")) +\n        COS(RADIANS(1)) * COS(RADIANS("Latitude_degrees")) *\n        COS(RADIANS("Longitude_degrees") - RADIANS(103))\n    ) AS distance_in_meters\nFROM "Wpi Data"\nORDER BY distance_in_meters\nLIMIT 5;\n\n')


# ### 2 Which country has the largest number of ports with a cargo_wharf? Youranswer should include the columns country and port_count only.

# In[61]:


get_ipython().run_cell_magic('sql', '', '\nSELECT \n    "Wpi_country_code" as country,\n    count("Main_port_name") as port_count \nfrom \n    "Wpi Data"  \nGROUP BY \n    "Wpi_country_code" \nORDER BY \n    port_count DESC \nLIMIT 1\n')


#  ### 3. You receive a distress call from the middle of the North Atlantic Ocean. The person on the line gave you a coordinates of lat: 32.610982, long: -38.706256 and asked for the nearest port with provisions, water, fuel_oil and diesel. Your answer should include the columns country, port_name, port_latitude and port_longitude only.

# In[32]:


get_ipython().run_cell_magic('sql', '', '\nSELECT "Wpi_country_code" AS country, "Main_port_name" AS port_name, "Latitude_degrees" AS port_latitude, "Longitude_degrees" AS port_longitude,\n    (6371000 * \n        acos(\n            cos(radians(32.610982)) * cos(radians("Latitude_degrees")) * cos(radians("Longitude_degrees") - radians(-38.706256)) +\n            sin(radians(32.610982)) * sin(radians("Latitude_degrees"))\n        )\n    ) AS distance_in_meters\nFROM "Wpi Data"\nWHERE "Supplies_provisions" = \'Y\' AND "Supplies_water" = \'Y\' AND "Supplies_fuel_oil" = \'Y\' AND "Supplies_diesel_oil" = \'Y\'\nORDER BY distance_in_meters\nLIMIT 1;\n\n')


# # THE END

# #
