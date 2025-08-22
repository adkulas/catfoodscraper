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
    

    async def update_animal(self, animal_id):
        headers = {
            "Cookie": f"PFSESSION={self.pfsession}"
        }

        response = await self.client.post(
            "https://svc.petfinder.com/graphql",
            json= {
                "operationName": "UpdatePslAnimal",
                "variables": {
                    "animal": {
                        "animalType": "3",
                        "animalName": "test2",
                        "description": "The bio...",
                        "notes": "",
                        "internalNotes": "",
                        "tags": [
                            "Affectionate",
                            "Smart",
                            "Quiet",
                            "Funny",
                            "Athletic",
                            "Brave",
                            "Gentle",
                            "Friendly",
                            "Protective",
                            "Independent",
                            "Couch",
                            "Curious",
                            "Loves",
                            "Loyal",
                            "Dignified",
                            "Playful"
                        ],
                        "primaryPhotoId": "",
                        "behavior": {
                            "activityLevel": None,
                            "interactionsOtherAnimals": None,
                            "houseTrained": 1,
                            "requiresFencedYard": None,
                            "knowsBasicCommands": None,
                            "personalityTraits": [
                                "Affectionate",
                                "Smart",
                                "Quiet",
                                "Funny",
                                "Athletic",
                                "Brave",
                                "Gentle",
                                "Friendly",
                                "Protective",
                                "Independent",
                                "Couch",
                                "Curious",
                                "Loves",
                                "Loyal",
                                "Dignified",
                                "Playful"
                            ],
                            "interactions": {
                                "otherAnimals": 3,
                                "cats": 3,
                                "dogs": 3,
                                "kids": 3
                            }
                        },
                        "organization": {
                            "organizationId": "55110",
                            "legacyOrganizationId": 55110,
                            "organizationAnimalId": "",
                            "contactId": "",
                            "legacyContactId": None,
                            "locationId": "150641",
                            "legacyLocationId": 150641,
                            "internalNotes": "PCON profile info"
                        },
                        "physical": {
                            "birthDate": "2025-04-02",
                            "coatLength": "Short",
                            "declawed": False,
                            "sex": "Female",
                            "speciesId": 5,
                            "spayedNeutered": True,
                            "specialNeeds": False,
                            "specialNeedsNotes": None,
                            "vaccinated": True,
                            "breed": {
                                "primary": 86,
                                "secondary": None,
                                "mixed": False,
                                "primaryName": "Domestic Short Hair",
                                "secondaryName": "Unknown"
                            },
                            "color": {
                                "primary": "Black",
                                "secondary": "Torbie",
                                "tertiary": "Lilac Point"
                            },
                            "size": "Medium",
                            "age": "Baby"
                        },
                        "residency": {
                            "adoptionDate": None,
                            "adoptionFee": 0,
                            "adoptionStatus": None,
                            "adoptionStatusChangeDate": None,
                            "displayAdoptionFee": False,
                            "intakeDate": "2025-08-20",
                            "intakeType": None,
                            "transferDate": None,
                            "transferFromOrganizationId": None
                        },
                        "meta": {
                            "recordStatus": "draft"
                        }
                    },
                    "updateAnimalId": animal_id
                },
                "query": "mutation UpdatePslAnimal($updateAnimalId: String!, $animal: AnimalUpdate!) {\n  updateAnimal(id: $updateAnimalId, animal: $animal) {\n    animalName\n    animalType\n    description\n    extendedDescription\n    microchipId\n    primaryPhotoId\n    primaryPhotoUrl\n    notes\n    internalNotes\n    tags\n    importUpdatesEnabled\n    importDeletesEnabled\n    animalId\n    animalTypeName\n    legacyAnimalId\n    platformAnimalId\n    behavior {\n      activityLevel\n      interactionsOtherAnimals\n      houseTrained\n      requiresFencedYard\n      knowsBasicCommands\n      personalityTraits\n      interactions {\n        cats\n        dogs\n        otherAnimals\n        kids\n        __typename\n      }\n      __typename\n    }\n    meta {\n      revision\n      recordStatus\n      create {\n        time\n        identity {\n          client\n          user\n          __typename\n        }\n        __typename\n      }\n      update {\n        time\n        __typename\n      }\n      importDeletesEnabled\n      importUpdatesEnabled\n      publishTime\n      __typename\n    }\n    organization {\n      organizationId\n      legacyOrganizationId\n      organizationAnimalId\n      contactId\n      legacyContactId\n      locationId\n      legacyLocationId\n      internalNotes\n      name\n      display_id\n      __typename\n    }\n    _organization {\n      organizationName\n      organizationType\n      organizationTypeOther\n      displayId\n      taxId\n      primaryPhotoId\n      notes\n      medicalCareProvided\n      missionStatement\n      onsiteVet\n      rehomeProgram\n      supportsRehome\n      spayNeuterPolicy\n      spayNeuterPolicyReason\n      specialServices\n      exportApi\n      exportPartners\n      director\n      employeeCount\n      volunteerCount\n      fosterCount\n      website\n      otherPlatforms\n      animalTypes\n      socialUrl\n      organizationId\n      legacyOrganizationId\n      locations {\n        organizationId\n        legacyLocationId\n        locationName\n        contactName\n        phone\n        email\n        isApptOnly\n        isMapHidden\n        isPublic\n        locationType\n        locationId\n        __typename\n      }\n      adoption {\n        adoptionApplUrl\n        adoptionFeeMax\n        adoptionFeeMin\n        adoptionPolicies\n        annualAdoptions\n        annualFosters\n        annualIntake\n        __typename\n      }\n      primaryContact {\n        legacyContactId\n        firstName\n        lastName\n        phone\n        email\n        linkedin\n        role\n        notes\n        userId\n        legacyUserId\n        contactId\n        __typename\n      }\n      primaryContactId\n      primaryLocationId\n      contacts {\n        legacyContactId\n        firstName\n        lastName\n        phone\n        email\n        linkedin\n        role\n        notes\n        userId\n        legacyUserId\n        contactId\n        __typename\n      }\n      animalTemplates {\n        animalTemplates {\n          legacyAnimalTemplateId\n          templateName\n          animalName\n          description\n          extendedDescription\n          tags\n          animalType\n          animalTemplateId\n          type {\n            id\n            label\n            key\n            attributes\n            coatLengths\n            colors\n            sexes\n            __typename\n          }\n          organization {\n            organizationId\n            legacyOrganizationId\n            organizationAnimalId\n            contactId\n            legacyContactId\n            locationId\n            legacyLocationId\n            internalNotes\n            __typename\n          }\n          species {\n            animalTypeId\n            speciesId\n            name\n            __typename\n          }\n          __typename\n        }\n        nextPageToken\n        __typename\n      }\n      primaryLocation {\n        organizationId\n        legacyLocationId\n        locationName\n        contactName\n        phone\n        email\n        isApptOnly\n        isMapHidden\n        isPublic\n        locationType\n        locationId\n        __typename\n      }\n      mailingAddress {\n        street\n        street2\n        city\n        state\n        postalCode\n        country\n        __typename\n      }\n      publicUrl {\n        url\n        __typename\n      }\n      primaryPhoto {\n        id\n        caption\n        mediaId\n        smallUrl\n        largeUrl\n        fullUrl\n        createdAt\n        updatedAt\n        __typename\n      }\n      photos {\n        id\n        caption\n        mediaId\n        smallUrl\n        largeUrl\n        fullUrl\n        createdAt\n        updatedAt\n        __typename\n      }\n      logo {\n        mediaId\n        createdAt\n        updatedAt\n        __typename\n      }\n      meta {\n        revision\n        recordStatus\n        active\n        deactiveReason\n        enabled\n        lockReason\n        lastActiveTime\n        lastIndexTime\n        __typename\n      }\n      __typename\n    }\n    _location {\n      organizationId\n      legacyLocationId\n      locationName\n      contactName\n      phone\n      email\n      isApptOnly\n      isMapHidden\n      isPublic\n      locationType\n      locationId\n      address {\n        street\n        street2\n        city\n        state\n        postalCode\n        country\n        __typename\n      }\n      geo {\n        latitude\n        longitude\n        __typename\n      }\n      hours {\n        sunday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        monday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        tuesday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        wednesday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        thursday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        friday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        saturday {\n          open\n          close\n          notes\n          isOpen\n          __typename\n        }\n        __typename\n      }\n      organization {\n        organizationName\n        organizationType\n        organizationTypeOther\n        displayId\n        taxId\n        primaryPhotoId\n        notes\n        medicalCareProvided\n        missionStatement\n        onsiteVet\n        rehomeProgram\n        supportsRehome\n        spayNeuterPolicy\n        spayNeuterPolicyReason\n        specialServices\n        exportApi\n        exportPartners\n        director\n        employeeCount\n        volunteerCount\n        fosterCount\n        website\n        otherPlatforms\n        animalTypes\n        socialUrl\n        organizationId\n        legacyOrganizationId\n        primaryContactId\n        primaryLocationId\n        __typename\n      }\n      meta {\n        revision\n        recordStatus\n        __typename\n      }\n      __typename\n    }\n    _contact {\n      legacyContactId\n      firstName\n      lastName\n      phone\n      email\n      linkedin\n      role\n      notes\n      userId\n      legacyUserId\n      contactId\n      __typename\n    }\n    physical {\n      birthDate\n      coatLength\n      declawed\n      sex\n      speciesId\n      speciesName\n      spayedNeutered\n      specialNeeds\n      specialNeedsNotes\n      vaccinated\n      breed {\n        primary\n        primaryName\n        secondary\n        secondaryName\n        mixed\n        __typename\n      }\n      color {\n        primary\n        secondary\n        tertiary\n        __typename\n      }\n      size {\n        label\n        range {\n          min\n          max\n          label\n          __typename\n        }\n        __typename\n      }\n      age {\n        value\n        label\n        rangeLabel\n        __typename\n      }\n      __typename\n    }\n    residency {\n      adoptionDate\n      adoptionFee\n      adoptionFeeWaived\n      adoptionStatus\n      adoptionStatusChangeDate\n      displayAdoptionFee\n      intakeDate\n      intakeType\n      transferDate\n      transferFromOrganizationId\n      __typename\n    }\n    history {\n      field\n      original\n      update\n      changeType\n      changeDate\n      changedBy\n      sectionChanged\n      __typename\n    }\n    adoptionInquiries {\n      adoptionInquiries {\n        id\n        user {\n          firstName\n          lastName\n          email\n          __typename\n        }\n        __typename\n      }\n      totalCount\n      __typename\n    }\n    views {\n      total\n      sum\n      days {\n        date\n        count\n        __typename\n      }\n      __typename\n    }\n    sponsorAPetUrl {\n      url\n      __typename\n    }\n    distance\n    pagination {\n      countPerPage\n      totalCount\n      currentPage\n      totalPages\n      __typename\n    }\n    facets {\n      facet\n      values {\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    publicUrl\n    debuggingMetadata {\n      source\n      nestedErrors\n      authUsed\n      __typename\n    }\n    __typename\n  }\n}"
            },
            headers=headers
        )
        print(response.status_code)
        json_resp = await response.json()
        print(json.dumps(json_resp, indent=2))
