# Test cases for xss.yml. Run with `mise run py:semgrep`.
import json

import jinja2
from fastapi import Response
from fastapi.responses import HTMLResponse
from jinja2 import Environment, Template
from markupsafe import Markup

from universalrecipes.routes.spa import script_safe_json


def templates(source: str):
    # ruleid: universalrecipes-jinja-autoescape
    Template(source)

    # ruleid: universalrecipes-jinja-autoescape
    jinja2.Environment(loader=None)

    # ruleid: universalrecipes-jinja-autoescape
    Template(source, autoescape=False)

    # ok: universalrecipes-jinja-autoescape
    Template(source, autoescape=True)

    # ok: universalrecipes-jinja-autoescape
    Environment(loader=None, autoescape=True)


def script_tags(schema: dict, name: str):
    # ruleid: universalrecipes-script-tag-json
    a = f"""<script type="application/ld+json">{json.dumps(schema)}</script>"""

    # ruleid: universalrecipes-script-tag-json
    b = f"<script>var name = {name};</script>"

    # ok: universalrecipes-script-tag-json
    c = f"""<script type="application/ld+json">{script_safe_json(schema)}</script>"""

    return a, b, c


def responses(name: str):
    # ruleid: universalrecipes-html-response-fstring
    HTMLResponse(f"<h1>{name}</h1>")

    # ruleid: universalrecipes-html-response-fstring
    Response(f"<h1>{name}</h1>", media_type="text/html")

    # ruleid: universalrecipes-html-response-fstring
    Markup(f"<b>{name}</b>")

    # ok: universalrecipes-html-response-fstring
    Response(f'{{"name": "{name}"}}', media_type="application/json")
