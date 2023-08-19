import sqlite3
from typing import List

from flask import Flask
from flask import render_template
from flask import request

from db import fetch, get_foreign_keys, get_table_info, insert, update


def is_fk(column: str, keys: list) -> bool:
    key_list: list = [key["from"] for key in keys]
    return column in key_list


def get_fk(table):
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
    return foreign_keys


def insert_values(request, foreign_keys):
    data = dict(request.values)
    insert_table = data["table"]
    del data["table"]
    del data["action"]
    for key in data.keys():
        if is_fk(key, foreign_keys):
            if data[key] != '':
                data[key] = int(data[key])
        if data[key] == '':
            data[key] = None
    insert(insert_table, data)


def update_values(request, foreign_keys):
    data = dict(request.values)
    insert_table = data["table"]
    del data["table"]
    del data["action"]
    for key in data.keys():
        if is_fk(key, foreign_keys):
            if data[key] != '':
                data[key] = int(data[key])
        if data[key] == '':
            data[key] = None
    update(insert_table, data)


def main_tech(app: Flask):
    @app.route("/edit/<string:table_name>", methods=["GET", "POST"])
    def edit(table_name) -> str:
        foreign_keys = get_fk(table_name)
        if request.method == 'POST':
            if request.values["action"] == "add":
                insert_values(request, foreign_keys)
            if request.values["action"] == "update":
                update_values(request, foreign_keys)
        table_data: List[sqlite3.Row] = fetch(table_name)
        data_list: List[dict] = [dict(data) for data in table_data]
        columns: List[sqlite3.Row] = get_table_info(table_name)
        columns = [dict(column) for column in columns]
        columns_types = dict()
        for idx, column in enumerate(columns):
            if column["name"] in [fk['from'] for fk in foreign_keys]:
                columns_types[column["name"]] = "FK"
                columns[idx]["type"] = "FK"
            else:
                columns_types[column["name"]] = column["type"]
        for row in data_list:
            for key, value in row.items():
                if key in columns_types:
                    row[key] = {"type": columns_types[key], "value": value}

        return render_template('edit.html', columns=columns, table_name=table_name, table=data_list,
                               fk_keys=foreign_keys)
