#!/usr/bin/env python3
import yaml
import pdb

import click
from jira import JIRA


@click.command()
@click.argument('token', type=click.File('r'))
def test(token):
    token_text = token.read().strip()
    jira = JIRA("https://bastianmobilerobotics.atlassian.net",
                basic_auth=('mallain@bastiansolutions.com', token_text))

    # jira = JIRA("https://bastiansolutionslab1.atlassian.net/",
    #             basic_auth=('mallain@bastiansolutions.com',
    #                         'jZ8gKL1o50XGvDGnTt6GC429'))

    # MANUAL CREATION
    # jira.create_issue(project="TP", summary="This is a test story",
    #                   description="Be careful with fire.",
    #                   issuetype={'name': 'Story'})

    # BULK CREATION
    with open('../templates/test_project_example.yaml', 'r') as readfile:
        issue_dicts = yaml.load(readfile, Loader=yaml.Loader)

    issues = []
    for issue_dict in issue_dicts:
        issues.append(jira.create_issue(fields=issue_dict))

    jira.add_issues_to_sprint(sprint_id=2,
                              issue_keys=[i.key for i in issues])

    # getting sprints, only returns 50 despite maxResults
    # sprints = jira.sprints(board_id=8, startAt=40)

    # getting components
    # components = jira.project_compoonents(project='TP')

    # getting projects
    # projects = jira.projects()

    # retrieving issues
    # issues = jira.issue('TP-1')

    # ultra board is 46
    # overhead board is


if __name__ == "__main__":
    test()
