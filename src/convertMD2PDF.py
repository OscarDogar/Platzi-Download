from weasyprint import HTML
from markdown import markdown

backgroundColor = "#13161c"
color = "whitesmoke"

def convert_html_to_pdf(md_content, filepath):
    html_content = markdown(md_content)
    # Add basic styling
    styled_html = f"""
    <html>
    <head>
    <style>
    @page {{
        size: A4;
        margin: 1cm;
        background-color: {backgroundColor};
    }}

    body {{
        font-family: Roobert, sans-serif;
        font-size: 16px;
        color: {color};
    }}

    .card {{
        background: {backgroundColor};
        border-radius: 12px;
        padding: 20px;
    }}
    img {{ 
        display: block; 
        margin: 10px auto; 
        max-width: 100%; 
        max-height: 90vh; 
        object-fit: contain; 
        page-break-inside: avoid; 
    }}
    a {{
        color: {color};
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

    # Convert HTML → PDF
    HTML(string=styled_html).write_pdf(filepath)