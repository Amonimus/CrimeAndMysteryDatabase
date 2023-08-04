import sqlite3


def get_db_connection():
	conn: sqlite3.Connection = sqlite3.connect('database.db')
	conn.execute("PRAGMA foreign_keys = 1")
	conn.row_factory = sqlite3.Row
	return conn


def sql_select(rows):
	return f"SELECT {rows}"


def sql_from(sql, table):
	sql += f" FROM {table}"
	return sql


def sql_where(sql, column, condition):
	sql += f" WHERE {column}={condition}"
	return sql

def sql_order(sql, column, method):
	sql += f" ORDER BY {column} {method}"
	return sql


def fetch(table) -> list:
	conn: sqlite3.Connection = get_db_connection()
	sql = sql_from(sql_select('*'), table)
	result: list = conn.execute(sql).fetchall()
	conn.close()
	return result


def fetch_id(table, id) -> dict:
	conn: sqlite3.Connection = get_db_connection()
	sql = sql_where(sql_from(sql_select('*'), table), 'id', id)
	result: dict = conn.execute(sql).fetchone()
	conn.close()
	return result


def fetch_condition(table, column, condition) -> list:
	conn: sqlite3.Connection = get_db_connection()
	sql = sql_where(sql_from(sql_select('*'), table), column, condition)
	result: list = conn.execute(sql).fetchall()
	conn.close()
	return result

def fetch_condition_ordered(table, column, condition, order_column, order) -> list:
	conn: sqlite3.Connection = get_db_connection()
	sql = sql_order(sql_where(sql_from(sql_select('*'), table), column, condition), order_column, order)
	result: list = conn.execute(sql).fetchall()
	conn.close()
	return result


def table_info(table):
	conn: sqlite3.Connection = get_db_connection()
	sql = f"PRAGMA foreign_key_list({table});"
	result: list = conn.execute(sql).fetchall()
	conn.close()
	return result
