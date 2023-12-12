import datetime

from flask import Flask, request

from data.services import BaseAttachmentsManager, BaseTicketManager
from data.services.FsAttachmentsManager import FsAttachmentsManager
from data.services.mysql.MySqlTicketManager import MySqlTicketManager
from helpers.TicketBuilder import TicketBuilder

app = Flask(__name__)

attachments_manager: BaseAttachmentsManager = FsAttachmentsManager()
ticket_manager: BaseTicketManager = MySqlTicketManager()


@app.post("/create-ticket")
def create_ticket():
    ticket_builder = TicketBuilder()
    
    ticket_builder.with_author(int(request.form.get("authorId")))\
        .with_text(request.form.get("text"))\
        .with_timestamp(datetime.UTC)

    for filename in request.files:
        form_file = request.files.get(filename)
        ticket_builder.with_attachment(form_file.filename, form_file.mimetype)
        
    result_ticket = ticket_manager.create_ticket(ticket_builder)

    for attachment in result_ticket.attachments:
        associated_form_file = request.files[attachment.filename]
        attachments_manager.create(attachment.id, associated_form_file.read())
        
    return 200

@app.put("/approve-ticket")
def approve_ticket():
    try:
        ticket_id = int(request.args.get("id", int))
        
        ticket_manager.approve_ticket(ticket_id)
        return 200
    except ValueError:
        return 400


@app.put("/deny-ticket")
def deny_ticket():
    try:
        ticket_id = int(request.args.get("id", int))

        ticket_manager.deny_ticket(ticket_id)
        return 200
    except ValueError:
        return 400


@app.put("/request-review-for-ticket")
def request_review_for_ticket():
    try:
        ticket_id = int(request.args.get("id"))
        text = str(request.json["text"])

        ticket_manager.request_changes_for_ticket(ticket_id, text)
        return 200
    except ValueError:
        return 400


@app.put("/resolve-review-request")
def resolve_review_request():
    pass


if __name__ == '__main__':
    app.run()
