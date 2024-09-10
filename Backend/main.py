# Import Libraries
import re, ast
import copy
import json 
import keys
import mysql.connector
import pandas as pd
import anthropic

from colorama import Fore, Style
from table_schema import schema

ANTHROPIC_ACESSS_TOKEN = keys.anthropic

## Query Decomposition Agent(Modified the prompt and made it more accurate, removed function calling as it was not needed)
def dashboard(user_query):
    # user_query += " with 2 diverse panels."
    decomposed_query = []

    default_sys_message = f"""
        You are an AI assistant specialized in query decomposition with access to the schema of a database. Your task is to analyze a
        given user query, break it down into independent sub-queries, and ensure each sub-query can be executed independently against the
        provided database schema. An independent sub-query is a smaller, self-contained question whose answer does not depend on the
        answer to another sub-query. If the user query cannot be broken down into independent sub-queries, return the original query as is.
        Do not generate any SQL query, only generate the independent sub-queries.

        ### Schema Information:
            1. advanced_monthly_sales_for_retail_and_food_services
               - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
            2. advanced_monthly_sales_for_retail_and_food_services_categories
               - Columns: cat_idx (Primary key), cat_code, cat_desc
               - Relationship: cat_code is related to the category_code column of the table advanced_monthly_sales_for_retail_and_food_service.
            3. advanced_monthly_sales_for_retail_and_food_services_data_types
               - Columns: dt_idx (Primary key), dt_code, dt_desc
               - Relationship: dt_code is related to the data_type_code column in the advanced_monthly_sales_for_retail_and_food_service table.
            4. housing_vacancies_and_homeownership
               - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id
            5. housing_vacancies_and_homeownership_categories
               - Columns: cat_idx (Primary key), cat_code, cat_desc
               - Relationship: cat_code is related to the category_code column of the table housing_vacancies_and_homeownership.
            6. housing_vacancies_and_homeownership_data_types
               - Columns: dt_idx (Primary key), dt_code, dt_desc
               - Relationship: dt_code is related to the data_type_code column in the housing_vacancies_and_homeownership table.
            7. international_trade
               - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
            8. international_trade_categories
               - Columns: cat_idx (Primary key), cat_code, cat_desc
               - Relationship: cat_code is related to the category_code column of the table international_trade.
            9. international_trade_data_types
               - Columns: dt_idx (Primary key), dt_code, dt_desc
               - Relationship: dt_code is related to the data_type_code column in the international_trade table.
            10. manufacturers_shipments_inventories_and_orders
                - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
            11. manufacturers_shipments_inventories_and_orders_categories
                - Columns: cat_idx (Primary key), cat_code, cat_desc
                - Relationship: cat_code is related to the category_code column of the table manufacturers_shipments_inventories_and_orders.
            12. manufacturers_shipments_inventories_and_orders_data_types
                - Columns: dt_idx (Primary key), dt_code, dt_desc
                - Relationship: dt_code is related to the data_type_code column in the manufacturers_shipments_inventories_and_orders table.
            
        ### Instructions:
        1. Analyze the user query considering the provided schema to determine if it can be segmented into smaller independent sub-queries.
        2. Ensure each sub-query is executable independently within the context of the database schema.
        3. If the query cannot be broken down, return the original query without modifications.
        4. Provide a clear and concise response with the identified sub-queries or the original query.

        ### CAUTION:
        1. You only have to generate the sub-queries, do not generate any SQL query.
        2. Always ensure that each sub-query is independent of all the previous sub-queries, that its answer does not depend on the answer to another sub-query.

        ### Output Format:
        User Query: The input query you must decompose.
        Sub-query: The independent sub-query generated from the user-query, this should be a valid python string and should not contain any SQL query.
        ....(this Sub-query can repeat N times)
        Final Response: A list containing each of above sub-queries, where each Sub-query is a valid python string.
           
        ### Examples:
            Example Query 1:
                User Query: "Find the average cell_value for each category in the advanced_monthly_sales_for_retail_and_food_services table and the corresponding category descriptions."
                Sub-query: "Find the average cell_value for each category_code in the advanced_monthly_sales_for_retail_and_food_services table."
                Sub-query: "Retrieve cat_desc for each cat_code from the advanced_monthly_sales_for_retail_and_food_services_categories table."
                Final Response: ["Find the average cell_value for each category_code in the advanced_monthly_sales_for_retail_and_food_services table.", "Retrieve cat_desc for each cat_code from the advanced_monthly_sales_for_retail_and_food_services_categories table."]

            Example Query 2:
                User Query: "Get the sale_value of international_trade data types with errors."
                Sub-query: "Get the sale_value of international_trade data types with errors."
                Final Response: ["Get the sale_value of international_trade data types with errors."]
    """

    client = anthropic.Anthropic(api_key=ANTHROPIC_ACESSS_TOKEN)
    model = "claude-3-haiku-20240307"
    messages = [
        {
            "role": "user",
            "content": f"User Query: {user_query}"
        }
    ]
    response = client.messages.create(
            model=model,
            system=default_sys_message,
            messages=messages,
            max_tokens=4096,
            stream=False,
            temperature=0.0,
    )
    
    ## Define a regex pattern to extract the `Final Response`
    pattern = "\[.*\]"
    for idx, block in enumerate(response.content):
        if block.type != "text":
            continue
    
        # print("[+] Below is the natural language repsonse generated by claude-haiku for the current block.....")
        # print(block.text)

        match = re.search(pattern=pattern, string=block.text, flags=re.DOTALL)
        if match:
            print("[+] Regex Match Found, processing the query.....")
            extracted_data = match.group()
            
            try:
                extracted_data = ast.literal_eval(extracted_data)
            except Exception as e:
                print("[-] Failed to parse the response from claude, below is the error that was raised.")
                print(e)
                continue

            # Insert the data back into `decomposed_query` list
            for idx, sub_query in enumerate(extracted_data):
                decomposed_query.append(sub_query)
                # print(f"[+] Sub-Query {idx + 1}: {sub_query}")
        else:
            print("[-] No match found......")
    print()
    return decomposed_query

