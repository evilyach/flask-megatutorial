import os

import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands. """

    @translate.command()
    def update() -> None:
        """Update all languages.

        Raises:
            RuntimeError: if commands fail
        """

        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel update -i messages.pot -d app/translations"):
            raise RuntimeError("update command failed")

        os.remove("messages.pot")

    @translate.command()
    def compile() -> None:
        """Compile all languages.

        Compiled file is stored in `translations/<lang>/LC_MESSAGES/messages.mo`

        Raises:
            RuntimeError: if commands fail
        """
        if os.system("pybabel compile -d app/translations"):
            raise RuntimeError("compile command failed")

    @translate.command()
    @click.argument("lang")
    def init(lang: str) -> None:
        """Initialize a new language.

        Args:
            lang (str): ISO 649-1 language code

        Raises:
            RuntimeError: if command fails
        """

        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
            raise RuntimeError("init command failed")

        os.remove("messages.pot")
