from src.cdc.domain.evaluations_rules import EvaluateRules


def test_get_key():
    er = EvaluateRules()

    months = er.get_key(er.constant_are_three_addresses, "months")

    assert months == 6

    months = er.get_key(er.constant_are_three_addresses, "day")

    assert months == "key doesn't exist"


def test_ret_rules():
    evaluate_rules = EvaluateRules()
    expected_rules = [
        evaluate_rules.constant_past_due_account,
        evaluate_rules.constant_broken_account,
        evaluate_rules.constant_two_broken_accounts,
        evaluate_rules.constant_are_three_addresses,
        evaluate_rules.constant_is_revolving_account,
        evaluate_rules.constant_is_fraudulent,
    ]
    assert evaluate_rules.ret_rules() == expected_rules