## Helper functions for Reasoning Agent
def extract_query_analysis(output):
    # Extract the Query Analysis section
    match = re.search(r'Query Analysis:(.*?)(Table Schemas:|$)', output, re.DOTALL)
    if match:
        query_analysis = match.group(1).strip()
        
        # Create a valid Python string by escaping quotes and backslashes
        python_string = f'"{query_analysis}"'
        return python_string
    return ""

def extract_table_schemas(output):
    match = re.search(r"Final Response:(.*?)({.*})", output, re.DOTALL)
    if match:
        schemas = match.group(2).strip()
        try:
            # Convert the string into a dictionary using json.loads
            if schemas.startswith('"') or schemas.startswith("'"):
                schemas = schemas[1:]
            if schemas.endswith('"') or schemas.endswith("'"):
                schemas = schemas[:-1]
            response_dict = json.loads(schemas)
            return response_dict
        except json.JSONDecodeError:
            print("[-] Error decoding JSON response")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}[-] Unable to extract `Reasoning Agent's` output.{Style.RESET_ALL}")
    return ""

## Reasoning Agent(Modified the prompt and made it more accurate, removed function calling, added regex for data extraction instead of pydantic parser)
def reason_agent(user_query):
    ## Purpose of this function is to generate a detailed natural language description that can be used to construct SQL-queries based on
    ## user-input.
    default_sys_message = f"""
        You are an AI assistant tasked with generating detailed, step-by-step instructions for resolving a user query using a specified
        database schema. Your instructions should outline the steps required to formulate SQL queries to address the user's request,
        including any necessary filtration, grouping, joins, and other operations.

        ### Schema Information:
        1. advanced_monthly_sales_for_retail_and_food_services
            - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
        2. advanced_monthly_sales_for_retail_and_food_services_categories
            - Columns: cat_idx (Primary key), cat_code, cat_desc
           - Relationship: cat_code is related to the category_code column of the table advanced_monthly_sales_for_retail_and_food_service.
        3. advanced_monthly_sales_for_retail_and_food_services_data_types
            - Columns: dt_idx (Primary key), dt_code, dt_desc
           - Relationship: dt_code is related to the data_type_code column in the advanced_monthly_sales_for_retail_and_food_service table.
        4. housing_vacancies_and_homeownership
           - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id
        5. housing_vacancies_and_homeownership_categories
           - Columns: cat_idx (Primary key), cat_code, cat_desc
            - Relationship: cat_code is related to the category_code column of the table housing_vacancies_and_homeownership.
        6. housing_vacancies_and_homeownership_data_types
           - Columns: dt_idx (Primary key), dt_code, dt_desc
           - Relationship: dt_code is related to the data_type_code column in the housing_vacancies_and_homeownership table.
        7. international_trade
           - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
        8. international_trade_categories
           - Columns: cat_idx (Primary key), cat_code, cat_desc
           - Relationship: cat_code is related to the category_code column of the table international_trade.
        9. international_trade_data_types
           - Columns: dt_idx (Primary key), dt_code, dt_desc
           - Relationship: dt_code is related to the data_type_code column in the international_trade table.
        10. manufacturers_shipments_inventories_and_orders
            - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
        11. manufacturers_shipments_inventories_and_orders_categories
            - Columns: cat_idx (Primary key), cat_code, cat_desc
            - Relationship: cat_code is related to the category_code column of the table manufacturers_shipments_inventories_and_orders.
        12. manufacturers_shipments_inventories_and_orders_data_types
            - Columns: dt_idx (Primary key), dt_code, dt_desc
            - Relationship: dt_code is related to the data_type_code column in the manufacturers_shipments_inventories_and_orders table.
        
        ###Instructions:
        1. Analyze the User Query: Examine the user query to understand the information being requested and the context in which it is required.
        2. Identify Relevant Tables and Columns: Based on the query, determine which tables and columns from the schema are relevant. Identify any relationships between tables that might be necessary for joins.
        3. Determine Required Operations:
            - Filtering: Specify any conditions that must be applied to the data (e.g., date ranges, specific categories).
            - Grouping: Identify if there is a need to group data (e.g., by category, by time period).
            - Joins: Determine if joins between tables are necessary to combine related information.
            - Aggregations: Specify any aggregations that need to be performed (e.g., sum, average).
            - Formulate SQL Instructions: Provide step-by-step instructions on how to construct SQL queries based on the identified operations. Ensure that the steps are clear and logically ordered to match the user query.
        4. Provide Schema Information: Include relevant schema details in the output to guide the construction of SQL queries.
        
        ### CAUTION:
        1. Your instructions should be in natural language, do not write or include any SQL query in your explanations.
        2. DO NOT HALLUCINATE table names, always use the table names provided in `Schema Information` section to identify the relevant tables for the user-query.

        ### Use the following format:
        User Query: The input query you must analyse.
        Query Analysis: Contains the detailed step by step instructions on how to resolve user query in natural language.
        Table Schemas: Contains the Schema information of the tables needed to resolve the above query.
        Final Response: Contains the final response in below format:
            {{
                "schema": [
                    "This is a list of strings, where each string contains the name of the table needed to resolve the user query."
                ]
            }}

        ### Examples:
            Example 1:
            User Query: Get the total sales value for each category in the advanced_monthly_sales_for_retail_and_food_services table for the year 2023.
            Query Analysis: Below is step by step query analysis:-
                1. Filter Data: Select records from the advanced_monthly_sales_for_retail_and_food_services table where the time column indicates the year 2023.
                2. Group Data: Group the filtered data by category_code.
                3. Aggregate Data: Calculate the total cell_value (sales value) for each category_code.
                4. Join: Join the result with the advanced_monthly_sales_for_retail_and_food_services_categories table on category_code to get cat_desc.
            Table Schemas: On the basis of above analysis the relevant table schemas are:
                1. advanced_monthly_sales_for_retail_and_food_services
                   - Columns: id (Primary key), category_code, cell_value(sales value), data_type_code, error_data, seasonally_adj, time, time_slot_id, us
                2. advanced_monthly_sales_for_retail_and_food_services_categories
                   - Columns: cat_idx (Primary key), cat_code, cat_desc
            Final Response: {{
                "schema": ["advanced_monthly_sales_for_retail_and_food_services", "advanced_monthly_sales_for_retail_and_food_services_categories"]
            }}
    """
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_ACESSS_TOKEN)
    model = "claude-3-haiku-20240307"
    messages = [
        {
            "role": "user",
            "content": f"User Query: {user_query}"   
        }
    ]

    response = client.messages.create(
            model=model,
            system=default_sys_message,
            messages=messages,
            max_tokens=4096,
            stream=False,
            temperature=0.0,
    )

    for idx, block in enumerate(response.content):
        if block.type != "text":
            continue
        # print("[+] Below is the block content....")
        # print(block.text, end="\n\n")

        ## Extract the detailed description generated by the LLM
        description = extract_query_analysis(block.text)
        schemas = extract_table_schemas(block.text)
        return {
            "Response": description,
            "Schema": schemas['schema']
        }
    return {}

