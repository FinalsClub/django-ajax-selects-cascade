try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-ajax-selects-cascade',
    version='0.1.0',
    description='Supports the dependence of one AutoCompleteSelectField upon the choice of another AutoCompleteSelectField.',
    author='Bryan Bonvallet',
    author_email='btbonval@gmail.com',
    url='https://github.com/btbonval/django-ajax-selects-cascade',
    packages=['ajax_select_cascade'],
    package_data={'ajax_select_cascade':
        [
            '*.py',
            '*.txt',
            'static/ajax_select_cascade/js/*.js',
        ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Framework :: Django",
        ],
    long_description="""\
Supports the dependence of one AutoCompleteSelectField upon the choice of
another AutoCompleteSelectField.

Requires django-ajax-selects in the Django environment.
"""
)
