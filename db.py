import sqlite3
from typing import List


def get_db_connection():
	conn: sqlite3.Connection = sqlite3.connect('database.db')
	conn.isolation_level = None
	conn.execute("PRAGMA foreign_keys = 1")
	conn.row_factory = sqlite3.Row
	return conn


def sql_select(rows: str) -> str:
	return f"SELECT {rows}"


def sql_from(sql: str, table: str) -> str:
	sql += f" FROM {table}"
	return sql


def sql_where(sql: str, column: str, condition: str) -> str:
	sql += f" WHERE {column}={condition}"
	return sql


def sql_order(sql: str, column: str, method: str) -> str:
	sql += f" ORDER BY {column} {method}"
	return sql


def query(func):
	def wrapper(*args, **kwargs) -> List[sqlite3.Row]:
		conn: sqlite3.Connection = get_db_connection()
		sql: str = func(*args)
		result: List[sqlite3.Row] = conn.execute(sql).fetchall()
		conn.close()
		return result

	return wrapper


@query
def fetch(table: str) -> List[sqlite3.Row]:
	return sql_from(sql_select('*'), table)


@query
def fetch_id(table: str, id: int) -> List[sqlite3.Row]:
	return sql_where(sql_from(sql_select('*'), table), 'id', id)


@query
def fetch_condition(table: str, column: str, condition: str) -> List[sqlite3.Row]:
	return sql_where(sql_from(sql_select('*'), table), column, condition)


@query
def fetch_condition_ordered(table: str, column: str, condition: str, order_column: str, order: str) -> List[
	sqlite3.Row]:
	return sql_order(sql_where(sql_from(sql_select('*'), table), column, condition), order_column, order)

# @query
# def insert(table: str, data: dict):
# 	columns = (str(list(data.keys()))[1:-1])
# 	values = (str(list(data.values()))[1:-1])
# 	sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
# 	print(sql)
# 	return sql

def insert(table: str, data: dict):
	columns = ', '.join(data.keys())
	placeholders = ', '.join('?' * len(data))
	sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)
	values = [int(x) if isinstance(x, bool) else x for x in data.values()]

	conn: sqlite3.Connection = get_db_connection()
	result: List[sqlite3.Row] = conn.execute(sql, values).fetchall()

	conn.close()
	return result

def update(table: str, data: dict):
	row_id = data["id"]
	del data["id"]
	sql = 'UPDATE {} SET {} WHERE id={}'.format(table, ', '.join('{}=?'.format(k) for k in data), row_id)
	values = [int(x) if isinstance(x, bool) else x for x in data.values()]

	conn: sqlite3.Connection = get_db_connection()
	result: List[sqlite3.Row] = conn.execute(sql, values).fetchall()

	conn.close()
	return result


@query
def get_foreign_keys(table: str) -> List[sqlite3.Row]:
	return f"PRAGMA foreign_key_list({table});"


@query
def get_table_info(table: str) -> List[sqlite3.Row]:
	return f"PRAGMA table_info({table});"


@query
def get_table_list() -> List[sqlite3.Row]:
	return f"PRAGMA table_list;"
