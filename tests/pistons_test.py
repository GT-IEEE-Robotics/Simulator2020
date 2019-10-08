from simulator import Pistons

def test_start():
    piston_length = 10

    pistons = Pistons.Pistons(piston_length)
    assert len(pistons.status_list) == piston_length

    for piston in pistons.status_list:
        assert piston == Pistons.piston_state.off







