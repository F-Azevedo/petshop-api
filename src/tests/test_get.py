import requests


class TestGet:
    def test_get_all_owners(self):
        url = "http://localhost:8000/owners"
        resp = requests.get(url)
        assert resp.status_code == 200

    def test_get_owner_number_one(self):
        url = "http://localhost:8000/owners/1"
        resp = requests.get(url)
        assert resp.status_code in [200, 400]

    def test_get_pets_from_owner(self):
        url = "http://localhost:8000/owners/1/pets"
        resp = requests.get(url)
        assert resp.status_code in [200, 400]

    def test_get_one_pet_from_owner(self):
        url = "http://localhost:8000/owners/1/pets/2"
        resp = requests.get(url)
        assert resp.status_code in [200, 400]

    def test_get_all_pets(self):
        url = "http://localhost:8000/pets"
        resp = requests.get(url)
        assert resp.status_code == 200

    def test_get_pets_count(self):
        url = "http://localhost:8000/pets/count"
        resp = requests.get(url)
        assert resp.status_code == 200

    def test_get_pets_from_specie(self):
        url = "http://localhost:8000/pets/platypus"
        resp = requests.get(url)
        assert resp.status_code in [200, 400]

    def test_get_owner_of_each_pet_of_specie(self):
        url = "http://localhost:8000/pets/platypus/owners"
        resp = requests.get(url)
        assert resp.status_code in [200, 400]
