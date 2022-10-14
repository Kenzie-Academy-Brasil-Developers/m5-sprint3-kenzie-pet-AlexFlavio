from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from .serializers import AnimalSerializer
from .models import Animal

# Create your views here.


class AnimalView(APIView):
    def get(self, request):
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)
        ...

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
        ...


class AnimalDetailView(APIView):

    def get(self,request,animal_id:int):
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)
        ...


    def patch(self, request, animal_id: int):
        error_keys = ["traits", "group", "sex"]
        errors = {
            key: f"You can not update {key} property."
            for key, value in request.data.items()
            if key in error_keys
        }

        if errors:
            return Response(errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
        ...

    def delete(self,request,animal_id:int):
        animal = get_object_or_404(Animal, id=animal_id)
        animal.delete()
        return Response(status.HTTP_204_NO_CONTENT)
        ...
