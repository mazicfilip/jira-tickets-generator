from requests.auth import HTTPBasicAuth

from app.config import JIRA_EMAIL, JIRA_API_TOKEN


def jira_authentication():
    return HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
