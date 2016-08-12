from setuptools import setup

def readme():
    with open('README') as f:
        return f.read()

setup(name='music_sampler',
        setup_requires=['setuptools_scm'],
        use_scm_version=True,
        description='A music player which associates each key on the keyboard '
            'to a set of actions to run',
        long_description=readme(),
        classifiers= [
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.5',
            'Topic :: Multimedia :: Sound/Audio :: Players'
        ],
        keywords='music sampler keyboard',
        url='https://git.immae.eu/?p=perso/Immae/Projets/Python/MusicSampler.git',
        author='Ismaël Bouya',
        author_email='ismael.bouya@normalesup.org',
        license='MIT',
        packages=['music_sampler', 'music_sampler.actions'],
        install_requires=[
            'Cython>=0.24',
            'Kivy>=1.9.1',
            'pydub>=0.16.4',
            'Pygame>=1.9.2.dev1',
            'sounddevice>=0.3.3',
            'TRANSITIONS>=0.4.1',
            'PyYAML>=3.11'
        ],
        entry_points={
            'console_scripts': ['music_sampler=music_sampler.app:main'],
        },
        include_package_data=True,
        zip_safe=False)

