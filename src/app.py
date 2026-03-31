"""Flask application for MaggotCorp homepage."""

import argparse
import os
from datetime import datetime

import markdown
from flask import Flask, render_template, abort

app = Flask(__name__)
app.secret_key = 'a_secret_key_for_development'  # Change this in production

PROJECTS = [
    'dumb_phone',
    'flutter-gangwars',
    'flutter-lab',
    'flutter-zombieTim'
]

DOC_TYPES = {
    'readme': 'README.md',
    'user_guide': 'USER_GUIDE.md',
    'license': 'LICENSE.md',
    'privacy': 'PRIVACY_POLICY.md'
}

def get_project_path(project):
    """Get the file system path for a project directory."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), project)

def read_md_file(path):
    """Read and convert a markdown file to HTML."""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return markdown.markdown(content)
    return None

# class EditorForm(FlaskForm):
#     content = TextAreaField('Content')
#     submit = SubmitField('Save')
#
# @app.route('/admin/about', methods=['GET', 'POST'])
# def admin_about():
#     form = EditorForm()
#     data_path = os.path.join(os.path.dirname(__file__), 'data', 'about.json')
#
#     if form.validate_on_submit():
#         with open(data_path, 'w') as f:
#             json.dump({'content': form.content.data}, f)
#         return redirect(url_for('home'))
#
#     try:
#         with open(data_path, 'r') as f:
#             data = json.load(f)
#             form.content.data = data.get('content', '')
#     except FileNotFoundError:
#         form.content.data = ''
#
#     return render_template('admin_about.html', form=form)

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('home.html')

@app.route('/<project>')
def product(project):
    """Render a project product page with full README."""
    if project not in PROJECTS:
        abort(404)

    project_path = get_project_path(project)

    # Load full README
    readme_path = os.path.join(project_path, 'README.md')
    readme_content = read_md_file(readme_path)
    if readme_content is None:
        readme_content = '<p>README not available.</p>'

    return render_template('product.html',
                           project=project,
                           readme_content=readme_content,
                           doc_types=DOC_TYPES.keys())

@app.context_processor
def inject_globals():
    """Inject global variables into templates."""
    return {"projects": PROJECTS, "current_year": datetime.now().year}

# Mapping from project/doc_type to template names (without .html extension)
TEMPLATE_MAP = {
    ('dumb_phone', 'readme'): 'dumb_phone_readme',
    ('dumb_phone', 'user_guide'): 'dumb_phone_userguide',
    ('dumb_phone', 'privacy'): 'dumb_phone_privacy',
    ('flutter-gangwars', 'readme'): 'gangwars_readme',
    ('flutter-gangwars', 'user_guide'): 'gangwars_userguide',
    ('flutter-gangwars', 'privacy'): 'gangwars_privacy',
    ('flutter-lab', 'readme'): 'flutter_lab_readme',
    ('flutter-lab', 'user_guide'): 'flutter_lab_userguide',
    ('flutter-lab', 'privacy'): 'flutter_lab_privacy',
    ('flutter-zombieTim', 'readme'): 'zombie_tim_readme',
    ('flutter-zombieTim', 'user_guide'): 'zombie_tim_userguide',
    ('flutter-zombieTim', 'privacy'): 'zombie_tim_privacy',
}


@app.route('/<project>/<doc_type>')
def document(project, doc_type):
    """Render a document page for a specific project and document type."""
    if project not in PROJECTS or doc_type not in DOC_TYPES:
        abort(404)

    # First, try to read from the project directory
    file_name = DOC_TYPES[doc_type]
    path = os.path.join(get_project_path(project), file_name)
    content = read_md_file(path)

    if content is not None:
        # Use the generic document template with markdown content
        return render_template('document.html', project=project, doc_type=doc_type, content=content)

    # If markdown file doesn't exist, try to use the specific template
    template_name = TEMPLATE_MAP.get((project, doc_type))
    if template_name:
        return render_template(f'{template_name}.html')

    # No content available
    abort(404)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='MaggotCorp Homepage Flask Application'
    )
    parser.add_argument(
        '--port', type=int, default=5000,
        help='Port to run the application on (default: 5000)'
    )
    parser.add_argument(
        '--host', type=str, default='127.0.0.1',
        help='Host to run the application on (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--debug', action='store_true', default=True,
        help='Run in debug mode (default: True)'
    )
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
