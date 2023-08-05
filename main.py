from flask import Flask

from app import app
from articles import main_artciles
from filters import main_filters
from lists import main_lists
from main_pages import main_pages
from tech import main_tech


def create_app() -> Flask:
	main_pages(app)
	main_artciles(app)
	main_lists(app)
	main_tech(app)
	main_filters(app)
	return app


if __name__ == '__main__':
	app: Flask = create_app()
	app.run(host='0.0.0.0', port=5000, debug=True)
