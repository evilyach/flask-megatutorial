from app import (
    app,
    db,
    login
)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "login": login,
    }
