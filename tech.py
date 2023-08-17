import sqlite3
from typing import List

from flask import Flask
from flask import request
from flask import render_template

from db import fetch, get_foreign_keys, get_table_info, insert

def is_fk(column: str, keys: list) -> bool:
	key_list: list = [key["from"] for key in keys]
	return column in key_list

def main_tech(app: Flask):
	@app.route("/edit/<string:table>", methods=["GET", "POST"])
	def edit(table) -> str:
		fkinfo: list = get_foreign_keys(table)
		foreign_keys = []
		for fk in fkinfo:
			foreign_keys.append(
				{
					"from": fk["from"],
					"table": fk["table"],
					"to": fk["to"],
				}
			)

		if request.method == 'POST':
			data = dict(request.values)
			insert_table = data["table"]
			del data["table"]
			for key in data.keys():
				if is_fk(key, foreign_keys):
					if data[key] != '':
						data[key] = int(data[key])
					else:
						data[key] = None
			insert(insert_table, data)

		table_data: List[sqlite3.Row] = fetch(table)
		data_list: List[dict] = [dict(data) for data in table_data]
		columns: List[sqlite3.Row] = get_table_info(table)
		return render_template('edit.html', columns=columns, table_name=table, table=data_list, keys=foreign_keys)
