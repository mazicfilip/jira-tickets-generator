from typing import List, Dict, Annotated

from fastapi import APIRouter, Request, Depends

from app.auth.utils import oauth2_scheme
from app.config import LIMIT
from app.jira.utils import create_jira_ticket, create_notification
from app.models.ticket import TicketDataRequest, TicketDataResponse
from app.routers.limiter import limiter

router = APIRouter(
    prefix="",
)


@router.post("/generate")
@limiter.limit(LIMIT)
async def generate_tickets(
        request: Request,
        ticket_data: List[TicketDataRequest],
        token: Annotated[str, Depends(oauth2_scheme)]) -> List[TicketDataResponse]:
    tickets: List[TicketDataResponse] = []
    for data in ticket_data:
        tickets.append(create_jira_ticket(data))
    return tickets


@router.post("/webhooks/send_notification/{issue_id}")
@limiter.limit(LIMIT)
async def send_notification(
        request: Request,
        issue_id: str) -> Dict[str, str]:
    create_notification(issue_id)
    return {"message": "Notification sent"}
