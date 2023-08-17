import sqlite3
from typing import Union

from flask import Flask

from db import fetch_condition, get_foreign_keys, fetch


def main_filters(app: Flask):
	@app.template_filter('fk')
	def foreign_key(id: int, table: str, column: str) -> Union[int, sqlite3.Row]:
		result = id
		if id is not None:
			for column_info in get_foreign_keys(table):
				if column == column_info['from']:
					result: sqlite3.Row = fetch_condition(column_info['table'], column_info['to'], str(id))[0]
					break
		else:
			result = ""
		return result

	@app.template_filter('is_fk')
	def is_fk(column: str, keys: list) -> bool:
		key_list: list = [key["from"] for key in keys]
		return column in key_list
	@app.template_filter('get_fk_values')
	def get_fk_values(column: str, keys: list) -> list:
		results = []
		for key in keys:
			if column == key["from"]:
				results = fetch(key["table"])
				break
		return results