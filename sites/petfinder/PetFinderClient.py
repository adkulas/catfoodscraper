from utils.http_client import HttpClient
from rnet import Cookie
import os
import json
from furl import furl

class PetFinderClient(HttpClient):
    def __init__(self, *, proxies=None, delay_range=(0.9, 2.0)):
        super().__init__(proxies=proxies, delay_range=delay_range)
        self.pfsession = os.getenv("PETFINDER_PFSESSION")
        cookie = Cookie(name = "PFSESSION", value = self.pfsession )
        self.client.set_cookie("https://pro.petfinder.com", cookie)

    async def Get_Organization_Animals(self):
        headers = {
            "Cookie": f"PFSESSION={self.pfsession}"
        }

        return await self.client.post(
            "https://services.petfinder.com/graphql",
            json= {
                "operationName": "GetOrganizationAnimals",
                "variables": {
                    "displayId": "on742",
                    "first": 30,
                    "searchInput": {
                        "gender": [],
                        "animalType": [],
                        "adoptionStatus": [],
                        "query": "",
                        "age": [],
                        "breed": [],
                        "recordStatus": [
                            "PUBLISHED",
                            "DRAFT"
                        ],
                        "sortField": "CREATED",
                        "sortDir": "DESC"
                    }
                },
                "query": "query GetOrganizationAnimals($displayId: ID, $first: Int, $after: String, $searchInput: OrgAnimalSearchInput) {\n  sourceOrganization(displayId: $displayId) {\n    id\n    animals(first: $first, after: $after, searchInput: $searchInput) {\n      edges {\n        cursor\n        node {\n          ... on SourceAnimal {\n            ...AbstractAnimal\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      pageInfo {\n        startCursor\n        endCursor\n        hasNextPage\n        hasPreviousPage\n        __typename\n      }\n      totalCount\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AbstractAnimal on SourceAnimal {\n  id\n  organization {\n    name\n    displayId\n    __typename\n  }\n  publicContact {\n    email\n    phone\n    address {\n      address1\n      address2\n      city\n      state\n      postcode\n      country\n      __typename\n    }\n    __typename\n  }\n  type_ {\n    id\n    name\n    __typename\n  }\n  species_ {\n    id\n    name\n    __typename\n  }\n  breeds {\n    primary {\n      id\n      name\n      __typename\n    }\n    secondary {\n      id\n      name\n      __typename\n    }\n    mixed\n    __typename\n  }\n  colors {\n    primary\n    secondary\n    tertiary\n    __typename\n  }\n  age\n  gender\n  size\n  coat\n  name\n  description\n  organizationAnimalId\n  primaryPhotoUrl\n  adoptionStatus_\n  adoptionStatusChanged\n  attributes {\n    spayedNeutered\n    houseTrained\n    declawed\n    specialNeeds\n    shotsCurrent\n    __typename\n  }\n  environment {\n    children\n    cats\n    dogs\n    otherAnimals\n    animals\n    __typename\n  }\n  tags\n  adoptionFee\n  adoptionFeeWaived\n  displayAdoptionFee\n  privateContact_ {\n    id\n    firstName\n    lastName\n    __typename\n  }\n  location {\n    id\n    name\n    __typename\n  }\n  extendedDescription\n  internalNotes\n  arrival\n  arrivalDate\n  adoptionDate\n  birthDate\n  recordStatus\n  specialNeeds\n  organizationTransferredFrom\n  transferDate\n  importUpdatesEnabled\n  importDeletesEnabled\n  createdAt\n  updatedAt\n  changeHistory {\n    id\n    type\n    modifiedBy\n    modifiedAt\n    properties\n    adoptionInquiryCount\n    adoptionStatus\n    note\n    oldOrgName\n    newOrgName\n    __typename\n  }\n  validationErrors {\n    error\n    field\n    __typename\n  }\n  video {\n    attachmentId\n    mediaId\n    type\n    url\n    thumbnail\n    service\n    embedCode\n    status\n    __typename\n  }\n  url\n  photos_ {\n    attachmentId\n    mediaId\n    type\n    url\n    thumbnail\n    service\n    embedCode\n    status\n    __typename\n  }\n  statistics {\n    views {\n      total\n      __typename\n    }\n    inquiries {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
            },
            headers=headers
        )
    
    async def create_animal(self):
        response = await self.client.get('https://pro.petfinder.com/_next/data/YCcppK5tXKEBlLBrLSrmq/pro/organization/on742/add-pet/cat.json?organizationId=on742&id=cat',
            headers={ "Cookie": f"PFSESSION={self.pfsession}" }
        )

        print(response.status_code)
        
        json_resp = await response.json()
        redirect = json_resp.get('pageProps', {}).get('__N_REDIRECT', {})
        pet_id = furl(redirect).path.segments[-2]
        print(f"Created new cat, Pet ID: {pet_id}")
        return pet_id



    async def Get_Organization_Animal_Names(self):
        headers = {
            "Cookie": f"PFSESSION={self.pfsession}"
        }

        response = await self.client.post(
            "https://services.petfinder.com/graphql",
            json= {
                "operationName": "GetOrganizationAnimals",
                "variables": {
                    "displayId": "on742",
                    # "first": 3,
                    "searchInput": {
                        "gender": [],
                        "animalType": [],
                        "adoptionStatus": [],
                        "query": "",
                        "age": [],
                        "breed": [],
                        "recordStatus": [
                            "PUBLISHED",
                            "DRAFT"
                        ],
                        "sortField": "CREATED",
                        "sortDir": "DESC"
                    }
                },
                "query": """
                    query GetOrganizationAnimals($displayId: ID, $first: Int, $after: String, $searchInput: OrgAnimalSearchInput) {
                        sourceOrganization(displayId: $displayId) {
                            animals(first: $first, after: $after, searchInput: $searchInput) {
                                edges {
                                    node {
                                        name
                                        id
                                    }
                                }
                            }
                        }
                    }
                """
            },
            headers=headers
        )
        json_resp = await response.json()

        # Extract all the names
        edges = json_resp.get("data", {}).get("sourceOrganization", {}).get("animals", {}).get("edges", [])
        names = {edge.get("node", {}).get("name") for edge in edges if edge.get("node", {}).get("name")}

        return names
