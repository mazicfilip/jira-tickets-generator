import json
import logging
from typing import Dict, Any

import requests
from fastapi import HTTPException

from app.config import JIRA_PROJECT_KEY, JIRA_URL
from app.models.ticket import TicketDataRequest, Payload, Fields, Description, Paragraph, Content, IssueType, Project, \
    TicketDataResponse
from .auth import jira_authentication

logger = logging.getLogger(__name__)


def create_jira_ticket(ticket_data: TicketDataRequest) -> TicketDataResponse:
    logger.info(f"Creating Jira ticket for data: {ticket_data}")

    requests_info = create_jira_ticket_request(ticket_data)
    response = requests.request(**requests_info)

    logger.info(f"Jira ticket creation response status code: {response.status_code}")

    if response.status_code != 201:
        logger.error(f"Failed to create Jira ticket. Response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to create Jira ticket")

    response_data = json.loads(response.text)
    logger.info(f"Jira ticket created successfully. Id: {response_data['id']}")

    if ticket_data.file_path != "":
        add_attachment_on_ticket(response_data["id"], ticket_data.file_path)

    return TicketDataResponse(**response.json())


def create_notification(issue_id: str) -> None:
    logger.info(f"Sending notification for issue id: {issue_id}")

    requests_info = create_notification_request(issue_id)
    response = requests.request(**requests_info)

    logger.info(f"Notification response status code: {response.status_code}")

    if response.status_code != 204:
        logger.error(f"Failed to send notification. Response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to create Jira notification")


def add_attachment_on_ticket(issue_id: str, file_path: str) -> None:
    logger.info(f"Adding attachment to Jira ticket with id: {issue_id}")

    requests_info = create_attachment_request(issue_id, file_path)
    response = requests.request(**requests_info)

    logger.info(f"Attachment response status code: {response.status_code}")

    if response.status_code != 200:
        logger.error(f"Failed to add attachment to Jira ticket. Response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to attach file on Jira ticket")


def create_jira_ticket_request(ticket_data: TicketDataRequest) -> Dict[str, Any]:
    url = f"{JIRA_URL}/issue"
    auth = jira_authentication()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = build_payload(ticket_data)

    return {
        "method": "POST",
        "url": url,
        "data": data,
        "headers": headers,
        "auth": auth
    }


def create_attachment_request(issue_id: str, file_path: str) -> Dict[str, Any]:
    url = f"{JIRA_URL}/issue/{issue_id}/attachments"
    auth = jira_authentication()
    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "no-check"
    }

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
        "auth": auth,
        "files": {
            "file": ("issue_file.txt", open(file_path, "rb"), "application-type")
        }
    }


def create_notification_request(issue_id: str) -> Dict[str, Any]:
    url = f"{JIRA_URL}/issue/{issue_id}/notify"
    auth = jira_authentication()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "htmlBody": "The comment on this issue has been deleted.",
        "restrict": {
            "groupIds": [],
            "permissions": [
                {
                    "key": "BROWSE"
                }
            ]
        },
        "subject": "Comment deleted",
        "textBody": "The comment on this issue has been deleted.",
        "to": {
            "reporter": True
        }
    })

    return {
        "method": "POST",
        "url": url,
        "data": payload,
        "headers": headers,
        "auth": auth
    }


def build_payload(ticket_data: TicketDataRequest) -> json:
    payload = Payload(
        fields=Fields(
            summary=ticket_data.summary,
            description=Description(
                content=[
                    Paragraph(
                        content=[
                            Content(text=ticket_data.description)
                        ]
                    )
                ]
            ),
            issuetype=IssueType(),
            project=Project(id=JIRA_PROJECT_KEY)
        )
    )

    return payload.json()