## Helper functions for act_agent and charting_agent
def get_schemas_in_string_format(tables_schemas):
    schema_string = """"""
    for idx, table_name in enumerate(tables_schemas):
        # print(table_name)
        table_schema = schema[table_name]
        table_schema = ast.literal_eval(table_schema)

        #
        schema_string += f"{idx + 1}. " + table_name + ": "
        for column in table_schema:
            column_name = column['Field']
            column_data_type = column['Type']
            schema_string += str(column_name) + f"({column_data_type}), "
        schema_string = schema_string[:-2] + "\n"
    return schema_string

def extract_response(output):
    match = re.search(r"Final Response:(.*?)({.*})", output, re.DOTALL)
    if match:
        response_data = match.group(2).strip()
        response_data = re.sub(r"\s+", r" ", response_data.strip())

        try:
            # Convert the string into a dictionary using json.loads
            if response_data.startswith('"') or response_data.startswith("'"):
                response_data = response_data[1:]
            if response_data.endswith('"') or response_data.endswith("'"):
                response_data = response_data[:-1]
            response_dict = json.loads(response_data)
            return response_dict
        except json.JSONDecodeError:
            print(f"{Fore.RED}{Style.BRIGHT}[-] Error decoding JSON response.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}[-] Unable to extract `Act Agent's` output.{Style.RESET_ALL}")
    return {}

