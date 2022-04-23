from flask_babel import _
import requests

from app import app


def translate(text: str, source_language: str, target_language: str) -> str:
    """Translate text using Yandex Translate service.

    Args:
        text (str): text to translate
        source_language (str): ISO 649-1 source language code
        target_language (str): ISO 649-1 target language code

    Returns:
        str: translated text
    """

    token = app.config["YANDEX_TRANSLATE_TOKEN"]
    if token is None:
        return _("Yandex Translate Token is not set up")

    folder_id = app.config["YANDEX_TRANSLATE_FOLDER_ID"]
    if folder_id is None:
        return _("Yandex Translate Folder ID is not set up")

    body = {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "texts": [text],
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        "https://translate.api.cloud.yandex.net/translate/v2/translate",
        json=body,
        headers=headers,
    )

    if response.status_code != 200:
        return _("Could not translate text")

    print(response.text)
