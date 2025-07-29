# app/services/gmail_service.py

import base64
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import httpx
from datetime import datetime
from app.schema.gmail_schema import (
    SendEmailInput, SendEmailOutput,
    GetEmailsInput, GetEmailsOutput,
    ReadEmailInput, ReadEmailOutput,
    SearchEmailsInput, SearchEmailsOutput,
    DeleteEmailInput, DeleteEmailOutput,
    ReplyToEmailInput, ReplyToEmailOutput,
    ForwardEmailInput, ForwardEmailOutput,
    GetLabelsInput, GetLabelsOutput,
    MarkAsReadInput, MarkAsReadOutput,
    MarkAsUnreadInput, MarkAsUnreadOutput,
    Email
)
from app.config import GOOGLE_GMAIL_TOKEN

def get_gmail_service():
    """Get Gmail API service instance"""
    headers = {
        "Authorization": f"Bearer {GOOGLE_GMAIL_TOKEN}",
        "Content-Type": "application/json"
    }
    return headers

def create_message(sender: str, to: str, subject: str, body: str, cc: Optional[str] = None, bcc: Optional[str] = None) -> str:
    """Create a message for an email"""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc
    
    msg = MIMEText(body)
    message.attach(msg)
    
    return base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

def send_email(input: SendEmailInput) -> SendEmailOutput:
    """Send an email using Gmail API"""
    try:
        headers = get_gmail_service()
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        
        # Get user's email address
        user_info_url = "https://gmail.googleapis.com/gmail/v1/users/me/profile"
        user_response = httpx.get(user_info_url, headers=headers)
        user_response.raise_for_status()
        sender_email = user_response.json().get("emailAddress")
        
        if not sender_email:
            return SendEmailOutput(success=False, message="❌ Could not retrieve sender email address")
        
        # Create message
        raw_message = create_message(
            sender=sender_email,
            to=input.to,
            subject=input.subject,
            body=input.body,
            cc=input.cc,
            bcc=input.bcc
        )
        
        payload = {"raw": raw_message}
        response = httpx.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        email_id = response.json().get("id")
        return SendEmailOutput(
            success=True,
            message=f"✅ Email sent successfully to {input.to}",
            email_id=email_id
        )
        
    except Exception as e:
        return SendEmailOutput(success=False, message=f"❌ Error sending email: {str(e)}")

def get_emails(input: GetEmailsInput) -> GetEmailsOutput:
    """Get emails from Gmail"""
    try:
        headers = get_gmail_service()
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        
        params = {
            "maxResults": input.max_results
        }
        
        if input.query:
            params["q"] = input.query
        if input.label:
            params["labelIds"] = input.label
        
        response = httpx.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        messages = response.json().get("messages", [])
        if not messages:
            return GetEmailsOutput(success=True, message="📭 No emails found")
        
        # Get detailed information for each email
        emails = []
        message_lines = ["📧 Recent emails:"]
        
        for msg in messages:
            email_detail = get_email_details(msg["id"], headers)
            if email_detail:
                emails.append(email_detail)
                message_lines.append(f"- {email_detail.subject} from {email_detail.sender} ({email_detail.date})")
        
        return GetEmailsOutput(
            success=True,
            message="\n".join(message_lines),
            emails=emails
        )
        
    except Exception as e:
        return GetEmailsOutput(success=False, message=f"❌ Error fetching emails: {str(e)}")

def get_email_details(email_id: str, headers: dict) -> Optional[Email]:
    """Get detailed information for a specific email"""
    try:
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{email_id}"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        
        msg_data = response.json()
        headers_data = msg_data.get("payload", {}).get("headers", [])
        
        # Extract header information
        subject = next((h["value"] for h in headers_data if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers_data if h["name"] == "From"), "Unknown")
        recipient = next((h["value"] for h in headers_data if h["name"] == "To"), "Unknown")
        date = next((h["value"] for h in headers_data if h["name"] == "Date"), "")
        
        # Extract body
        body = extract_email_body(msg_data.get("payload", {}))
        
        # Check for attachments
        has_attachments = "parts" in msg_data.get("payload", {})
        
        # Extract labels
        labels = msg_data.get("labelIds", [])
        
        return Email(
            id=email_id,
            subject=subject,
            sender=sender,
            recipient=recipient,
            body=body,
            date=date,
            labels=labels,
            has_attachments=has_attachments
        )
        
    except Exception as e:
        print(f"Error getting email details: {str(e)}")
        return None

def extract_email_body(payload: dict) -> str:
    """Extract email body from payload"""
    try:
        if "body" in payload and payload["body"].get("data"):
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    if part["body"].get("data"):
                        return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        
        return "No readable content"
        
    except Exception as e:
        return f"Error extracting body: {str(e)}"

def read_email(input: ReadEmailInput) -> ReadEmailOutput:
    """Read a specific email by ID"""
    try:
        headers = get_gmail_service()
        email_detail = get_email_details(input.email_id, headers)
        
        if not email_detail:
            return ReadEmailOutput(success=False, message="❌ Email not found or could not be read")
        
        return ReadEmailOutput(
            success=True,
            message=f"📧 Email: {email_detail.subject}",
            email=email_detail
        )
        
    except Exception as e:
        return ReadEmailOutput(success=False, message=f"❌ Error reading email: {str(e)}")

