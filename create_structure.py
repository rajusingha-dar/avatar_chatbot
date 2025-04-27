import os

# Define the folder and file structure
structure = {
    "logs/": [],
    "static/": [
        "index.html",
        "css/main.css",
        "js/app.js",
        "js/audioProcessor.js",
        "js/avatarController.js",
        "js/apiClient.js",
    ],
    "modules/": [
        "__init__.py",
        "config.py",
        "logger.py",
        "models.py",
        "routes/__init__.py",
        "routes/main.py",
        "routes/speech.py",
        "routes/chat.py",
        "routes/tts.py",
        "templates/fallback_html.py",
    ],
}

# Files at the root level
root_files = ["app.py", ".env", "requirements.txt"]

def create_structure(base_path="."):
    # Create root level files
    for file in root_files:
        file_path = os.path.join(base_path, file)
        if not os.path.exists(file_path):
            open(file_path, 'w').close()
            print(f"Created file: {file_path}")

    # Create folders and files
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")
        for file in files:
            file_path = os.path.join(base_path, folder, file)
            # Ensure parent directories for nested files
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'w').close()
            print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_structure()
