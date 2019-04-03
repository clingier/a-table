"""Test pour les fonctions dans utils"""
from atable.utils import normalize_aliment_lists


def test_normalize_aliment_lists1() -> None:
    """Test 1 of normalize_aliment."""
    requete = "des tomate avec un chien et des balles dans les sardines"
    assert normalize_aliment_lists(requete) == ["sardine", "tomate"]


def test_normalize_aliment_lists2() -> None:
    """Test 2 of normalize_aliment."""
    requete = "Ne devrait rien renvoyer aksfsadf;lkjwerqw[rjqrow rpwnq"
    assert normalize_aliment_lists(requete) == []


def test_normalize_aliment_lists3() -> None:
    """Test 3 of normalize_aliment."""
    requete = "topinambour, celeri-rave et pissenlit"
    # La liste peut etre amelioree
    assert normalize_aliment_lists(requete) == ['celeri', 'topinambour']
