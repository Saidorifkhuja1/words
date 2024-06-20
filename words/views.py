from rest_framework import generics, permissions, status
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from accounts.utils import unhash_token
from .models import Word
from .serializzers import *
from .permissions import IsOwner




class APIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class WordListAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    pagination_class = APIListPagination



class WordDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WordSerializer
    queryset = Word.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class CreateWordAPIView(generics.CreateAPIView):
    serializer_class = WordBaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Decode the token and retrieve user information
            decoded_token = unhash_token(self.request.headers)
            user_id = decoded_token['user_id']  # Assuming 'user_id' is in the decoded token payload
            user = User.objects.get(pk=user_id)

            # Set the user for the word being created
            serializer.save(user=user)

        except Exception as e:
            raise APIException("Failed to create word: " + str(e))



# class CreateWordAPIView(generics.CreateAPIView):
#     serializer_class = WordBaseSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save()
#


class UpdateWordAPIView(generics.UpdateAPIView):
    serializer_class = WordUseSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Word.objects.all()

    def perform_update(self, serializer):
        serializer.save()



class DeleteWordAPIView(generics.DestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        instance.delete()












