import sqlite3


def create_employee_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS employees(id integer, name, id_team)')

    connection.commit()
    connection.close()


def create_project_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS projects(id integer, project_number text, project_name text,'
                   'project_description text, start_date text, end_date text)')

    connection.commit()
    connection.close()


def create_teams_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS teams(id integer, team_name text, team_leader text)')

    connection.commit()
    connection.close()


def create_employees_projects_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS employees_projects(id_employee integer, id_project integer,'
                   ' time integer)')

    connection.commit()
    connection.close()


def add_employee(employee_id, employee_name, id_team):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO employees VALUES(?, ?, ?)', (employee_id, employee_name, id_team))

    connection.commit()
    connection.close()



def add_project(project_id, project_number, project_name, project_description, start_date, end_date):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO projects VALUES(?, ?, ?, ?, ?, ?)', (project_id, project_number, project_name,
                                                                     project_description, start_date, end_date))

    connection.commit()
    connection.close()


def add_team(team_id, team_name, team_leader):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO teams VALUES(?, ?, ?)', (team_id, team_name, team_leader))

    connection.commit()
    connection.close()


def add_hours(employee_id, project_id, time_on_project):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO employees_projects VALUES(?, ?, ?)', (employee_id, project_id, time_on_project))

    connection.commit()
    connection.close()