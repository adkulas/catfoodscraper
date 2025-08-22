from typing import List, Optional
from interaction_types import InteractionTypes


class Animal:
    class Behavior:
        class Interactions:
            def __init__(
                self,
                good_with_other_animals: int = InteractionTypes.UNKNOWN,
                good_with_cats: int = InteractionTypes.UNKNOWN,
                good_with_dogs: int = InteractionTypes.UNKNOWN,
                good_with_kids: int = InteractionTypes.UNKNOWN,
            ):
                self.good_with_other_animals = good_with_other_animals
                self.good_with_cats = good_with_cats
                self.good_with_dogs = good_with_dogs
                self.good_with_kids = good_with_kids

        def __init__(
            self,
            interactions: "Animal.Behavior.Interactions",
            personality_traits: List[str],
            house_trained: int = 1,
        ):
            self.interactions = interactions

            valid_traits = [
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
                "Playful",
            ]

            self.personality_traits = personality_traits.filter(
                lambda trait: trait in valid_traits
            )
            self.house_trained = house_trained

    class Organization:
        def __init__(
            self,
            organization_id: str = "55110",
            legacy_organization_id: int = 55110,
            organization_animal_id: str = "",
            contact_id: str = "",
            legacy_contact_id: Optional[int] = None,
            location_id: str = "150641",
            legacy_location_id: int = 150641,
            shelter_notes: str = "",
        ):
            self.organization_id = organization_id
            self.legacy_organization_id = legacy_organization_id
            self.organization_animal_id = organization_animal_id
            self.contact_id = contact_id
            self.legacy_contact_id = legacy_contact_id
            self.location_id = location_id
            self.legacy_location_id = legacy_location_id
            self.shelter_notes = shelter_notes
