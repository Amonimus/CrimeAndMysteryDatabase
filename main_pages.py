from flask import Flask
from flask import render_template


def main_pages(app: Flask):
	@app.route("/")
	def index() -> str:
		return render_template('main/index.html')

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('main/404.html'), 404
