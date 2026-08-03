from .translations import TRANSLATIONS


def get_text(language, key):
    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["de"]
    ).get(
        key,
        key
    )