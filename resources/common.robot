*** Settings ***
Library     ..${/}library${/}utils.py
Variables   ..${/}variables.py
Library     ..${/}library${/}DataBase.py  ${DB_PATH}
Resource    keywords.robot