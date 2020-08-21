import pytest

from robot import Robot, Direction, IllegalMoveException


@pytest.fixture
def robot():
    return Robot()


def test_constructor(robot):
    state = robot.state()

    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


''' Test Turns '''

def test_north_turn(robot):
    state = robot.state()
    assert state['direction'] == Direction.NORTH

def test_east_turn(robot):
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.EAST

def test_south_turn(robot):
    robot.turn()
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.SOUTH

def test_west_turn(robot):
    robot.turn()
    robot.turn()
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.WEST


''' Test Moves '''

def test_move_north(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1

def test_move_east(robot):
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2

def test_move_south(robot):
    robot.move()
    robot.turn()
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1

def test_move_west(robot):
    robot.turn()
    robot.move()
    robot.turn()
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1

''' Test Illegal Moves '''

def test_illegal_move_to_south(robot):
    robot.turn()
    robot.turn()
    with pytest.raises(IllegalMoveException):
        robot.move()

def test_illegal_move_to_west(robot):
    for i in range(3):
        robot.turn()
    with pytest.raises(IllegalMoveException):
        robot.move()

def test_illegal_move_to_north(robot):
    for i in range(9):
        robot.move()
    with pytest.raises(IllegalMoveException):
        robot.move()

def test_illegal_move_to_east(robot):
    robot.turn()
    for i in range(9):
        robot.move()
    with pytest.raises(IllegalMoveException):
        robot.move()

''' Test Back Tracks '''

def test_back_track_without_history(robot):
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1

def test_back_track_after_making_a_move(robot):
    robot.move()
    robot.move()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 9
    assert state['col'] == 1

def test_back_track_after_making_a_turn(robot):
    robot.turn()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1

def test_back_track_after_making_multiple_moves(robot):
    for i in range(5):
        robot.move()
    robot.turn()
    for i in range(4):
        robot.move()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.EAST
    assert state['row'] == 5
    assert state['col'] == 4

def test_back_track_all_multiple_moves_after_making_multiple_moves(robot):
    for i in range(9):
        robot.move()
    robot.turn()  # turn to face East
    for j in range(9):
        robot.move()
    robot.turn()  # turn to face South
    for k in range(9):
        robot.move()
    robot.turn()  # turn to face West
    for x in range(9):
        robot.move()


    cols = list(range(2,11))

    for x in range(9):
        robot.back_track()
        state = robot.state()
        assert state['direction'] == Direction.WEST
        assert state['row'] == 10
        assert state['col'] == cols[x]

    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.SOUTH
    assert state['row'] == 10
    assert state['col'] == 10

    rows = list(range(9,0,-1))
    for y in range(9):
        robot.back_track()
        state = robot.state()
        assert state['direction'] == Direction.SOUTH
        assert state['row'] == rows[y]
        assert state['col'] == 10

    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.EAST
    assert state['row'] == 1
    assert state['col'] == 10

    cols = list(range(9,0,-1))
    for z in range(9):
        robot.back_track()
        state = robot.state()
        assert state['direction'] == Direction.EAST
        assert state['row'] == 1
        assert state['col'] == cols[z]

    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 1
    assert state['col'] == 1

    rows = list(range(2,11))
    for a in range(9):
        robot.back_track()
        state = robot.state()
        assert state['direction'] == Direction.NORTH
        assert state['row'] == rows[a]
        assert state['col'] == 1
