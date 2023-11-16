from flask import Flask

app = Flask(__name__)

@app.post("/create-ticket")
def create_ticket():
    raise NotImplementedError()


@app.put("/approve-ticket")
def approve_ticket():
    raise NotImplementedError()


@app.put("/deny-ticket")
def deny_ticket():
    raise NotImplementedError()


@app.put("/request-review-for-ticket")
def request_review_for_ticket():
    raise NotImplementedError()


@app.put("/resolve-review-request")
def resolve_review_request():
    raise NotImplementedError()


if __name__ == '__main__':
    app.run()
