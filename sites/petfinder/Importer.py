from .PetFinderClient import PetFinderClient
import json


class Importer:
    def __init__(self):
        self.client = PetFinderClient()

    async def crawl(self):
        # resp = await self.client.Get_Organization_Animals()
        # print("Headers: ", resp.headers)
        # print("Cookies: ", resp.cookies)
        # print(resp.status_code)
        # json_resp = await resp.json()
        # print(json.dumps(json_resp, indent=2))

        created_id = await self.client.create_animal()

        names = await self.client.Get_Organization_Animal_Names()
        print(names)

        # await self.client.update_animal(created_id)
        await self.client.update_animal(created_id)
