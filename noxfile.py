#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import nox


@nox.session
def test(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_test.txt")
    session.install("-e", ".", "--no-deps")
    session.run("pytest", "--cov=pycasino", "tests/")
    # session.run("coveralls")


@nox.session
def blacken(session):
    session.install("black")
    session.run("black", "--version")
    session.run("black", "--check", "pycasino", "tests", "noxfile.py", "setup.py")


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "--version")
    session.run("flake8", "setup.py", "docs", "pycasino", "tests")


@nox.session
def docs(session):
    session.install("-r", r"docs\requirements.txt")

    session.chdir("docs")
    if os.path.exists("_build"):
        shutil.rmtree("_build")
    session.run("sphinx-build", "-W", "source/", "_build/html")
