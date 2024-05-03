from typing import List

from pydantic import BaseModel, Field


class TicketDataRequest(BaseModel):
    summary: str
    description: str
    file_path: str = ""


class TicketDataResponse(BaseModel):
    id: str
    key: str
    self: str


class Content(BaseModel):
    text: str
    type: str = "text"


class Paragraph(BaseModel):
    content: List[Content]
    type: str = "paragraph"


class Description(BaseModel):
    content: List[Paragraph]
    type: str = "doc"
    version: int = 1


class IssueType(BaseModel):
    name: str = "Task"


class Project(BaseModel):
    id: str


class Fields(BaseModel):
    summary: str
    description: Description
    issuetype: IssueType
    project: Project


class Payload(BaseModel):
    fields: Fields
    update: dict = Field(default={})
