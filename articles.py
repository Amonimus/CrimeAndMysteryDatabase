import sqlite3
from typing import List

from flask import Flask
from flask import render_template

from db import fetch_condition, fetch_condition_ordered


def main_artciles(app: Flask):
	@app.route("/criminal/<int:id>")
	def criminal(id: int) -> str:
		criminal: sqlite3.Row = fetch_condition('criminals', 'id', str(id))[0]
		felonies: List[sqlite3.Row] = fetch_condition_ordered('felonies', 'culprit_id', criminal["id"], 'case_order',
															  'ASC')
		return render_template('articles/criminal.html', criminal=criminal, felonies=felonies)

	@app.route("/case/<int:id>")
	def case(id: int) -> str:
		case: sqlite3.Row = fetch_condition('cases', 'id', str(id))[0]
		felonies: List[sqlite3.Row] = fetch_condition_ordered('felonies', 'case_id', case["id"], 'case_order', 'ASC')
		return render_template('articles/case.html', case=case, felonies=felonies)

	@app.route("/work/<int:id>")
	def work(id: int) -> str:
		work: sqlite3.Row = fetch_condition('works', 'id', str(id))[0]
		cases: List[sqlite3.Row] = fetch_condition('cases', 'work_id', work["id"])
		return render_template('articles/work.html', work=work, cases=cases)
