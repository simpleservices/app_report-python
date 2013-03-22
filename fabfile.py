from fabric.api import local


def test():
    local('python -m unittest discover -v')


def check_pep8():
    local('clear; pep8 --first --show-source .')
