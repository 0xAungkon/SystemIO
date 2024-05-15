'''
Dictionary CRUD Functions
'''





from fastapi import FastAPI, HTTPException
from .context import Context
# import libraries


def get_row_by_id(table,id: int, columns:list=['*']):
    columns=','.join(columns)
    # convert list to query string
    cursor = Context.database.cursor()
    query = "SELECT {} FROM {} WHERE id=%s;".format(columns,table)
    cursor.execute(query, (id,))
    # build query
    column_names = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if(row):
        return Context.list_to_dict([row], column_names)[0]
    else:
        return False
    # get row as dict in case of success or return false in case of failure

def get_rows_by_where(table, where: dict, columns:list=['*'],order_by='1',order_type='ASC',limit=10,offset=0):
    columns=','.join(columns)
    # convert list to query string
    where_sql=""
    for key, value in where.items():
        where_sql+=f"{key}='{value}' AND "
    # build where query from dict
    
    cursor = Context.database.cursor()
    query = "SELECT {} FROM {}".format(columns,table)
    query += f" WHERE {where_sql} TRUE ORDER BY {order_by} {order_type} LIMIT {limit} OFFSET {offset};"
    cursor.execute(query, (where,))
    # build query
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if(rows):
        return Context.list_to_dict(rows, column_names)
        # return list of dict
    else:
        return False
    


def get_row_by_where(table, where: dict, columns:list=['*']):
    columns=','.join(columns)
    # convert list to query string
    where_sql=""
    for key, value in where.items():
        where_sql+=f"{key}='{value}' AND "
    # build where query from dict
    
    cursor = Context.database.cursor()
    query = "SELECT {} FROM {}".format(columns,table)
    query += f" WHERE {where_sql} TRUE;"
    cursor.execute(query, (where,))
    # build query
    column_names = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if(row):
        return Context.list_to_dict([row], column_names)[0]
    else:
        return False
    # get row as dict in case of success or return false in case of failure
    
def update_row_by_id(table,id: int, data: dict):
    # convert dict to query string
    data_sql=""
    for key, value in data.items():
        data_sql+=f"{key}='{value}', "
    # build data query from dict
    data_sql=data_sql[:-2]
    # remove last comma
    cursor = Context.database.cursor()
    query = "UPDATE {} SET {} WHERE id=%s;".format(table,data_sql)
    cursor.execute(query, (id,))
    return get_row_by_id(table,id)

def insert_row(table, data: dict):
    # Extract column names and values
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    
    # Build and execute the query
    cursor = Context.database.cursor()
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
    cursor.execute(query, tuple(data.values()))
    # Retrieve last inserted id
    cursor.execute('SELECT LASTVAL()')
    id= cursor.fetchone()[0]
    return get_row_by_id(table,id)

