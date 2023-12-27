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
         'start_date': '12.12.2023', 'end_date': '14.12.2024'},
    1:
        {'project_number': 'R101', 'project_name': 'Kółeczka', 'project_description': 'Kółka na półkę',
        'start_date': '13.01.2024', 'end_date': '30.12.2024'},
    }

teams = {
    0:
        {'team_name': 'Bytowy team', 'team_leader': 'Mati Mass'}
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


# @app.route('/check_hours')
# def check_hours():
#     return 'check_hours'


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


# @app.route('/arch')
# def arch():
#     return 'arch'


@app.route('/employees/<int:employee_id>')
def employee(employee_id):
    employee = employees.get(employee_id)
    if not employee:
        return render_template('404.html', message=f'A employee with id {id} was not found.')
    if 'projects_emp' not in employees[employee_id].keys():
        return render_template('employee_without_hours.html', employee=employee)
    else:
        return render_template('employee.html', employee=employee)


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

    return render_template('team.html', team=team)

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


@app.route("/employees/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        team = request.form.get('team')
        employee_id = len(employees)
        employees[employee_id] = {'employee_id': employee_id, 'name': name, 'team': team}

        return redirect(url_for('employee', employee_id=employee_id))
        #przekierowuje nas na tę stronę którą stworzyliśmy
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
                          'team_leader': team_leader}
        return redirect(url_for('team', team_id=team_id))
    return render_template('add_team.html')

if __name__ == '__main__':
    app.run(debug=True)
