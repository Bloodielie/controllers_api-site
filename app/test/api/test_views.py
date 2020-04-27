from fastapi.testclient import TestClient

path = '/api/brest'


def test_get_situation_in_city(client: TestClient):
    def main_test(r):
        json = r.json()
        assert r.status_code == 200
        assert isinstance(json, dict)

    response = client.get(f'{path}/get_situation/all?selection_bus_stop=dirty')
    main_test(response)
    response = client.get(f'{path}/get_situation/1?selection_bus_stop=dirty')
    main_test(response)


def test_get_diverse_data(client: TestClient):
    def main_test(r):
        json = r.json()
        assert r.status_code == 200
        assert isinstance(json, list)
        assert len(json) > 0
        assert isinstance(json[0], str)

    response = client.get(f'{path}/city_stops')
    main_test(response)
    response = client.get(f'{path}/transport_numbers')
    main_test(response)
    response = client.get(f'{path}/transport_stops')
    main_test(response)
