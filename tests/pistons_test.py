from simulator import Pistons

def test_start():
    piston_length = 10

    pistons = Pistons.Pistons(piston_length)
    assert len(pistons.status_list) == piston_length

    for piston in pistons.status_list:
        assert piston == Pistons.piston_state.off

    pistons.turn_on_piston(1)
    assert pistons.status_list[1] == Pistons.piston_state.on

    pistons.turn_off_piston(1)
    assert pistons.status_list[1] == Pistons.piston_state.off

    print(pistons.piston_status())


test_start()