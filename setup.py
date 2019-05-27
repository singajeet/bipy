""" Setup.py file for bipy package
"""
from setuptools import setup

setup(
    name="bipy",
    version="0.1.0",
    author="Ajeet Singh",
    author_email="singajeet@gmail.com",
    packages=["bipy", "bipy.core", "bipy.core.db", "bipy.core.db.analytic",
              "bipy.core.db.connection_managers", "bipy.core.db.repository",
              "bipy.core.db.warehouse", "bipy.core.db.warehouse.browsers",
              "bipy.core.db.warehouse.base_meta_gen", "bipy.core.decorators",
              "bipy.core.security"
             ],
    url="https://github.com/singajeet/bipy",
    license="LICENSE.txt",
    description="Python based BusinessIntelligence application",
    long_description=open('README.txt').read(),
    install_requires=["yapsy", "sqlalchemy"]
)
