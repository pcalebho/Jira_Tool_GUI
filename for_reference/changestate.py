from jira import JIRA
import click
from datetime import datetime
from datetime import timedelta

#### HOW TO USE ####
#Make sure Bastian Email is correct
#example command: python -m jira_tools.changestate secrets/token.txt  
#Moves Current Sprint ToDo issues into In Progress and adds 0 hours

#example command: python -m jira_tools.changestate --l0 secrets/token.txt 
#adds 0 hours to all In Progress issues

#example command: python -m jira_tools.changstate --ca secrets/token.txt
#transitions all In Progress issues to Resolved/Completed

site = "https://bastiansolutionslab1.atlassian.net"
email = "cho@bastiansolutions.com"              #CHANGE TO YOUR BASTIAN EMAIL

@click.command()
@click.option('--l0', is_flag=True)         #option to add only l0 to 
@click.option('--ca', is_flag=True)           #option to close in progress issues
@click.argument('token', type=click.File('r'))

def change(l0,ca,token):
    token_text = token.read().strip()
    #Search ToDo issues in current spring
    jira_connection = JIRA(site, basic_auth=(email, token_text))    
    
    if (l0 or ca):
        IssuesStatus = '"In Progress"'
    else:
        IssuesStatus = '"To Do"'
        
    issue_list = jira_connection.search_issues('assignee = currentUser() \
    and sprint in openSprints() and status = '+ IssuesStatus)
    
    #If it doesn't exist
    if len(issue_list) == 0:
        issue_list = jira_connection.search_issues('assignee = currentUser() \
        and sprint in futureSprints() and status = '+ IssuesStatus)

        
   #Search Issues
    for issue in issue_list:
         #Transitions       
        if ca:
            jira_connection.transition_issue(issue.key, "Resolved")
        elif not l0:
            jira_connection.transition_issue(issue.key, "In Progress")
        
        #add 0 hours
        if (l0 or not ca): 
            jira_connection.add_worklog(issue.key, timeSpent="0h")
            jira_connection.add_worklog(issue.key, timeSpent="0h", started = (datetime.now() + timedelta(days = 7)))            #add 0 hours a week later

    click.echo("Done")
    
if __name__ == '__main__':
    change()