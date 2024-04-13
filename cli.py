import click

from database import Base, Session
from text_analyzer.ml_model import MLModel
from text_analyzer.ml_service import MLService
from text_analyzer.user import User

session = Session()


@click.group()
def cli():
    pass


@cli.command()
@click.option("-n", "--name")
@click.option("-e", "--email")
@click.option("-p", "--password")
def add_user(name, email, password):
    session = Session()
    new_user = User(username=name, email=email, password=password)
    new_user.set_api_key(session)
    session.add(new_user)
    session.commit()
    click.echo(f"User: {name} added.")


@cli.command()
@click.option("-n", "--name")
def delete_user(name):
    session = Session()
    session.query(User).filter_by(username=name).delete()
    session.commit()
    click.echo(f"User: {name} deleted.")


@cli.command()
@click.option("-id")
@click.option("-a", "--amount")
def update_balance(id, amount):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    user.update_balance(int(amount), session)
    click.echo(
        f"{user.username} updated balance by {amount}, current balance = {user.balance}"
    )


@cli.command()
@click.option("-id")
@click.option("-t", "--text")
def execute_task(id, text):
    session = Session()
    model = MLModel()
    service = MLService(model)
    user = session.query(User).filter_by(id=id).first()
    task = service.execute_task(user, text, session)
    click.echo(task)


@cli.command()
@click.option("-t", "--text")
def classify_test(text):
    model = MLModel()
    task = model.classify_text(text)
    click.echo(task)


if __name__ == "__main__":
    cli()
