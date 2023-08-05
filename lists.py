from flask import render_template
import sqlite3
from typing import List
from flask import Flask
from db import fetch, table_list


def main_lists(app: Flask):
	@app.route("/list/criminals")
	def criminals() -> str:
		criminals: List[sqlite3.Row] = fetch('criminals')
		return render_template('lists/criminals.html', criminals=criminals)

	@app.route("/list/cases")
	def cases() -> str:
		cases: List[sqlite3.Row] = fetch('cases')
		return render_template('lists/cases.html', cases=cases)

	@app.route("/list/works")
	def works() -> str:
		works: List[sqlite3.Row] = fetch('works')
		return render_template('lists/works.html', works=works)

	@app.route("/list/edits")
	def edits() -> str:
		tables: List[sqlite3.Row] = table_list()
		return render_template('lists/edits.html', tables=tables)
