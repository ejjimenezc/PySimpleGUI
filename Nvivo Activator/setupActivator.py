from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

includefiles = ['icon.ico', 'AcceptedCountryFormat.txt']
packages = ['cryptography','tempfile','PySimpleGUI','subprocess','base64','sys','os','threading']

buildOptions = dict(packages = packages, excludes = [], include_files = includefiles)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Activator.py', base=base, targetName = 'Activador de Nvivo', icon = "icon.ico")
]

setup(
    name='Activator',
    version = '0.8.0',
    description = 'Activador de Nvivo 12 para INACAP',
    author = 'Software Shop',
    options = dict(build_exe = buildOptions),
    executables = executables)
