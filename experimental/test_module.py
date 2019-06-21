# contents of test_module.py with source code and the test
from pathlib import Path


class Exam:
    def __init__(self):
        self.exam = 'Math'

    def examize(self, extra):
        return self.exam + extra


class E(Exam):
    def examize(self, extra):
        self.exam = 'TestMath'
        return super().examize(extra)


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")


def test_exam(monkeypatch):
    def mockreturn(self, extra):
        return 'Test' + 'extra'

    exam = E()
    monkeypatch.setattr(Exam, "examize", mockreturn)
    assert exam.examize('extra') == 'Testextra'
    assert exam.exam == 'TestMath'
