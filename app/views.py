from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status

from app.tokens import TokenGenerator
from django.template.loader import render_to_string

# from app.permissions import IsAllowedToWrite
from app.permissions import IsAllowedToRead, IsOwnerOrReadonly
from .models import User, Post
from .serializers import POstSerializer, UserSerializer, RegistrationSerializer, UserPasswordResetSerializer, \
    CustomPasswordResetSerializer, CustomPasswordResetDoneSerializer


@api_view(['GET', 'POST'])
def registration_view(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = RegistrationSerializer(user, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
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
                    email=serializer.validated_data['email'],
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
    user = User.objects.all()
    serializer_class = POstSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadonly,)

    def send_email(self, request, pk):
        post = Post.objects.get(pk=pk)
        status = post.status
        user = post.owner.username
        send_mail("Status",
                  "Dear " +user+ "," +
                              " It has been "+ status,
                  "from@example.com",
                  [post.owner.email],
                  fail_silently=False)
        return render(request, 'app/index.html')

    def update(self, request, pk, *args, **kwargs):
        response = super(PostDetail, self).update(request, *args, **kwargs)
        self.send_email(request, pk)
        return response


@csrf_exempt
@api_view(['POST'])
def passwordreset_view(request):
    if request.method == 'POST':
        # user = User.objects.all()
        serializer = CustomPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # print(email)
            if email != '':
                email = User.objects.get(email=email)
                if not email:
                    return Response(data={'message': "Couldn't found matching email!"})
                else:
                    # token, created = Token.objects.get_or_create(user=user)email
                    # return Response(TokenGenerator().make_token(email))
                    return Response(send_email(email))
            else:
                return Response(data={'message': 'Empty email provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email(user):
    message = render_to_string('app/password_reset_email.html', {
        'protocol': 'http',
        'domain': 'localhost:8000',
        'uid': str(user.pk),
        'token': TokenGenerator().make_token(user),
    })
    mail_subject = 'Password Reset.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    send = email.send()
    return send

@csrf_exempt
@api_view(['POST'])
def passwordresetdone_view(request, uid):
    if request.method == 'POST':
        user = User.objects.get(pk=uid)
        serializer = CustomPasswordResetDoneSerializer(data=request.POST)
        if serializer.is_valid(request.POST):
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']
            if password == password2:
                user.set_password(password)
                user.save()
                return Response("Password reset done!")
            else:
                return Response("Confirm your password and try again")
        else:
            return Response(serializer.errors)

        return Response(serializer.data)



# def send_email(request):
#     subject = request.POST.get('subject', 'Status')
#     message = request.POST.get('message', 'this is message')
#     from_email = request.POST.get('from_email', 'from@example.com')
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['asminrai7@gmail.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/posts/')
#     else:
#         return HttpResponse('Make sure all fields are entered and valid.')


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




