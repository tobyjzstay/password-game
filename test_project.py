from datetime import date, timedelta
import project
import requests


def test_invalid_rule_1():
    assert project.rule_1("root") == False


def test_valid_rule_1():
    assert project.rule_1("admin") == True


def test_invalid_rule_2():
    assert project.rule_2("forty-two") == False


def test_valid_rule_2():
    assert project.rule_2("42") == True


def test_invalid_rule_3():
    assert project.rule_3("python") == False


def test_valid_rule_3():
    assert project.rule_3("Python") == True


def test_invalid_rule_4():
    assert project.rule_4("admin") == False


def test_valid_rule_4():
    assert project.rule_4("@dm!n") == True


def test_invalid_rule_5():
    assert project.rule_5("35") == False


def test_valid_rule_5():
    assert project.rule_5("82645") == True


def test_invalid_rule_6():
    assert project.rule_6("martius") == False


def test_valid_rule_6():
    assert project.rule_6("january") == True


def test_invalid_rule_7():
    assert project.rule_7("ivxlcdm") == False


def test_valid_rule_7():
    assert project.rule_7("aDMIn") == True


def test_invalid_rule_8():
    assert project.rule_8("exoskeleton") == False


def test_valid_rule_8():
    assert project.rule_8("seashell") == True


def test_invalid_rule_9():
    assert project.rule_9("viiv") == False


def test_valid_rule_9():
    assert project.rule_9("VIIV") == True


def test_invalid_rule_10():
    # get yesterday's wordle
    r = requests.get(
        "https://www.nytimes.com/svc/wordle/v2/{0}.json".format(
            date.today() - timedelta(days=1)
        )
    )
    wordle = r.json().get("solution")
    assert project.rule_10(wordle) == False


def test_valid_rule_10():
    assert project.rule_10(project.get_wordle()) == True
