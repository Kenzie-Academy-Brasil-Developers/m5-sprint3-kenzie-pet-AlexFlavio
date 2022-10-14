from django.test import TestCase

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from animals.models import Animal
from groups.models import Group
from traits.models import Trait


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.snow_data = {
            "name": "Snow",
            "age": 3,
            "weight": 20.43,
            "sex": "Macho",
        }

        cls.group_data = {"name": "Cães", "scientific_name": "Canis Familiaris"}
        cls.group = Group.objects.create(**cls.group_data)
        cls.snow = Animal.objects.create(**cls.snow_data, group=cls.group)

        cls.snow.save()

        ...

    def test_animal_object_representation(self):
        expected = f"<Animal {self.snow.id} - {self.snow.name}>"
        result = repr(self.snow)
        msg = 'Verifique se o "__repr__" de objetos "User" está correto'
        self.assertEqual(expected, result, msg)
        ...

    def test_convert_dog_age_to_human_years_method(self):
        expected = 48
        result = self.snow.convert_dog_age_to_human_years()
        msg = 'Verifique se o método "convert_dog_age_to_human_years" está retornando como esperado'
        self.assertEqual(expected, result, msg)
        ...

    def test_name_max_length(self):
        expected_max_length = 50
        result_max_length = Animal._meta.get_field("name").max_length
        msg = f'Verifique se a propriedade "max_length" de name foi definida como {expected_max_length}'
        self.assertEqual(expected_max_length, result_max_length, msg)
        ...

    def test_sex_max_length(self):
        expected_max_length = 15
        result_max_length = Animal._meta.get_field("sex").max_length
        msg = f'Verifique se a propriedade "max_length" de name foi definida como {expected_max_length}'
        self.assertEqual(expected_max_length, result_max_length, msg)
        ...


class AnimalRelationshipTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.snow_data = {
            "name": "Snow",
            "age": 3,
            "weight": 20.43,
            "sex": "Macho",
        }

        cls.group1 = Group.objects.create(
            name="cães", scientific_name="Canis Familiaris"
        )
        cls.group2 = Group.objects.create(
            name="patos", scientific_name="Cairina moschata"
        )

        cls.trait1 = Trait.objects.create(name="Pelo Alto")
        cls.trait2 = Trait.objects.create(name="Asas Brancas")
        cls.snow = Animal.objects.create(**cls.snow_data, group=cls.group1)
        ...

    def test_many_to_one_relationship_with_group(self):
        expected = "'Group' object has no attribute 'add'"

        with self.assertRaisesMessage(AttributeError, expected):
            self.snow.group.add(self.group2)
            self.snow.save()

        ...

    def test_many_to_many_relationsship_with_traits(self):

        self.snow.traits.add(self.trait1)
        self.snow.save()

        self.snow.traits.add(self.trait2)
        self.snow.save()

        expected = 2
        result = self.snow.traits.count()
        msg = f"Verifique se snow possui {2} Traits"

        self.assertEqual(expected, result, msg)
        ...


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group = Group.objects.create(
            name="cães", scientific_name="Canis Familiaris"
        )
        ...

    def test_name_max_length(self):
        expected_max_length = 20
        result_max_length = Group._meta.get_field("name").max_length
        msg = f'Verifique se a propriedade "max_length" de name foi definida como {expected_max_length}'
        self.assertEqual(expected_max_length, result_max_length, msg)
        ...

    def test_name_unique(self):
        expected = True
        result = Group._meta.get_field("name").unique
        msg = (
            f'Verifique se a propriedade "unique" de name foi definida como {expected}'
        )
        self.assertEqual(expected, result, msg)
        ...

    def test_scientific_name_max_length(self):
        expected = 20
        result = Group._meta.get_field("scientific_name").max_length
        msg = f'Verifique se a propriedade "max_length" de scientific_name_unique foi definida como {expected}'
        self.assertEqual(expected, result, msg)
        ...

    def test_scientific_name_unique(self):
        expected = True
        result = Group._meta.get_field("scientific_name").unique
        msg = f'Verifique se a propriedade "unique" de scientific_name_unique foi definida como {expected}'
        self.assertEqual(expected, result, msg)
        ...


class TraitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.trait = Trait.objects.create(name="Pelo Alto")
        ...

    def test_name_max_length(self):
        expected = 20
        result = Trait._meta.get_field("name").max_length
        msg = f'Verifique se a propriedade "max_length" de name foi definida como {expected}'
        self.assertEqual(expected, result, msg)
        ...

    def test_name_unique(self):
        expected = True
        result = Trait._meta.get_field("name").unique
        msg = (
            f'Verifique se a propriedade "unique" de name foi definida como {expected}'
        )
        self.assertEqual(expected, result, msg)
        ...
