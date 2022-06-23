import requests
from requests.structures import CaseInsensitiveDict


class TestPut:
    def test_update_person(self):
        url = "http://localhost:8000/update/person/4/"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = """
        {
          "name": "Rodrigo Laiola",
          "document": 1,
          "dateOfBirth": "2022-06-23"
        }
        """
        resp = requests.put(url, headers=headers, data=data)
        assert resp.status_code in [200, 400]

    def test_update_animal(self):
        url = "http://localhost:8000/update/animal/3"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = """
        {
          "name": "Garfield",
          "cost": 100,
          "species": "cat",
          "owner_id": 3
        }
        """
        resp = requests.put(url, headers=headers, data=data)
        assert resp.status_code in [200, 400]
