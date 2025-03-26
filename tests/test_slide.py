from tests.__init__ import *

def test_fake_trefoil_slide():
    fake_trefoil = Diagram([
        (4, 1, 5, 2), (5, 3, 6, 2), (6, 3, 1, 4)
    ])
    target = Diagram([
        (3, 2, 4, 3), (5, 4, 6, 5), (6, 2, 1, 1)
    ])
    assert slide(fake_trefoil, 2, 4, 6) == target

def test_unknot1_slide():
    unknot1 = Diagram([
        (8, 1, 9, 2), (2, 9, 3, 10), (3, 11, 4, 10), (7, 5, 8, 4), (12, 6, 1, 5), (6, 12, 7, 11)
    ])
    target = Diagram([
        (8, 1, 9, 2), (2, 9, 3, 10), (3, 11, 4, 10), (11, 5, 12, 4), (6, 6, 7, 5), (7, 1, 8, 12)
    ])
    assert slide(unknot1, 5, 7, 12) == target

def test_unknot2_slide():
    unknot2 = Diagram([
        (2, 11, 3, 12), (3, 8, 4, 9), (4, 10, 5, 9), (5, 1, 6, 12), (6, 1, 7, 2), (7, 10, 8, 11)
    ])
    target = Diagram([
        (1, 10, 2, 11), (3, 8, 4, 9), (4, 10, 5, 9), (5, 1, 6, 12), (6, 11, 7, 12), (7, 2, 8, 3)
    ])
    assert slide(unknot2, 2, 7, 11) == target

def test_undefined_valid_face_slide():
    with pytest.raises(ReidemeisterError):
        slide(knot(3, 1), 2, 4, 6)

def test_undefined_invalid_face_slide():
    with pytest.raises(ReidemeisterError):
        slide(knot(3, 1), 1, 2, 4)
