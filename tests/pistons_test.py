from simulator import Pistons

def test_start(piston_length):
    piston_length=10

    pistons=Pistons(piston_length)
    assert len(pistons.status_list) == piston_length

    for i in pistons.status_list:
        assert piston == piston_state.off







