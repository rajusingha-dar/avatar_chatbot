"""
Fallback HTML template for when static files are not available
"""

# The fallback HTML to use when static/index.html is not available
FALLBACK_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Avatar Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        .error {
            color: #721c24;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Voice Avatar Chatbot</h1>
    <div class="error">
        <p>The main application interface could not be loaded.</p>
        <p>Please make sure the static files are properly set up.</p>
    </div>
    <p>This is a fallback page.</p>
</body>
</html>
"""

def get_fallback_html():
    """
    Return the fallback HTML content
    """
    return FALLBACK_HTML