## Act Agent(Used Anthropic's SDK instead of LangChain, changed the function's signature, i.e added user-query arguement, modified the prompt and included user-query to enhance context)
def act_agent(user_query, description, tables_schema, previous_query="", previous_error="", error_explaination={"cause": "None", "solution": "None"}):
    system_message = f"""
        You are an AI assistant tasked with generating an SQL query based on the provided user query, schema of relevant tables, and
        detailed step-by-step guidance. Your role is to precisely formulate the SQL query to retrieve the desired information while ensuring
        the correctness of table names, column names, and operations applied based on the column data types according to the schema.

        If the guidance is insufficient to write an appropriate SQL query, you may rely on your inherent knowledge to make necessary
        adjustments. However, you must always ensure that the operations on columns make sense according to their data types and maintain
        strict adherence to the given schema.

        ### Instructions:
        1. Analyze the Guidance and Schema: Carefully review the provided step-by-step guidance and schema details to understand the operations required to fulfill the user query.
        2. Review Previous Errors and Adjust: If "Previous Query," "Previous Errors," "Cause," and "Solution" are provided, carefully examine these sections. Identify the cause of the error from the "Cause" field, and use the "Solution" to guide corrections or improvements in the SQL query. Avoid repeating the same mistakes and ensure that the corrected query addresses the identified issues.
        3. Data Type Awareness: Ensure that any operation applied to a column is appropriate for its data type. For example, if a column is of type VARCHAR, do not use numeric or date-specific functions directly; instead, use string manipulation functions suitable for that type.
        4. Generate the SQL Query: Construct an SQL query using the exact table and column names as specified in the schema. Ensure that the query performs the necessary operations such as filtering, grouping, joining, or aggregating, as outlined in the guidance.
        5. Describe the SQL Output: Write a brief description of what kind of data the query will fetch, explaining how it addresses the user query.
        6. Adhere to Schema Specifics: Ensure the table and column names in the SQL query match exactly with the provided schema. Avoid any deviations or assumptions that conflict with the given schema details.

        ### Input Format:
        1. User Query: A statement detailing what the user wants to retrieve from the database.
        2. Schema: A list of relevant tables with their columns, data types, and relationships, precisely matching the database.
        3. Step-by-Step Guidance: Detailed instructions on how to construct the SQL query, including the necessary operations.
        4. Previous Query: The SQL query that was previously generated, which caused an error. If this is the first attempt, this field will be empty string.
        5. Previous Errors: Any error messages or descriptions of what went wrong with the previous query. If this is the first attempt, this field will be empty string.
        6. Cause: A brief natural language description of what caused the error, if any. If this is the first time generating the query, this field will be an empty string.
        7. Solution: A brief natural language description of the solution to address the error, if any. If this is the first time generating the query, this field will be an empty string.

        ### Output Format:
        1. Output should be in the below format:
           Final Response: {{
                "sql_query": "Your SQL query here",
                "sql_query_description": "A clear description of what the query does and the type of data it will fetch."
           }}

        ### Example:
        -> User Query: "Find the average sales value for each data type in the international_trade table."
        -> Schema: Below is the schema of the relevant tables:
            international_trade: id (INT), category_code (VARCHAR), cell_value (FLOAT), data_type_code (VARCHAR)
        -> Step-by-Step Guidance:
            1. Group the records in the international_trade table by data_type_code.
            2. Calculate the average cell_value for each group.
            3. Join the result with international_trade_data_types on data_type_code to get dt_desc.
        -> Previous Query: SELECT dt_desc, AVG(cell_value) FROM international_trade JOIN international_trade_data_types ON data_type_code = dt_code GROUP BY dt_desc;
        -> Previous Errors: Error: Column 'data_type_code' is ambiguous.
        -> Cause: The error occurred because the data_type_code column exists in both tables, making it ambiguous.
        -> Solution: Use table aliases to explicitly specify the source of each column, particularly the ambiguous data_type_code.
        -> Final Response: {{
            "sql_query": "SELECT d.dt_desc, AVG(i.cell_value) AS average_sales FROM international_trade i JOIN international_trade_data_types d ON i.data_type_code = d.dt_code GROUP BY i.data_type_code, d.dt_desc;",
            "sql_query_description": "This query calculates the average sales value for each data type by grouping the data by data type codes and joining with the data types table to fetch the descriptions."
        }}
    """

    client = anthropic.Anthropic(api_key=ANTHROPIC_ACESSS_TOKEN)
    model = "claude-3-5-sonnet-20240620"

    input_message = f"""
        -> User Query: {user_query}
        -> Schema: Below is the schema of the relevant tables:
            {get_schemas_in_string_format(tables_schema)}
        -> Step-by-Step Guidance:
            {description}
        -> Previous Query: {previous_query}
        -> Previous Errors: {previous_error}
        -> Cause: {error_explaination['cause']},
        -> Solution: {error_explaination['solution']}
    """

    print(f"{Fore.BLACK}{Style.BRIGHT}[+] Input Message to `Act Agent` is shown below.{Style.RESET_ALL}")
    print(input_message)
    messages = [
        {
            "role": "user",
            "content": input_message  
        }
    ]
    # print("[+] Below is the input message to the LLM....")
    # print(input_message, end="\n\n")

    response = client.messages.create(
            model=model,
            system=system_message,
            messages=messages,
            max_tokens=8192,
            stream=False,
            temperature=0.0,
    )
    
    for idx, block in enumerate(response.content):
        if block.type != "text":
            continue
        response_data = extract_response(block.text)
        return response_data
    return {}

