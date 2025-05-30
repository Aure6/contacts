import os
import json
import pytest
import contacts_manager as cm

TEST_FILE = "test_contacts.txt"

@pytest.fixture(autouse=True)
def run_around_tests():
    """Create a test file before running tests and delete it afterwards"""
    # Avant chaque test : vider contacts et supprimer fichier test s'il existe
    cm.contacts.clear()
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    # Après test : nettoyer fichier test
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_ajouter_contact_valide():
    """Test adding a valid contact"""
    cm.ajouter_contact_moteur("Alice", "alice.jpg")
    assert len(cm.contacts) == 1
    assert cm.contacts[0]["name"] == "Alice"

def test_ajouter_contact_nom_vide():
    """Test adding a contact with an empty name"""
    cm.ajouter_contact_moteur("", "bob.jpg")
    assert cm.contacts[0]["name"] == "Sans nom"
    assert cm.contacts[0]["image"] == "bob.jpg"

def test_ajouter_contact_image_vide():
    """Test adding a contact with an empty image"""
    cm.ajouter_contact_moteur("Charlie", "")
    assert cm.contacts[0]["name"] == "Charlie"
    assert cm.contacts[0]["image"] == "placeholder.jpg"

def test_ajouter_contact_champs_vides():
    """Test adding a contact with empty name and image"""
    with pytest.raises(ValueError):
        cm.ajouter_contact_moteur("", "")

def test_sauvegarder_et_charger_contacts():
    """Test saving and loading contacts"""
    cm.ajouter_contact_moteur("Alice", "alice.jpg")
    cm.sauvegarder_contacts(TEST_FILE)
    
    # Vider la liste pour tester le chargement
    cm.contacts.clear()
    cm.charger_contacts(TEST_FILE)
    
    assert len(cm.contacts) == 1
    assert cm.contacts[0]["name"] == "Alice"
    assert cm.contacts[0]["image"] == "alice.jpg"

def test_charger_contacts_fichier_inexistant():
    """Test loading contacts from a non-existent file"""
    # Assurer que fichier test n'existe pas
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    cm.charger_contacts(TEST_FILE)
    assert cm.contacts == []
