import sqlite3
from typing import List

from flask import Flask
from flask import render_template

from db import fetch, table_info, column_list


def main_tech(app: Flask):
	@app.route("/edit/<string:table>")
	def edit(table) -> str:
		table_data: List[sqlite3.Row] = fetch(table)
		foreign_keys: List[sqlite3.Row] = table_info(table)[0]
		data_list: List[dict] = [dict(data) for data in table_data]
		columns: List[sqlite3.Row] = column_list(table)
		return render_template('edit.html', columns=columns, table_name=table, table=data_list, keys=foreign_keys)
