import requests
from requests.structures import CaseInsensitiveDict


class TestPost:
    def test_post_person(self):
        url = "http://localhost:8000/new/person"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = """
        {
          "name": "Laiola",
          "document": 5,
          "dateOfBirth": "2022-06-23"
        }
        """
        resp = requests.post(url, headers=headers, data=data)
        assert resp.status_code in [201, 400]

    def test_post_animal(self):
        url = "http://localhost:8000/new/animal"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = """
        {
          "name": "Garfield",
          "cost": 100,
          "species": "cat",
          "owner_id": 1
        }
        """
        resp = requests.post(url, headers=headers, data=data)
        assert resp.status_code in [201, 400]

    def test_post_specie(self):
        url = "http://localhost:8000/new/species"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = """
        {
          "name": "wolf"
        }
        """
        resp = requests.post(url, headers=headers, data=data)
        assert resp.status_code in [201, 400]