def search_emails(input: SearchEmailsInput) -> SearchEmailsOutput:
    """Search emails using Gmail search syntax"""
    try:
        headers = get_gmail_service()
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        
        params = {
            "q": input.query,
            "maxResults": input.max_results
        }
        
        response = httpx.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        messages = response.json().get("messages", [])
        if not messages:
            return SearchEmailsOutput(success=True, message=f"🔍 No emails found for query: {input.query}")
        
        # Get detailed information for each email
        emails = []
        message_lines = [f"🔍 Search results for '{input.query}':"]
        
        for msg in messages:
            email_detail = get_email_details(msg["id"], headers)
            if email_detail:
                emails.append(email_detail)
                message_lines.append(f"- {email_detail.subject} from {email_detail.sender} ({email_detail.date})")
        
        return SearchEmailsOutput(
            success=True,
            message="\n".join(message_lines),
            emails=emails
        )
        
    except Exception as e:
        return SearchEmailsOutput(success=False, message=f"❌ Error searching emails: {str(e)}")

def delete_email(input: DeleteEmailInput) -> DeleteEmailOutput:
    """Delete an email by ID"""
    try:
        headers = get_gmail_service()
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{input.email_id}"
        
        response = httpx.delete(url, headers=headers)
        response.raise_for_status()
        
        return DeleteEmailOutput(success=True, message="✅ Email deleted successfully")
        
    except Exception as e:
        return DeleteEmailOutput(success=False, message=f"❌ Error deleting email: {str(e)}")

def reply_to_email(input: ReplyToEmailInput) -> ReplyToEmailOutput:
    """Reply to an email"""
    try:
        headers = get_gmail_service()
        
        # First, get the original email details
        original_email = get_email_details(input.email_id, headers)
        if not original_email:
            return ReplyToEmailOutput(success=False, message="❌ Original email not found")
        
        # Create reply message
        reply_subject = f"Re: {original_email.subject}" if not original_email.subject.startswith("Re:") else original_email.subject
        reply_body = f"\n\n--- Original Message ---\n{original_email.body}\n\n{input.reply_body}"
        
        # Send the reply
        reply_input = SendEmailInput(
            to=original_email.sender,
            subject=reply_subject,
            body=reply_body
        )
        
        reply_result = send_email(reply_input)
        
        if reply_result.success:
            return ReplyToEmailOutput(
                success=True,
                message=f"✅ Reply sent successfully to {original_email.sender}",
                reply_id=reply_result.email_id
            )
        else:
            return ReplyToEmailOutput(success=False, message=reply_result.message)
        
    except Exception as e:
        return ReplyToEmailOutput(success=False, message=f"❌ Error replying to email: {str(e)}")

def forward_email(input: ForwardEmailInput) -> ForwardEmailOutput:
    """Forward an email"""
    try:
        headers = get_gmail_service()
        
        # Get the original email details
        original_email = get_email_details(input.email_id, headers)
        if not original_email:
            return ForwardEmailOutput(success=False, message="❌ Original email not found")
        
        # Create forward message
        forward_subject = f"Fwd: {original_email.subject}"
        forward_body = f"""
--- Forwarded message ---
From: {original_email.sender}
Date: {original_email.date}
Subject: {original_email.subject}

{original_email.body}

{input.additional_message or ""}
"""
        
        # Send the forward
        forward_input = SendEmailInput(
            to=input.forward_to,
            subject=forward_subject,
            body=forward_body
        )
        
        forward_result = send_email(forward_input)
        
        if forward_result.success:
            return ForwardEmailOutput(
                success=True,
                message=f"✅ Email forwarded successfully to {input.forward_to}",
                forward_id=forward_result.email_id
            )
        else:
            return ForwardEmailOutput(success=False, message=forward_result.message)
        
    except Exception as e:
        return ForwardEmailOutput(success=False, message=f"❌ Error forwarding email: {str(e)}")

def get_labels(input: GetLabelsInput) -> GetLabelsOutput:
    """Get all Gmail labels"""
    try:
        headers = get_gmail_service()
        url = "https://gmail.googleapis.com/gmail/v1/users/me/labels"
        
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        
        labels_data = response.json().get("labels", [])
        labels = [label["name"] for label in labels_data]
        
        return GetLabelsOutput(
            success=True,
            message=f"🏷️ Found {len(labels)} labels",
            labels=labels
        )
        
    except Exception as e:
        return GetLabelsOutput(success=False, message=f"❌ Error fetching labels: {str(e)}")

def mark_as_read(input: MarkAsReadInput) -> MarkAsReadOutput:
    """Mark an email as read"""
    try:
        headers = get_gmail_service()
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{input.email_id}/modify"
        
        payload = {
            "removeLabelIds": ["UNREAD"]
        }
        
        response = httpx.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        return MarkAsReadOutput(success=True, message="✅ Email marked as read")
        
    except Exception as e:
        return MarkAsReadOutput(success=False, message=f"❌ Error marking email as read: {str(e)}")

def mark_as_unread(input: MarkAsUnreadInput) -> MarkAsUnreadOutput:
    """Mark an email as unread"""
    try:
        headers = get_gmail_service()
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{input.email_id}/modify"
        
        payload = {
            "addLabelIds": ["UNREAD"]
        }
        
        response = httpx.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        return MarkAsUnreadOutput(success=True, message="✅ Email marked as unread")
        
    except Exception as e:
        return MarkAsUnreadOutput(success=False, message=f"❌ Error marking email as unread: {str(e)}") 