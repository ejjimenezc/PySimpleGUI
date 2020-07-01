from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

includefiles = []
packages = ['cryptography','PySimpleGUI','subprocess','base64','sys','os']

buildOptions = dict(packages = packages, excludes = [], include_files = includefiles)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('crypto.py', base=base, targetName = 'Encriptador')
]

setup(
    name='Encriptador',
    version = '1.0.0',
    description = 'Encriptador de licencia de Nvivo 12',
    author = 'Edwin Jimenez',
    options = dict(build_exe = buildOptions),
    executables = executables)
