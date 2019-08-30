from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

# from app.permissions import IsAllowedToWrite
from app.permissions import IsAllowedToRead, IsOwnerOrReadonly
from .models import User,Post
from .serializers import POstSerializer, UserSerializer, RegistrationSerializer

@api_view(['GET', 'POST'])
def registration_view(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = RegistrationSerializer(user, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']
            try:
                user_type = serializer.validated_data['user_type'],
            except:
                user_type = "User"
            try:
                address = serializer.validated_data['address']
            except:
                address = ""
            try:
                phone_number = serializer.validated_data['phone_number']
            except:
                phone_number = ""

            if password == password2:
                user = User(
                    user_type=user_type,
                    username=serializer.validated_data['username'],
                    address=address,
                    phone_number=phone_number

                )
                user.set_password(password)
                user.save()
            else:
                return Response("Confirm your password and try again")
        else:
            return Response(serializer.errors)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'posts': reverse('post-list', request=request),
        # 'posts-create': reverse('post-create', request=request),
    })



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = POstSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = POstSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadonly,)


# class PostList(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = POstSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, * args, **kwargs)
#
#
# class PostCreate(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = POstSerializer
#     permission_classes = (permissions.IsAuthenticated, IsAllowedToWrite)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostDetail(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = POstSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class PostUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = POstSerializer
#     permission_classes = (permissions.IsAuthenticated, IsAllowedToWrite)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAllowedToRead,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)




