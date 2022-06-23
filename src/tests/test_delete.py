import requests


class TestDelete:
    def test_delete_person(self):
        url = "http://localhost:8000/delete/person/1"
        resp = requests.delete(url)
        assert resp.status_code in [200, 400]

    def test_delete_animal(self):
        url = "http://localhost:8000/delete/animal/1"
        resp = requests.delete(url)
        assert resp.status_code in [200, 400]

    def test_delete_specie(self):
        url = "http://localhost:8000/delete/species/wolf"
        resp = requests.delete(url)
        assert resp.status_code in [200, 400]
