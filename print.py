from jinja2 import Template


def print_3x1_label(sku, description, qr_code_url):
    # Load the HTML template from a file
    with open("template.html", "r") as f:
        template_str = f.read()

    # Create a Jinja2 template object
    template = Template(template_str)

    # Render the template with the dynamic content
    html = template.render(sku=sku, description=description, qr_code_url=qr_code_url)

    # Print the rendered HTML for testing
    print(html)
    