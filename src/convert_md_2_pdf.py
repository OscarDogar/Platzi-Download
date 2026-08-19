"""Utilities to convert Markdown content into styled A4 PDF files."""

from markdown import markdown
from xhtml2pdf import pisa

BACKGROUND_COLOR = "#fdfdfd"
COLOR = "#1F1F1F"


def convert_html_to_pdf(md_content, filepath):
    """Convert Markdown content to a styled A4 PDF and save it to a file.

    Args:
        md_content: Markdown source to convert.
        filepath: Destination path for the generated PDF.
    """
    html_content = markdown(md_content)

    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            @page {{
                size: A4;
                margin: 1cm;
                background-color: {BACKGROUND_COLOR};
            }}

            html, body {{
                margin: 0;
                padding: 0;
                background-color: {BACKGROUND_COLOR};
            }}

            body {{
                font-family: Helvetica, sans-serif;
                font-size: 16px;
                line-height: 1.3;
                color: {COLOR};
                background-color: {BACKGROUND_COLOR};
            }}

            .card {{
                background-color: {BACKGROUND_COLOR};
                padding: 20px;
            }}

            /* Paragraphs - more separated */
            p {{
                margin-top: 0;
                margin-bottom: 12px;
                padding: 0;
            }}

            /* Headings */
            h1 {{
                margin-top: 18px;
                margin-bottom: 10px;
            }}

            h2 {{
                margin-top: 16px;
                margin-bottom: 9px;
            }}

            h3 {{
                margin-top: 14px;
                margin-bottom: 8px;
            }}

            h4, h5, h6 {{
                margin-top: 10px;
                margin-bottom: 7px;
            }}

            /* Lists - more compact */
            ul, ol {{
                margin-top: 3px;
                margin-bottom: 8px;
                padding-left: 25px;
            }}

            li {{
                margin-top: 0;
                margin-bottom: 2px;
                padding: 0;
            }}

            /* Avoid large gap between paragraph and list */
            p + ul,
            p + ol {{
                margin-top: 0;
            }}

            /* Avoid large gap after lists */
            ul + p,
            ol + p {{
                margin-top: 8px;
            }}

            /* Images */
            img {{
                display: block;
                margin: 10px auto;
                max-width: 100%;
            }}

            /* Links */
            a {{
                color: {COLOR};
            }}

            /* Blockquotes */
            blockquote {{
                margin-top: 8px;
                margin-bottom: 10px;
                padding-left: 10px;
            }}

            /* Code blocks */
            pre {{
                margin-top: 8px;
                margin-bottom: 10px;
            }}

            code {{
                font-family: monospace;
            }}

            /* Tables */
            table {{
                margin-top: 8px;
                margin-bottom: 10px;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            {html_content}
        </div>
    </body>
    </html>
    """

    with open(filepath, "wb") as output:
        result = pisa.CreatePDF(styled_html, dest=output)

    if result.err:
        raise RuntimeError("Failed to generate PDF")