## Error Explanantion Agent
def error_explainer(tables_schema, previous_query="", previous_error=""):
    system_message = f"""
        You are an expert SQL analyst and database troubleshooter. Given an SQL query, the error message generated when running the query,
        and the schema information of the tables involved, your task is to provide a detailed and clear explanation of why the error occurred
        and a step-by-step guide on how to fix it. Your response should be comprehensive, addressing all possible causes of the error, and
        include any necessary adjustments to the query.

        ### Instructions:
        1. Analyze the Error: Carefully read the SQL query, error message, and table schema information provided. Identify the specific cause of the error based on the query structure, table relationships, column types, and constraints.
        2. Explain the Cause: Provide a thorough explanation of why the error occurred. Clearly identify the problematic parts of the SQL query, referencing relevant aspects of the table schema or error message.
        3. Step-by-Step Solution: Offer a detailed, actionable plan to fix the error. Include specific modifications to the SQL query, alternative approaches, or suggestions on how to restructure the data or query to resolve the issue.

        ### Input Format:
        1. SQL Query: The SQL query that was executed.
        2. Error Message: The exact error message generated when running the query.
        3. Table Schema Information: The schema details of the tables involved in the query, including column names, data types, constraints, primary and foreign keys.

        ### Output Format:
        1. Output should be in the below format:
            Final Response: {{
                "cause": "A clear and concise explanation of why the error occurred."
                "solution": "Step-by-step guidance on how to fix the error, including specific modifications to the query."
            }}
        
        ### Example:
            SQL Query: SELECT * FROM employees WHERE hire_date >= '2023-01-01' UNION SELECT * FROM departments.
            Error Message: ERROR 1222 (21000): The used SELECT statements have a different number of columns.
            Table Schema Information:
                1. employees: emp_id(INT), first_name (VARCHAR(50)), last_name (VARCHAR(50)), hire_date (DATE)
                2. departments: dept_id (INT), dept_name (VARCHAR(50))
            Final Response: {{
                "cause": "The error occurred because the UNION operation requires both SELECT statements to have the same number of columns with compatible data types. The employees table has four columns, while the departments table has two, causing the mismatch.",
                "solution": "To resolve the error, ensure both SELECT statements return the same number of columns. You can use NULL as placeholders for missing columns or explicitly select matching columns."
            }}
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_ACESSS_TOKEN)
    model = "claude-3-haiku-20240307"

    input_message = f"""
        SQL Query: {previous_query}

        Error Message: {previous_error}

        Table Schema Information:
        {get_schemas_in_string_format(tables_schema)}
    """

    messages = [
        {
            "role": "user",
            "content": input_message  
        }
    ]
    print(f"{Fore.BLACK}{Style.BRIGHT}[+] Input Message to `Error Explainer Agent` is shown below.{Style.RESET_ALL}")
    print(input_message)

    response = client.messages.create(
            model=model,
            system=system_message,
            messages=messages,
            max_tokens=4096,
            stream=False,
            temperature=0.0,
    )
    
    for idx, block in enumerate(response.content):
        if block.type != "text":
            continue
        response_data = extract_response(block.text)
        return response_data
    return {}

## Connetion means this will run the sql query on mysql database and return the dataframe what we are getting form the databases.
def connection(query):
    config = {
        'user': keys.user,
        'password': keys.password,
        'host': keys.host,
        'database': keys.database,
        'auth_plugin': 'mysql_native_password', # this plugin defines how mysql handles the authentication process for users
    }
    conn = mysql.connector.connect(**config)
    df = pd.read_sql(query, conn)
    return df

## Charting Agent(Used Anthropic's SDK instead of LangChain, changed the function's signature, i.e added user-query arguement, modified the prompt and included user-query to enhance context)
def chart_description(user_query, tables_schemas, df):
    system_message = f"""
        You are an AI assistant tasked with determining the appropriate visualization settings based on a user query, sample data extracted
        from a database, and the schema of the tables used in the query. Your goal is to identify the correct plot type, plot title, x-axis
        label, y-axis label, and legend label, ensuring the labels align precisely with the column names as defined in the table schema.

        ### Instructions:
        1. Analyze the User Query: Understand the user’s intent and the type of insight or relationship they are seeking from the data.
        2. Examine the Sample Data: Review the provided sample data to identify key columns and their values, which will help in determining the appropriate visualization approach.
        3. Refer to the Schema: Ensure that the x-axis and y-axis labels directly match the column names from the table schema, without alterations or assumptions. The labels must accurately reflect the data used in the query.
        4. Determine Plot Settings:
            4.1. Plot Type: Choose the most appropriate type of plot (e.g., bar chart, line plot, scatter plot, pie chart) based on the nature of the data and the user query.
            4.2. Plot Title: Create a clear and descriptive title that summarizes the main focus of the plot.
            4.3. X Label and Y Label: Set the labels for the x-axis and y-axis to match the relevant column names exactly as specified in the table schema.
            4.4. Legend Label: If applicable, identify an appropriate label for the legend to differentiate multiple data series.
        
        ### Input Format:
        1. User Query: A description of what the user wants to visualize or understand from the data.
        2. Sample Data: A subset of data extracted from the database that answers the user query.
        3. Table Schema: The schema of the relevant tables including column names and their data types.

        ### CAUTION:
        1. If "legend_label" is not applicable, set its value to null, as in JSON.

        ### Output Format:
        Final Response: {{
            "plot_type": "Specify the type of plot (e.g., bar, line, scatter, pie)",
            "plot_title": "A clear title summarizing the main focus of the plot",
            "x_label": "Exact name of the x-axis column from the schema",
            "y_label": "Exact name of the y-axis column from the schema",
            "legend_label": "Label for the legend (if applicable) else set it to null"
        }}

        ### Example:
            User Query: "Visualize the total sales value per category for the year 2023."
            Sample Data:
                | category_code | cell_value |
                |---------------|------------|
                | CAT001        | 120000     |
                | CAT002        | 95000      |
            Table Schema: Below is the schema information of the relevant tables:
                advanced_monthly_sales_for_retail_and_food_services: category_code (VARCHAR), cell_value (FLOAT), time (VARCHAR)
            Final Response: {{
                "plot_type": "bar",
                "plot_title": "Total Sales Value per Category in 2023",
                "x_label": "category_code",
                "y_label": "cell_value",
                "legend_label": "Sales Value"
            }}
    """

    client = anthropic.Anthropic(api_key=ANTHROPIC_ACESSS_TOKEN)
    model = "claude-3-haiku-20240307"
    input_message = f"""
        User Query: {user_query}
        Sample Data:
    {df}
        Table Schema: Below is the schema information of the relevant tables:
            {get_schemas_in_string_format(tables_schemas)}
    """

    # print("[+] Below is the input message.")
    # print(input_message)
    messages = [
        {
            "role": "user",
            "content": input_message
        }
    ]

    response = client.messages.create(
            model=model,
            system=system_message,
            messages=messages,
            max_tokens=4096,
            stream=False,
            temperature=0.0,
    )

    for idx, block in enumerate(response.content):
        if block.type != "text":
            continue
        visualisation_data = extract_response(block.text)
        return visualisation_data
    return {}

def main(main_query):
    answer = []
    empty_list = []
    
    print(f"{Fore.BLACK}{Style.BRIGHT}[+] User Query: {Style.RESET_ALL}", main_query, end="\n\n")
    print(f"{Fore.GREEN}{Style.BRIGHT}[+] Entering Query Decomposition Agent Chain>>>{Style.RESET_ALL}")
    queries = dashboard(main_query) ## Decomposing the query into sub-queries that can be independently executed
    
    print(f"{Fore.BLACK}{Style.BRIGHT}[+] Query Decomposition Agent Finished, below are the identified sub-queries.{Style.RESET_ALL}")
    print(queries)
    print("[+] Total Number of Sub-Queries: ", len(queries))
    print(end="\n\n")

    for idx, user_query in enumerate(queries):
        try:
            print(f"{Fore.BLACK}{Style.BRIGHT}[+] Processing sub-query {idx + 1}: {Style.RESET_ALL}", user_query, end="\n\n")
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] Entering the Reasoning Agent Chain>>>{Style.RESET_ALL}")
            reason_agent_response = reason_agent(user_query) ## This agent writes a detailed step by step guide on how to resolve the user-query.
            
            print(f"{Fore.BLACK}{Style.BRIGHT}[+] Reason Agent Finished. Response is shown below.{Style.RESET_ALL}")
            print("[+] Detailed guide generated by `Reason Agent:\n", reason_agent_response['Response'])
            print("[+] Table Schema necessary to resolve the query as identified by `Reason Agent`:\n", reason_agent_response['Schema'])
            print()

            ## Extracting the `Reason Agent`'s response
            description = reason_agent_response['Response']
            tables_schema = reason_agent_response['Schema']

            ## Check for hallucinations
            de_hallucinated_tables_schemas = []
            for table_name in tables_schema:
                if table_name in schema.keys():
                    de_hallucinated_tables_schemas.append(table_name)
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}[+] Hallucination Encountered, removing the hallucinated table.{Style.RESET_ALL}")
            print(f"{Fore.BLACK}{Style.BRIGHT}[+] De-hallucinated tables: {Style.RESET_ALL}", de_hallucinated_tables_schemas, end="\n\n")

            ## Checking if data-pertaining to sub-query is not present in any of the tables
            if not de_hallucinated_tables_schemas:
                print(f"{Fore.RED}{Style.BRIGHT}[-] Data pertaining to user-query is not present in database.{Style.RESET_ALL}", end="\n\n")
                result = {
                    "sql_query": "",
                    "plot_type_name": "table",
                    "plot_title": "Error Data Not Present",
                    "x": "Error",
                    "y": "Reason",
                    "legend": None,
                    "data": [{
                        'x_value': "Bad Request: 400(Status Code)",
                        'y_value': f"Data requested by user for the following sub-query is not present in the database. Please Try again.\n{Fore.BLACK}{Style.BRIGHT} [+] Sub-Query: {Style.RESET_ALL} {user_query}"
                    }],
                    "description": "Data pertaining to user-query is not present in database. Thus no sql statement was generated."
                }
                empty_list.append(result)
                continue

            ## Generating SQL query for the provided user-query, using the instructions given in `description` by using `Act Agent`
            act_agent_response, sql_query_v, sql_query_description_v, df = None, None, None, None
            previous_query, previous_error = None, None
            error_explanation = {
                "cause": "None",
                "solution": "None"
            }

            max_retry = 0
            while True:
                if max_retry > 2:
                    break
                try:
                    if max_retry == 0:
                        print(f"{Fore.GREEN}{Style.BRIGHT}[+] Entering the Act Agent Chain>>>{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}{Style.BRIGHT}[+] Rentering the Act Agent Chain, as error was encountered previously>>>{Style.RESET_ALL}")
                    act_agent_response = act_agent(user_query, description, de_hallucinated_tables_schemas, previous_query, previous_error, error_explanation)
                   
                    sql_query_v = act_agent_response["sql_query"]
                    sql_query_description_v = act_agent_response["sql_query_description"]

                    print(f"{Fore.BLACK}{Style.BRIGHT}[+] Act Agent Finished. Response is shown below{Style.RESET_ALL}")
                    print("[+] SQL description: ", sql_query_description_v, end="\n\n")
                    print("[+] SQL Query: ", sql_query_v)

                    ## Running the SQL query against the database
                    df = connection(sql_query_v)
                    print(f"{Fore.GREEN}{Style.BRIGHT}[+] SQL Execution Successful{Style.RESET_ALL}")
                    break
                except Exception as e:
                    print(f"{Fore.RED}{Style.BRIGHT}[-] Inappropriate SQL query. Error is shown below{Style.RESET_ALL}")
                    print(e)
                    print(f"{Fore.GREEN}{Style.BRIGHT}[+] Entering the Error Explainer Agent Chain>>>{Style.RESET_ALL}")
                    previous_query = sql_query_v
                    previous_error = str(e)
                    error_explanation = error_explainer(de_hallucinated_tables_schemas, previous_query, previous_error)
                    max_retry += 1

            if df.empty:
                print(f"{Fore.RED}{Style.BRIGHT}[-] No data relating to user-query could be found in databse.{Style.RESET_ALL}")
                result = {
                    "sql_query": sql_query_v,
                    "plot_type_name": "table",
                    "plot_title": "Error Data Not Present",
                    "x": "Error",
                    "y": "Reason",
                    "legend": None,
                    "data": [{
                        'x_value': "Bad Request: 400(Status Code)",
                        'y_value': f"Data requested by user for the following sub-query is not present in the database. Please Try again.\n{Fore.BLACK}{Style.BRIGHT} [+] Sub-Query: {Style.RESET_ALL} {user_query}"
                    }],
                    "description": sql_query_description_v
                }
                empty_list.append(result)
                continue

            five_rows = df.head(5).to_markdown(index=False, tablefmt="grid")
            print(f"{Fore.BLACK}{Style.BRIGHT}[+] Subset of data retrieved is shown below.{Style.RESET_ALL}")
            print(five_rows, end="\n\n")

            print(f"{Fore.GREEN}{Style.BRIGHT}[+] Entering the Charting Agent Chain>>>{Style.RESET_ALL}")
            plot_description_response = chart_description(user_query, tables_schema, five_rows)
            print(f"{Fore.BLACK}{Style.BRIGHT}[+] Charting Agent Finished. Response is shown below{Style.RESET_ALL}")
            print(plot_description_response)

            plot_type_name_v = plot_description_response["plot_type"]
            plot_title_v = plot_description_response["plot_title"]
            x_label_v = plot_description_response["x_label"]
            y_label_v = plot_description_response["y_label"]
            legend_label_v = plot_description_response["legend_label"]

            x_value, y_value = None, None
            data = [{
                'x_value': None,
                'y_value': None
            }]

            try:
                x_value = df[x_label_v]
                x_value_list = [value for _, value in x_value.items()]
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT} [-] Column-Name for X-label is not present in the table schema.{Style.RESET_ALL}")
                print(e)
                continue
            
            try:
                y_value = df[y_label_v]
                y_value_list = [value for _, value in y_value.items()]
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT} [-] Column-Name for Y-label is not present in the table schema.{Style.RESET_ALL}")
                print(e)
                continue

            if not legend_label_v:
                data = [{'x_value': x_val, 'y_value': y_val} for x_val, y_val in zip(x_value_list, y_value_list)]
                print(f"{Fore.RED}{Style.BRIGHT} [-] No label found.{Style.RESET_ALL}")
            else:
                legend_value = df[legend_label_v]
                legend_value_list = [value for _, value in legend_value.items()]
                data = [{'x_value': x_val, 'y_value': y_val, 'legend_value': legend_val} for x_val, y_val, legend_val in zip(x_value_list, y_value_list, legend_value_list)]

            result = {
                "sql_query": sql_query_v,
                "plot_type_name": plot_type_name_v,
                "plot_title": plot_title_v,
                "x": x_label_v,
                "y": y_label_v,
                "legend": legend_label_v,
                "data": copy.deepcopy(data),
                "description": sql_query_description_v
            }
            answer.append(result)
            print("---------------------------------------------------------------------------------------------", end="\n\n")
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT} An Exception has occurred.{Style.RESET_ALL}")
            print(e)
            result = {
                    "sql_query": sql_query_v or "",
                    "plot_type_name": "table",
                    "plot_title": "Error Data Not Present",
                    "x": "Error",
                    "y": "Reason",
                    "legend": None,
                    "data": [{
                        'x_value': "Bad Request: 400(Status Code)",
                        'y_value': f"Data requested by user for the following sub-query is not present in the database. Please Try again.\n{Fore.BLACK}{Style.BRIGHT} [+] Sub-Query: {Style.RESET_ALL} {user_query}"
                    }],
                    "description":  sql_query_description_v or "Data pertaining to user-query is not present in database. Thus no sql statement was generated."
                }
            empty_list.append(result)

    if len(empty_list) == len(queries):
        return empty_list
    return answer
