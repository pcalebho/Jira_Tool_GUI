#!/usr/bin/env python3
import sys
import yaml
import pprint
from copy import deepcopy

import click
from jira import JIRA

from jira_tools.validator import Validator


@click.command()
@click.option('--closed-sprints', '-c', default=False, is_flag=True,
              help="Include closed sprints in search (slower).")
@click.option('--prompt/--no-prompt', '/-n', default=True, is_flag=True,
              help="Whether to prompt before creating new issues")
@click.option('--duplicates/--no-duplicates', '/-w', default=False,
              help="(Not implemented) Check for duplicates before creating issues")
@click.option('--fatal-errors/--skip-errors', '/-k', default=True,
              help="Exit early if validation fails, else create issues which are valid")
@click.option('--verbose', '-v', default=True, is_flag=True,
              help="Show additional debug output")
@click.option('--pageview', '-p', default=False, is_flag=True,
              help="Display validated issues with pager before creation")
@click.option('--dry-run', '-d', default=False, is_flag=True,
              help="Exit before actually creating issues")
@click.option('--prepend-sprint', '-s', default=False, is_flag=True,
              help="Prepend the sprint code to the task with a dash")
@click.argument('token', type=click.File('r'))
@click.argument('config', type=click.File('r'))

def upload(closed_sprints, prompt, duplicates, fatal_errors, verbose, pageview,
           dry_run, prepend_sprint, token, config):
    """Use TOKEN to connect to Jira site and upload issues from CONFIG."""
    # parse yaml into list of story, task, bugs
    config = yaml.load(config, Loader=yaml.Loader)
    issues = []

    try:
        for issue_cfg in config['issues']:
            issue = deepcopy(config['defaults'])
            issue.update(issue_cfg)
            issues.append(issue)

        site = config['site']
        email = config['email']
    except KeyError as err:
        click.secho("Config is missing key '{}'".format(err.args[0]), err=True)

    # setup jira session
    token_text = token.read().strip()
    jira = JIRA(site, basic_auth=(email, token_text))

    # validate issues
    v = Validator(jira, fatal_errors=fatal_errors, verbose=verbose,
                  duplicates=duplicates, closed_sprints=closed_sprints,
                  prepend_sprint=prepend_sprint)
    vissues = v.validate(issues)

    if len(vissues) == 0:
        click.secho("No issues to upload after validation.", err=True, fg='red')
        return

    # Handle various options
    result = ("Validated {} issues in projects {}. "
              .format(len(vissues), set(vi['project'] for vi in vissues)))
    if pageview:
        click.echo_via_pager(result + "\n\n"
            + pprint.pformat({issue['summary']: issue for issue in vissues}))
    if dry_run or (prompt and not click.confirm("\n" + result + "Proceed?")):
        return

    results = []
    with click.progressbar(
        vissues,
        label='Creating issues via the Jira API...',
        # item_show_func=lambda i: i['summary'],
    ) as bar:
        for issue in bar:
            sprint_id = issue.pop('sprint').id
            epic_id = issue.pop('epic').id
            board = issue.pop('board')

            res = jira.create_issue(issue)
            results.append(res)
            jira.add_issues_to_sprint(sprint_id=sprint_id,
                                      issue_keys=[res.key])

            # the add_issues_to_epic API appears to be deprecated
            try:
                jira.add_issues_to_epic(epic_id=epic_id,
                                        issue_keys=[res.key])
            except NotImplementedError:
                res.update(fields={'parent': {'id': epic_id}})

            jira.add_worklog(res.key, timeSpent="0h")
            #jira.transitions(res)

            
    for res in results:
        click.secho("Created issue {!r}".format(res))


    # if failed, prompt to launch editor
    # run sprint selector
    # if dry-run or verbose, print final issues
    # if not dry-run upload with jira authenticator
    return 0


if __name__ == "__main__":
    upload()
