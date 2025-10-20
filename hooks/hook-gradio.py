# pylint: disable=invalid-name
"""
This module is a hook for PyInstaller to correctly bundle the gradio package.
"""

module_collection_mode = {
    'gradio': 'py',
}
