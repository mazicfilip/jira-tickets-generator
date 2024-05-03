# Jira Ticket Generator API

## Description
This is a FastAPI-based API application for generating Jira tickets with Rivian-themed data. It provides endpoints to create Jira tickets in a specified project and customize ticket details.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/mazicfilip/jira-tickets-generator.git
    ```
2. Navigate to the project directory:
    ```bash
    cd jira-tickets-generator
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Set up your Jira instance and obtain API credentials.
2. Update the configuration in `config.py` with your Jira URL and project key.
3. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```
4. Access the Swagger documentation at `http://localhost:8000/docs` to view available endpoints and interact with the API.

## Endpoints

### Generate Tickets
- **URL**: `/generate`
- **Method**: `POST`
- **Description**: Generates new Jira tickets with Rivian-themed data.
- **Request Body**: JSON data containing ticket details.
    ```json
    [
        {
            "summary": "Rivian R1T Review",
            "description": "The Rivian R1T is an electrifying addition to the pickup truck market, combining innovative technology with rugged capabilities.",
            "file_path": "optional\\file\\path"
        },
        {
            "summary": "Rivian R1S Launch Event",
            "description": "Join us for the exciting launch event of the Rivian R1S, an all-electric SUV revolutionizing the automotive industry."
        }
    ]
    ```
- **Response**: JSON data containing details of the generated tickets.

### Webhook for Notifications
- **URL**: `/webhooks/send_notification/{issue_id}`
- **Method**: `POST`
- **Description**: Sends a notification when a comment is deleted from a Jira issue.
- **Parameters**:
    - `issue_id` (str): ID of the Jira issue.
- **Response**: JSON data indicating success or failure of the notification.

## Docker Support
This project includes Docker support for containerization. To build and run the Docker container, use the following commands:
```bash
docker build -t jira-ticket-api .
docker run -d -p 8000:8000 jira-ticket-api