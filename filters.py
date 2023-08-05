import sqlite3
from typing import Union

from flask import Flask

from db import fetch_condition, table_info


def main_filters(app: Flask):
	@app.template_filter('fk')
	def foreign_key(id: int, table: str, column: str) -> Union[int, sqlite3.Row]:
		result = id
		for column_info in table_info(table):
			if column == column_info['from']:
				result: sqlite3.Row = fetch_condition(column_info['table'], column_info['to'], str(id))[0]
				break
		return result
