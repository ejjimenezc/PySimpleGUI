from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

includefiles = ['icon.ico', 'AcceptedCountryFormat.txt']
packages = ['cryptography','tempfile','PySimpleGUI','subprocess','base64','sys','os']

buildOptions = dict(packages = packages, excludes = [], include_files = includefiles)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Activator.py', base=base, targetName = 'Activador de Nvivo', icon = "icon.ico")
]

setup(
    name='Activator',
    version = '7.0.0',
    description = 'Activador de Nvivo 12',
    author = 'Edwin Jimenez',
    options = dict(build_exe = buildOptions),
    executables = executables)
