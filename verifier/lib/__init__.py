from pathlib import Path
from sys import platform
from cffi import FFI
from platform import architecture, machine


_ffi_def = """
extern char* ffiverify(char* proofQREncoded, char* configpath);
extern void freeCString(char* s);
"""

def _libpath():
    return Path(__file__).parent.absolute()


def listlibs():
    return [x.name for x in list(_libpath().glob('*.so')) + list(_libpath().glob('*.dll'))]


def loadlib(lib='auto'):
    if lib == 'auto':
        lib = _autodetect()

    lib = _libpath() / lib

    if not lib.is_file():
        raise ValueError(f'Could not find verifier lib {lib.name} choose one of: {", ".join(listlibs())}')

    ffi = FFI()
    ffi.cdef(_ffi_def)
    verifier = ffi.dlopen(str(lib.absolute()))

    return verifier, ffi


def _autodetect():
    libos = None
    libext = '.so'

    if platform.startswith("linux"):
        libos = 'linux'
    elif platform.startswith("darwin"):
        libos = 'darwin'
    elif platform.startswith("win32"):
        libos = "windows"
        libext = '.dll'

    if libos is None:
        raise ValueError(f'Auto detect failed OS unknown: {platform}')


    libarch = None

    arch = architecture()
    mach = machine()

    if 'arm' in mach:
        if 'v7' in mach:
            libarch = 'armv7'
        elif 'v6' in mach:
            libarch = 'armv6'
        elif 'v5' in mach:
            libarch = 'armv5'
        elif '64' in mach:
            libarch = 'arm64'

    if 'aarch64' in mach:
        libarch = 'arm64'

    if 'x86' in mach:
        if '64' in mach:
            libarch = 'amd64'
        else:
            libarch = '386'

    if 'amd64' in mach:
        libarch = 'amd64'

    b32arches = ['i686', 'i386', 'i486']

    if mach.lower() in b32arches:
        if '64' in mach:
            libarch = 'amd64'
        else:
            libarch = '386'

    if libarch is None:
        raise ValueError(f'Auto detect failed CPU Architecture unknown: {arch} {mach}')


    return f"verifier-{libos}-{libarch}{libext}"
