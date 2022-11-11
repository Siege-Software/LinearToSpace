import requests

from linear import linear_endpoint, linear_headers, projects_query, statuses
from space import jetbrains_headers, jetbrains_endpoint


def check_project_exists(project_key: str):
    """
    Check if a project with the provided key exists on Jetbrains Space

    :param project_key: The project key
    :return: jetbrains project_id if the project exists
    """
    res = requests.get(url=f"{jetbrains_endpoint}/projects/key:{project_key}", headers=jetbrains_headers)
    if res.status_code == 200:
        print(f'The project with details {project} already exists on Jetbrains Space')
        return res.json()['id']
    else:
        return None


def create_project(project_data: dict):
    """
    Create a project if it does not exist of JetBrains Space.

    :param project_data: A dictionary containing the project data from Linear
    :return:
        Returns a tuple of (project_id, created), where project_id is the retrieved or created project id and
        created is a boolean specifying whether a new project was created.
    """
    project_key = project_data['name'].upper()
    jetbrains_project_id = check_project_exists(project_key)
    if jetbrains_project_id:
        return jetbrains_project_id, False

    data = {
        "key": {"key": project_key},
        "name": project_data['name'],
        "description": project_data['description']
    }
    res = requests.post(url=f"{jetbrains_endpoint}/projects", headers=jetbrains_headers, json=data)
    if res.status_code == 200:
        jetbrains_project_id = res.json()['id']
        print(f'Project created successfully with id: {jetbrains_project_id}')
    else:
        jetbrains_project_id = None
        print(f'{res.text}')

    return jetbrains_project_id, True


def get_issue_statuses(jetbrains_project_id: str):
    """
    Get the issue statuses for a project. The object of this is to get the status id that matches this project's id

    :param jetbrains_project_id: The Jetbrains Space Project id
    :return: A list of dictionaries containing each status data
    """
    res = requests.get(
        url=f"{jetbrains_endpoint}/projects/id:{jetbrains_project_id}/planning/issues/statuses",
        headers=jetbrains_headers,
    )
    return res.json()


def update_issue_statuses(jetbrains_project_id: str):
    """
    Jetbrains Space has pre-existing status. This methods overwrites the statuses or a Jetbrains Project using data
    obtained from Linear statuses

    :param jetbrains_project_id: The Jetbrains Space Project id
    :return: None
    """
    statuses_data = {"statuses": []}

    for key, values in statuses.items():
        statuses_data['statuses'].append(values | {'name': key})

    res = requests.patch(
        url=f"{jetbrains_endpoint}/projects/id:{jetbrains_project_id}/planning/issues/statuses",
        headers=jetbrains_headers,
        json=statuses_data
    )
    print(res.text)


def create_issue(issue_data: dict, jetbrains_project_id: str, issue_statuses):
    """
    Create an issue for a Space Project using data from Linear

    :param issue_data: A dictionary of the issue data as obtained on Linear
    :param jetbrains_project_id: The Jetbrains Space Project id
    :param issue_statuses: A list of dictionaries containing each status data from Jetbrains.
    :return: None
    """
    assignee_username = issue_data.get('assignee', {}).get('email', '').split('@')[0]
    linear_status_name = issue_data['state']['name'].lower()
    for status_data in issue_statuses:
        if status_data['name'].lower() == linear_status_name:
            status_id = status_data['id']
            break
    else:
        raise Exception('Status Not Found')

    data = {
        "title": issue_data['title'],
        "description": issue_data['description'],
        "assignee": f"username:{assignee_username}",
        "status": status_id,
    }
    res = requests.post(
        url=f"{jetbrains_endpoint}/projects/id:{jetbrains_project_id}/planning/issues",
        headers=jetbrains_headers,
        json=data
    )
    print(res.text)


def import_project_issues(linear_project_id: str, jetbrains_project_id: str):
    """
    Create all issues from a Linear Project to its equivalent on Jetbrains Space

    :param linear_project_id: The Linear Project id
    :param jetbrains_project_id: The Jetbrains Space Project id
    :return:
    """
    issues_query = f"""
        query Project {{
            project(id: "{linear_project_id}") {{
                issues {{
                     nodes {{
                         title
                         description
                         assignee {{
                             email
                         }}
                         state {{
                             name
                         }}
                         priority
                         priorityLabel
                    }}
                }}
            }}
        }}
        """
    res = requests.post(linear_endpoint, headers=linear_headers, json={'query': issues_query})
    project_issues = res.json()['data']['project']['issues']['nodes']
    issue_statuses = get_issue_statuses(jetbrains_project_id)
    for project_issue in project_issues:
        create_issue(project_issue, jetbrains_project_id, issue_statuses)


if __name__ == '__main__':
    response = requests.post(linear_endpoint, headers=linear_headers, json={'query': projects_query})
    linear_projects = response.json()['data']['projects']['nodes']
    for project in linear_projects:
        jetbrains_project_id, created = create_project(project)
        if not jetbrains_project_id:
            print(f'Could not create project with details: {project}')
            continue

        if not created:
            print("This project already exists. Skipping creating it's issues to avoid duplicates")
            continue

        update_issue_statuses(jetbrains_project_id)
        import_project_issues(project['id'], jetbrains_project_id)
