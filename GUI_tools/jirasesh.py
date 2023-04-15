#!/usr/bin/env python3
import sys
import yaml
import pprint
from copy import deepcopy
from jira import JIRA
from validator import Validator
import default_auth_constants as constants

class JiraInst():
    #Constructor
    def __init__(self):
        #Connect to jira and initiate session
        self.jira_session = JIRA(constants.SITE, basic_auth=(constants.EMAIL, constants.API_TOKEN))

        #import configure varibles
        with open('config_files/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self._states = config["states"]

    #Gets JIRA open or future issues for a given user
    def get_issues(self, assignee, search_state = None):
        issue_list = {}

        if search_state is None:
            for s in self._states:
                state_in_JQL = '\"' + s + '\"'
                query_JQL = 'assignee = \"' + assignee + '\" and sprint in (openSprints(),futureSprints()) and status = ' + state_in_JQL
                issue_list[s] = self.jira_session.search_issues(query_JQL)
        else:
            state_in_JQL = '\"' + search_state + '\"'
            query_JQL = 'assignee = \"' + assignee + '\" and sprint in (openSprints(),futureSprints()) and status = ' + state_in_JQL
            issue_list = self.jira_session.search_issues(query_JQL)

        return issue_list
    
    #Changes states of issues for a given user. 
    def change_state(self, assignee, final_state, initial_state = None, issues_2_change = None):            
        if initial_state is None:
            initial_state = self._states[0]

        if issues_2_change is None:
            issue_list = self.get_issues(assignee,initial_state)
        else:
            issue_list = issues_2_change

        try:
            for issue in issue_list:    
                self.jira_session.transition_issue(issue.key, final_state)
            return True
        except:
            return False
            
    def  log_hours(self, l0, ca, jira_session):    
        if (l0 or ca):
            IssuesStatus = "In Progress"
        else:
            IssuesStatus = "To Do"
            
        issue_list = jira_session.search_issues('assignee = currentUser() \
        and sprint in openSprints() and status = '+ IssuesStatus)
        
        #If it doesn't exist
        if len(issue_list) == 0:
            issue_list = jira_session.search_issues('assignee = currentUser() \
            and sprint in futureSprints() and status = '+ IssuesStatus)

            
        #Search Issues
        for issue in issue_list:
            #Transitions       
            if ca:
                jira_session.transition_issue(issue.key, "Resolved")
            elif not l0:
                jira_session.transition_issue(issue.key, "In Progress")
            
            #add 0 hours
            if (l0 or not ca): 
                jira_session.add_worklog(issue.key, timeSpent="0h")
                jira_session.add_worklog(issue.key, timeSpent="0h", started = (datetime.now() + timedelta(days = 7)))            #add 0 hours a week later

        click.echo("Done")

    # def upload(self, closed_sprints, prompt, duplicates, fatal_errors, verbose, pageview,
    #         dry_run, prepend_sprint, config):
    #     """Use TOKEN to connect to Jira site and upload issues from CONFIG."""
    #     # parse yaml into list of story, task, bugs
    #     config = yaml.load(config, Loader=yaml.Loader)
    #     issues = []

    #     try:
    #         for issue_cfg in config['issues']:
    #             issue = deepcopy(config['defaults'])
    #             issue.update(issue_cfg)
    #             issues.append(issue)

    #     except KeyError as err:
    #         click.secho("Config is missing key '{}'".format(err.args[0]), err=True)

    #     # validate issues
    #     v = Validator(jira, fatal_errors=fatal_errors, verbose=verbose,
    #                 duplicates=duplicates, closed_sprints=closed_sprints,
    #                 prepend_sprint=prepend_sprint)
    #     vissues = v.validate(issues)

    #     if len(vissues) == 0:
    #         click.secho("No issues to upload after validation.", err=True, fg='red')
    #         return

    #     # Handle various options
    #     result = ("Validated {} issues in projects {}. "
    #             .format(len(vissues), set(vi['project'] for vi in vissues)))
    #     if pageview:
    #         click.echo_via_pager(result + "\n\n"
    #             + pprint.pformat({issue['summary']: issue for issue in vissues}))
    #     if dry_run or (prompt and not click.confirm("\n" + result + "Proceed?")):
    #         return

    #     results = []
    #     with click.progressbar(
    #         vissues,
    #         label='Creating issues via the Jira API...',
    #         # item_show_func=lambda i: i['summary'],
    #     ) as bar:
    #         for issue in bar:
    #             sprint_id = issue.pop('sprint').id
    #             epic_id = issue.pop('epic').id
    #             board = issue.pop('board')

    #             res = jira.create_issue(issue)
    #             results.append(res)
    #             jira.add_issues_to_sprint(sprint_id=sprint_id,
    #                                     issue_keys=[res.key])

    #             # the add_issues_to_epic API appears to be deprecated
    #             try:
    #                 jira.add_issues_to_epic(epic_id=epic_id,
    #                                         issue_keys=[res.key])
    #             except NotImplementedError:
    #                 res.update(fields={'parent': {'id': epic_id}})

    #             jira.add_worklog(res.key, timeSpent="0h")
    #             #jira.transitions(res)

                
    #     for res in results:
    #         click.secho("Created issue {!r}".format(res))


    #     # if failed, prompt to launch editor
    #     # run sprint selector
    #     # if dry-run or verbose, print final issues
    #     # if not dry-run upload with jira authenticator
    #     return 0

if __name__ == "__main__":
    a = JiraInst()
    print(a._states)
    issue = a.get_issues('Caleb Ho','To Do')
    # issue = a.get_issues('Caleb Ho','Blocked')
    print(issue)
    #To Do -> Blocked works but not vice versa for change_state
    # print(a.change_state(assignee = 'Caleb Ho', final_state = 'To Do', issues_2_change = issue))
    print(a.change_state(assignee = 'Caleb Ho', final_state = 'Blocked', issues_2_change = issue))