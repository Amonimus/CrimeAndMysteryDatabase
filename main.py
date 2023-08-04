from flask import Flask, render_template

from app import app
from db import fetch, fetch_id, fetch_condition, table_info, fetch_condition_ordered


def create_app() -> Flask:
	@app.route("/")
	def index() -> str:
		return render_template('index.html')

	@app.route("/criminal/<int:id>")
	def criminal(id) -> str:
		criminal = fetch_condition('criminals', 'id', id)[0]
		felonies = fetch_condition_ordered('felonies', 'culprit_id', criminal["id"], 'case_order', 'ASC')
		return render_template('criminal.html', criminal=criminal, felonies=felonies)

	@app.route("/case/<int:id>")
	def case(id) -> str:
		case = fetch_condition('cases', 'id', id)[0]
		felonies = fetch_condition_ordered('felonies', 'case_id', case["id"], 'case_order', 'ASC')
		return render_template('case.html', case=case, felonies=felonies)

	@app.route("/work/<int:id>")
	def work(id) -> str:
		work = fetch_condition('works', 'id', id)[0]
		cases = fetch_condition('cases', 'work_id', work["id"])
		return render_template('work.html', work=work, cases=cases)

	@app.route("/list/criminals")
	def criminals() -> str:
		criminals: list = fetch('criminals')
		return render_template('criminals.html', criminals=criminals)

	@app.route("/list/cases")
	def cases() -> str:
		cases: list = fetch('cases')
		return render_template('cases.html', cases=cases)

	@app.route("/list/works")
	def works() -> str:
		works: list = fetch('works')
		return render_template('works.html', works=works)

	@app.route("/edit/<string:table>")
	def edit(table) -> str:
		table_data = fetch(table)
		return render_template('edit.html', table=table_data)

	@app.template_filter('fk')
	def foreign_key(id, table, column):
		result = id
		for column_info in table_info(table):
			print(id, table, column)
			if column == column_info['from']:
				result = fetch_condition(column_info['table'], column_info['to'], id)[0]
				break
		return result

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'), 404

	return app


if __name__ == '__main__':
	app: Flask = create_app()
	app.run(host='0.0.0.0', port=5000, debug=True)
