# Deployment Guide for MaggotCorp Homepage to PythonAnywhere

## Prerequisites
- A PythonAnywhere account (free tier should suffice for basic use).
- Git repository of the project (already set up as per workspace config).
- Ensure all dependencies are in `requirements.txt`.

## Steps

1. **Sign in to PythonAnywhere**:
   - Log in to your PythonAnywhere dashboard.

2. **Create a New Web App**:
   - Go to the "Web" tab.
   - Click "Add a new web app".
   - Select "Flask" as the framework.
   - Choose Python 3.10 or compatible version.
   - Set the project path, e.g., `/home/yourusername/maggotcorp-homepage/src/app.py`.

3. **Upload Code**:
   - Use the "Files" tab to upload your project files, or clone from Git:
     - In a Bash console: `git clone http://mofo-jackson:6009/maggotcorp/homepage.git`.
   - Ensure the working directory matches your setup.

4. **Configure WSGI**:
   - In the "Web" tab, edit the WSGI configuration file.
   - Point it to your app: `from app import app as application`.

5. **Static Files**:
   - In "Static files" section:
     - URL: `/static/`, Directory: `/home/yourusername/maggotcorp-homepage/src/static`.

6. **Install Dependencies**:
   - In a Bash console: `pip install --user -r requirements.txt`.

7. **Secret Key**:
   - Update `app.secret_key` in `src/app.py` to a secure value (generate one securely).

8. **Reload the App**:
   - Click "Reload" in the Web tab.

9. **Access**:
   - Visit `yourusername.pythonanywhere.com`.
   - Editor at `/admin/about` (add authentication in production).

## Notes
- File writes (e.g., to `about.json`) use persistent storage.
- For image uploads in Quill, may need paid plan or external storage.
- Monitor console for errors.