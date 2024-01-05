from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
employees = {}
#     {
#     0:
#         {'name': "Mati Bombalski", 'team': "Słoniowski Team", 'projects_emp':
#             {0: {'project_name': 'R100 - Rowerki', 'project_time': 20}}}
#     }

projects = {
    0:
        {'project_number': 'R100', 'project_name': 'Rowerki', 'project_description': 'Rowerki do jeżdżenia',
         'start_date': '2023-12-30', 'end_date': '2024-12-30'},
    1:
        {'project_number': 'R101', 'project_name': 'Kółeczka', 'project_description': 'Kółka na półkę',
            'start_date': '2024-01-12', 'end_date': '2024-06-12'},
    2:
        {'project_number': 'R102', 'project_name': 'Kwadraciki', 'project_description': 'Kwadraciki na półkę',
         'start_date': '2025-01-12', 'end_date': '2030-06-12'},
    }

teams = {
    0:
        {'team_name': 'Bytowy team', 'team_leader': 'Mati Mass', 'team_members': []},
    1:
        {'team_name': 'Pożarowy team', 'team_leader': 'Robi Bobi', 'team_members': []},
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hours')
def add_hours():
    if len(employees) == 0:
        return render_template('no_employee_hours.html')
    else:
        return render_template('list_of_employees_hours.html', employees=employees)


@app.route('/employees')
def list_of_employees():
    if len(employees) == 0:
        return render_template('no_employee.html')
    else:
        return render_template('list_of_employees.html', employees=employees)


@app.route('/projects')
def list_of_projects():
    if len(projects) == 0:
        return render_template('no_project.html')
    else:
        return render_template('list_of_projects.html', projects=projects)


@app.route('/teams')
def list_of_teams():
    if len(teams) == 0:
        return render_template('no_team.html')
    else:
        return render_template('list_of_teams.html', teams=teams)


# @app.route('/add_employee')
# def add_employee():
#     return render_template('add_employee.html', teams=teams)


# @app.route('/add_project')
# def add_project():
#     return render_template('add_project.html')


# @app.route('/add_team')
# def add_team():
#     return render_template('add_team.html')


@app.route('/employees/<int:employee_id>')
def employee(employee_id):
    employee = employees.get(employee_id)
    if not employee:
        return render_template('404.html', message=f'A employee with id {id} was not found.')
    return render_template('employee.html', employee=employee, employee_id=employee_id)


@app.route('/projects/<int:project_id>')
def project(project_id):
    project = projects.get(project_id)
    if not project:
        return render_template('404.html', message=f'A project was not found.')

    return render_template('project.html', project=project)


@app.route('/teams/<int:team_id>')
def team(team_id):
    team = teams.get(team_id)
    if not team:
        return render_template('404.html', message=f'A team was not found.')

    return render_template('team.html', team=team, teams=teams, employees=employees)


@app.route("/hours/<int:employee_id>", methods=['GET', 'POST'])
def add_hours_create(employee_id):
    employee = employees.get(employee_id)
    if not employee:
        return render_template('add_employee.html', employee=employee)
    return render_template('add_hours.html', projects=projects, employee_id=employee_id)


@app.route("/hours/create/<int:employee_id>", methods=['GET', 'POST'])
def add_hours_to_employee(employee_id):
    employee = employees.get(employee_id)
    if request.method == 'POST':
        project_name_hours = request.form.get('project_no')
        project_time_hours = request.form.get('time')
        if 'projects_emp' not in employees[employee_id].keys():
            projects_id = 0
            employees[employee_id]['projects_emp'] = {projects_id: {'project_name': project_name_hours,
                                                                    'project_time': project_time_hours}}
        else:
            projects_id = len(employees[employee_id]['projects_emp'])
            employees[employee_id]['projects_emp'][projects_id] = {'project_name': project_name_hours,
                                                                   'project_time': project_time_hours}
        return redirect(url_for('employee', employee_id=employee_id))
    return render_template('add_employee.html')


@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def employee_delete(employee_id):
    employee = employees.get(employee_id)
    if request.method == 'POST':
        for team_id, team_info in teams.items():
            if employee_id in team_info['team_members']:
                team_info['team_members'].remove(int(employee_id))
        del employees[employee_id]
        return redirect(url_for('list_of_employees'))
    return render_template('list_of_employees', employee_id=employee_id)


@app.route("/hours/delete/<int:employee_id>", methods=['POST'])
def hours_delete(employee_id):
    projects_id = request.form.get('projects_id')
    employee = employees.get(employee_id, {})
    project = employee.get('projects_emp', {}).get(int(projects_id))
    if request.method == 'POST':
        if project:
            del employee['projects_emp'][int(projects_id)]
            return redirect(url_for('employee', employee_id=employee_id))
    return render_template('employee.html', employee=employee, employee_id=employee_id)


@app.route('/projects/delete/<int:project_id>', methods=['POST'])
def project_delete(project_id):
    project = projects.get(project_id)
    project_number = project.get('project_number')
    project_name = project.get('project_name')
    project_no = project_number + " - " + project_name
    if request.method == 'POST':
        for emp_id, emp_info in employees.items():
            for emp_project_id, emp_project_info in emp_info['projects_emp'].items():
                if emp_project_info['project_name'] == project_no:
                    return render_template('data_are_used.html', message=f'First remove project '
                                                                         f'from project time in employees.')
        del projects[project_id]
        return redirect(url_for('list_of_projects'))
    return render_template('list_of_projects', project_id=project_id)


@app.route('/teams/delete/<int:team_id>', methods=['POST'])
def team_delete(team_id):
    team = teams.get(team_id)
    team_name = teams.get(team_id).get('team_name')
    if request.method == 'POST':
        for emp_id, emp_info in employees.items():
            if emp_info['team'] == team_name:
                return render_template('data_are_used.html', message=f'First remove employees from this team.')
        del teams[team_id]
        return redirect(url_for('list_of_teams'))
    return render_template('list_of_teams', team_id=team_id)


@app.route("/employees/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        team = request.form.get('team')
        employee_id = len(employees)
        # employees[employee_id] = {'employee_id': employee_id, 'name': name, 'team': team}
        employees[employee_id] = {'name': name, 'team': team, 'projects_emp':{}}
        for team_id, team_info in teams.items():
            if team_info['team_name'] == team:
                team_info['team_members'].append(employee_id)

        return redirect(url_for('employee', employee_id=employee_id))
        # przekierowuje nas na tę stronę którą stworzyliśmy
    return render_template('add_employee.html', teams=teams)


@app.route("/projects/create", methods=['GET', 'POST'])
def project_create():
    if request.method == 'POST':
        project_number = request.form.get('project_number')
        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        project_id = len(projects)
        projects[project_id] = {'project_number': project_number,
                                'project_name': project_name,
                                'project_description': project_description,
                                'start_date': start_date,
                                'end_date': end_date}

        return redirect(url_for('project', project_id=project_id))
    return render_template('add_project.html')


@app.route('/teams/create', methods=['GET', 'POST'])
def team_create():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        team_leader = request.form.get('team_leader')
        team_id = len(teams)
        teams[team_id] = {'team_name': team_name,
                          'team_leader': team_leader,
                          'team_members': []}
        return redirect(url_for('team', team_id=team_id))
    return render_template('add_team.html')


@app.route("/employees/update/<int:employee_id>", methods=['GET', 'POST'])
def employee_update(employee_id):
    employee = employees.get(employee_id)
    if request.method == 'POST':
        return redirect(url_for('employee_modify', employee_id=employee_id))
    return render_template('list_of_employees', employee_id=employee_id)


@app.route("/employees/modify/<int:employee_id>", methods=['GET', 'POST'])
def employee_modify(employee_id):
    employee = employees.get(employee_id)
    if request.method == 'POST':
        name = request.form.get('name')
        team = request.form.get('team')
        # employees[int(employee_id)] = {'employee_id': int(employee_id), 'name': name, 'team': team}
        employees[int(employee_id)]['name'] = name
        employees[int(employee_id)]['team'] = team
        for team_id, team_info in teams.items():
            if int(employee_id) in team_info['team_members']:
                team_info['team_members'].remove(int(employee_id))
            if team_info['team_name'] == team:
                team_info['team_members'].append(employee_id)

        return redirect(url_for('employee', employee_id=employee_id))
        # przekierowuje nas na tę stronę którą stworzyliśmy
    return render_template('modify_employee.html', teams=teams, employee_id=employee_id, employee=employee)


@app.route("/projects/update/<int:project_id>", methods=['GET', 'POST'])
def project_update(project_id):
    project = projects.get(project_id)
    if request.method == 'POST':
        return redirect(url_for('project_modify', project_id=project_id))
    return render_template('list_of_projects', project_id=project_id)


@app.route("/projects/modify/<int:project_id>", methods=['GET', 'POST'])
def project_modify(project_id):
    project = projects.get(project_id)
    project_number = project.get('project_number')
    project_name = project.get('project_name')
    project_no = project_number + " - " + project_name
    if request.method == 'POST':
        new_project_number = request.form.get('project_number')
        new_project_name = request.form.get('project_name')
        new_project_no = new_project_number + " - " + new_project_name
        # for loop change project in employees which are in this team
        for emp_id, emp_info in employees.items():
            for emp_project_id, emp_project_info in emp_info['projects_emp'].items():
                if emp_project_info['project_name'] == project_no:
                    emp_project_info['project_name'] = new_project_no
        project_number = request.form.get('project_number')
        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        projects[int(project_id)] = {'project_number': project_number,
                                     'project_name': project_name,
                                     'project_description': project_description,
                                     'start_date': start_date,
                                     'end_date': end_date}

        return redirect(url_for('project', project_id=project_id))
        # przekierowuje nas na tę stronę którą stworzyliśmy
    return render_template('modify_project.html', project_id=project_id, project=project)


@app.route("/teams/update/<int:team_id>", methods=['GET', 'POST'])
def team_update(team_id):
    team = teams.get(team_id)
    if request.method == 'POST':
        return redirect(url_for('team_modify', team_id=team_id))
    return render_template('list_of_teams', team_id=team_id)


@app.route("/teams/modify/<int:team_id>", methods=['GET', 'POST'])
def team_modify(team_id):
    team = teams.get(team_id)
    team_name = teams.get(team_id).get('team_name')
    if request.method == 'POST':
        # for loop change team in employees which are in this team
        for emp_id, emp_info in employees.items():
            if emp_info['team'] == team_name:
                new_team_name = request.form.get('team_name')
                emp_info['team'] = new_team_name
        team_name = request.form.get('team_name')
        team_leader = request.form.get('team_leader')
        teams[team_id]['team_name'] = team_name
        teams[team_id]['team_leader'] = team_leader

        return redirect(url_for('team', team_id=team_id))
    return render_template('modify_team.html', team_id=team_id, team=team)


if __name__ == '__main__':
    app.run(debug=True)
