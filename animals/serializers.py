from tokenize import group
from rest_framework import serializers
from traitlets import Instance
from animals.models import Animal, Sex
from groups.models import Group
from groups.serializers import GroupSerializer
from traits.models import Trait
from traits.serializers import TraitSerializer


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )

    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj: Animal) -> int:

        return obj.convert_dog_age_to_human_years()
        ...

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        new_group, _ = Group.objects.get_or_create(**group_data)

        animal = Animal.objects.create(**validated_data, group=new_group)

        for trait in traits_data:
            new_trait, _ = Trait.objects.get_or_create(**trait)
            animal.traits.add(new_trait)

        return animal

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    ...
