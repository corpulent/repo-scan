from reposcan import core


def test_calc_score():
    calc_data = {
        'req': {
            'extras': ['mock', 'ml-metadata', 'sklearn', 'tensorflow', 'tf-slim', 'six', 'absl-py', 'keras-tuner']
        }
    }
    assert core.calc_score(calc_data) == 92, "Should be 92"
