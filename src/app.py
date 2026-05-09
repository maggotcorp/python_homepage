"""Flask application for MaggotCorp homepage."""

import argparse
import os
from datetime import datetime

from flask import Flask, render_template, abort

app = Flask(__name__)

PROJECTS = [
    'dumb_phone',
    'flutter-gangwars',
    'flutter-lab',
    'zombieTim'
]

# Map project slugs to their display names
PROJECT_NAMES = {
    'dumb_phone': 'Dumb Phone',
    'flutter-gangwars': 'Gangwars',
    'flutter-lab': 'Maggot Lab',
    'zombieTim': 'Zombie Tim'
}

# Map project slugs to their descriptions
PROJECT_DESCRIPTIONS = {
    'dumb_phone': 'A comprehensive network security application for Android and iOS that provides real-time protection against threats, monitoring network traffic, and blocking malicious connections through two distinct firewall modes.',
    'flutter-gangwars': 'A cross-platform Flutter adaptation of the classic Gangwar game, now available on Android, iOS, Linux, Windows, macOS, and Web.',
    'flutter-lab': 'A comprehensive, intelligent security monitoring application built with Flutter, designed for Android and Linux.',
    'zombieTim': 'Zombie Tim is the world\'s first undead AI assistant with a gory, beautiful UI, enhanced intelligence, and word-learning capabilities!'
}

# Map project slugs to their template name prefix
TEMPLATE_PREFIXES = {
    'dumb_phone': 'dumb_phone',
    'flutter-gangwars': 'gangwars',
    'flutter-lab': 'flutter_lab',
    'zombieTim': 'zombie_tim'
}

DOC_TYPES = {
    'readme': 'README',
    'user_guide': 'User Guide',
    'license': 'License',
    'privacy': 'Privacy Policy'
}

DOC_TYPE_NAMES = {
    'readme': 'README',
    'user_guide': 'User Guide',
    'license': 'License',
    'privacy': 'Privacy Policy'
}

# Map doc_type to template suffix
DOC_TYPE_SUFFIXES = {
    'readme': 'readme',
    'user_guide': 'userguide',
    'license': 'license',
    'privacy': 'privacy'
}


@app.route('/')
def home():
    """Render the homepage."""
    return render_template('home.html')


@app.route('/<project>')
def product(project):
    """Render a project product page with full README."""
    if project not in PROJECTS:
        abort(404)

    prefix = TEMPLATE_PREFIXES.get(project)
    # Try to load the README content template
    readme_template = f'{prefix}_readme_content.html'

    return render_template('product.html',
                           project=project,
                           project_name=PROJECT_NAMES.get(project, project),
                           project_description=PROJECT_DESCRIPTIONS.get(project, ''),
                           readme_template=readme_template,
                           doc_types=DOC_TYPES.keys(),
                           doc_type_names=DOC_TYPE_NAMES)


@app.context_processor
def inject_globals():
    """Inject global variables into templates."""
    return {
        "projects": PROJECTS,
        "project_names": PROJECT_NAMES,
        "project_descriptions": PROJECT_DESCRIPTIONS,
        "current_year": datetime.now().year
    }


@app.route('/<project>/<doc_type>')
def document(project, doc_type):
    """Render a document page for a specific project and document type."""
    if project not in PROJECTS or doc_type not in DOC_TYPES:
        abort(404)

    prefix = TEMPLATE_PREFIXES.get(project)
    suffix = DOC_TYPE_SUFFIXES.get(doc_type)
    template_name = f'{prefix}_{suffix}.html'

    try:
        return render_template(template_name,
                               project=project,
                               project_name=PROJECT_NAMES.get(project, project),
                               doc_type=doc_type,
                               doc_type_name=DOC_TYPE_NAMES.get(doc_type, doc_type))
    except Exception:
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