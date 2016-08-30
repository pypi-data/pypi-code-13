import platform

target = platform.system().lower()

try:
	from Development import cccompiler
except ImportError:
	pass

try:
	from setuptools import setup, Extension

except ImportError:
	from distutils.core import setup
	from distutils.extension import Extension

Version = '2.4.1'

ShortDescription = 'modern OpenGL binding for Python'

LongDescription = '''
|Chat|

|PyPI-1| |PyPI-2| |PyPI-3| |github|

|PyPI-4| |PyPI-5|

OpenGL is a great environment for developing portable, platform independent,
interactive 2D and 3D graphics applications. The API implementation in Python
is cumbersome, resulting in applications with high latency. To solve this
problem we have developed ModernGL, a wrapper over OpenGL that simplifies the
creation of simple graphics applications like scientific simulations, small
games or user interfaces. Usually, acquiring in-depth knowledge of OpenGL
requires a steep learning curve. In contrast, ModernGL is easy to learn and
use, moreover it is capable of rendering with the same performance and
quality, with less code written.

.. |Chat| image:: https://badges.gitter.im/cprogrammer1994/ModernGL.svg
.. |PyPI-1| image:: https://img.shields.io/pypi/l/ModernGL.svg
.. |PyPI-2| image:: https://img.shields.io/pypi/pyversions/ModernGL.svg
.. |PyPI-3| image:: https://img.shields.io/pypi/v/ModernGL.svg
.. |github| image:: https://img.shields.io/github/tag/cprogrammer1994/ModernGL.svg
.. |PyPI-4| image:: https://img.shields.io/pypi/status/ModernGL.svg
.. |PyPI-5| image:: https://img.shields.io/pypi/dm/ModernGL.svg
'''

Classifiers = [
	'Development Status :: 5 - Production/Stable',
#	'Development Status :: 6 - Mature',
	'Environment :: Win32 (MS Windows)',
	'Environment :: X11 Applications',
	'Environment :: X11 Applications :: Gnome',
	'Environment :: X11 Applications :: GTK',
	'Environment :: X11 Applications :: KDE',
	'Environment :: X11 Applications :: Qt',
	'Intended Audience :: Developers',
	'Intended Audience :: Education',
	'License :: Freely Distributable',
	'License :: Free For Educational Use',
	'License :: Free For Home Use',
	'License :: Freeware',
	'License :: OSI Approved',
	'License :: OSI Approved :: MIT License',
	'Natural Language :: English',
	'Operating System :: Microsoft',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: Microsoft :: Windows :: Windows 7',
	'Operating System :: Microsoft :: Windows :: Windows 95/98/2000',
	'Operating System :: Microsoft :: Windows :: Windows CE',
	'Operating System :: Microsoft :: Windows :: Windows NT/2000',
	'Operating System :: Microsoft :: Windows :: Windows Server 2003',
	'Operating System :: Microsoft :: Windows :: Windows Server 2008',
	'Operating System :: Microsoft :: Windows :: Windows Vista',
	'Operating System :: Microsoft :: Windows :: Windows XP',
	'Operating System :: OS Independent',
	'Operating System :: POSIX',
	'Operating System :: POSIX :: Linux',
	'Operating System :: Unix',
	'Programming Language :: C',
	'Programming Language :: C++',
	'Programming Language :: Cython',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3 :: Only',
	'Topic :: Documentation',
	'Topic :: Desktop Environment',
	'Topic :: Education',
	'Topic :: Games/Entertainment',
	'Topic :: Multimedia',
	'Topic :: Multimedia :: Graphics',
	'Topic :: Multimedia :: Graphics :: 3D Modeling',
	'Topic :: Multimedia :: Graphics :: 3D Rendering',
	'Topic :: Multimedia :: Video',
	'Topic :: Scientific/Engineering :: Visualization',
	'Topic :: Software Development',
	'Topic :: Software Development :: Documentation',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: System :: Monitoring',
	'Topic :: Utilities',
]

Keywords = [
	'ModernGL',
	'modern OpenGL',
	'OpenGL',
	'visualization',
	'ray-tracing',
	'compute shader',
	'shader',
	'documentation',
	'documented',
	'graphics',
	'vulkan',
	'GLSL',
	'GPU',
	'GPGPU',
	'nvidia',
	'cuda',
	'amd',
	'GL',
	'GLU',
	'GLEXT',
	'WGL',
	'WGLEXT',
	'ARB',
	'GLX',
	'2D',
	'3D',
	'CAD',
	'glm',
	'design',
	'video',
]

Libraries = {
	'windows' : ['user32', 'gdi32'],
	'linux' : ['GL', 'dl'],
}

Sources = [
	'Source/Methods.cpp',
	'Source/Methods/Buffer.cpp',
	'Source/Methods/Compute.cpp',
	'Source/Methods/Core.cpp',
	'Source/Methods/Debug.cpp',
	'Source/Methods/Experimental.cpp',
	'Source/Methods/Framebuffer.cpp',
	'Source/Methods/Initialize.cpp',
	'Source/Methods/Program.cpp',
	'Source/Methods/Render.cpp',
	'Source/Methods/Shader.cpp',
	'Source/Methods/Texture.cpp',
	'Source/Methods/Transform.cpp',
	'Source/Methods/VertexArray.cpp',

	'Source/Types/ComputeShaderType.cpp',
	'Source/Types/EnableFlagType.cpp',
	'Source/Types/FramebufferType.cpp',
	'Source/Types/IndexBufferType.cpp',
	'Source/Types/ProgramType.cpp',
	'Source/Types/ShaderType.cpp',
	'Source/Types/StorageBufferType.cpp',
	'Source/Types/TextureType.cpp',
	'Source/Types/UniformBufferLocationType.cpp',
	'Source/Types/UniformBufferType.cpp',
	'Source/Types/UniformLocationType.cpp',
	'Source/Types/VertexArrayType.cpp',
	'Source/Types/VertexBufferType.cpp',

	'Source/Utils/BufferFormat.cpp',
	'Source/Utils/OpenGL.cpp',
	'Source/Utils/PythonMethod.cpp',

	'Source/Constants.cpp',
	'Source/Errors.cpp',
	'Source/Types.cpp',

	'Source/ModernGL.cpp',
]

ModernGL = Extension(
	'ModernGL.ModernGL',
	include_dirs = ['Source'],
	define_macros = [('MODERN_GL_VERSION', Version)],
	libraries = Libraries[target],
	sources = Sources,
)

args = {
	'name' : 'ModernGL',
	'version' : Version,
	'description' : ShortDescription,
	'long_description' : LongDescription,
	'url' : 'https://github.com/cprogrammer1994/ModernGL',
	'download_url' : 'https://github.com/cprogrammer1994/ModernGL/releases',
	'author' : 'Szabolcs Dombi',
	'author_email' : 'cprogrammer1994@gmail.com',
	'license' : 'MIT',
	'classifiers' : Classifiers,
	'keywords' : Keywords,
	'packages' : ['ModernGL'],
	'ext_modules' : [ModernGL],
	'platforms' : ['any'],
}

if target == 'windows':
	args['zip_safe'] = True

setup(**args)
