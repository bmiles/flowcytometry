from flow_cytometry import make_samples

def inc(x):
    return x + 1


def test_make_samples():
    assert len(make_samples([0,1,2,3], 10)) == 4


def test_answer_pass():
    assert inc(3) == 4
