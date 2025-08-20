import pytest
import asyncio
from sites.petfinder.PetFinderClient import PetFinderClient

@pytest.mark.asyncio
async def test_get_organization_animals():
    # Initialize the client
    client = PetFinderClient()

    # Call the method
    response = await client.Get_Organization_Animals()

    print(response.status_code)  # Print the status code for debugging

    # Print the response JSON
    print(response.json())

    # Optionally, add assertions to validate the response
    # assert response.status_code == 200
    # assert "data" in response.json()