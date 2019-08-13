import os
import slack
import json

approvedDomains = [s.strip() for s in open('domainwhitelist.txt').readlines()]

approvedUsers = json.load(open('approvedusers.json'))
    

def valid_email(email): 
    for domain in approvedDomains: 
        if email.endswith('.'+domain) or email.endswith('@'+domain): 
            return True 
    return False 

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
r = client.users_list()
emails = [member['profile'].get('email').lower() for member in r.data['members'] if member['profile'].get('email')] 
emails_not_valid = [email for email in emails if not valid_email(email)]

users = [(member['id'], member['deleted'], member['profile']['real_name'], member['profile']['email'].lower()) for member in r.data['members'] if member['profile'].get('email')]
users_not_valid = [user for user in users if not user[1] and not valid_email(user[3])]
for user in users_not_valid:
    approval = approvedUsers.get(user[0])
    if approval:
        print(f"User {user[0]} called {user[2]} has email address: {user[3]} - Approved by {approval['approvedby']} for {approval['reason']}")
    else:
        print(f"User {user[0]} called {user[2]} has email address: {user[3]} ")
