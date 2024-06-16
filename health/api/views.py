from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer
from ..models import HealthRecord, HealthPlan
from ..nlp_processor import simple_health_nlp


from .serializers import (
    HealthRecordSerializer,
    HealthRecordUpdateSerializer,
    HealthPlanSerializer,
)


class UserRegister(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            return Response(
                {"error": "Username, password, and email are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = settings.AUTH_USER_MODEL.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )


class UserLogin(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HealthRecordList(APIView):
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HealthRecordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        records = HealthRecord.objects.filter(user=request.user)
        serializer = HealthRecordSerializer(records, many=True)
        return Response(serializer.data)


class HealthRecordDetail(APIView):
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, record_id):
        try:
            return HealthRecord.objects.get(pk=record_id, user=self.request.user)
        except HealthRecord.DoesNotExist:
            raise Http404

    def get(self, request, record_id):
        record = self.get_object(record_id)
        serializer = HealthRecordSerializer(record)
        return Response(serializer.data)

    def put(self, request, record_id):
        record = self.get_object(record_id)
        serializer = HealthRecordUpdateSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, record_id):
        record = self.get_object(record_id)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HealthPlanList(APIView):
    serializer_class = HealthPlanSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = HealthPlan.objects.filter(user=request.user)
        serializer = HealthPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HealthPlanSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthPlanDetail(APIView):
    serializer_class = HealthPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, plan_id):
        try:
            return HealthPlan.objects.get(pk=plan_id, user=self.request.user)
        except HealthPlan.DoesNotExist:
            raise Http404

    def get(self, request, plan_id):
        plan = self.get_object(plan_id)
        serializer = HealthPlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, plan_id):
        plan = self.get_object(plan_id)
        serializer = HealthPlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = self.get_object(plan_id)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HealthQueryView(APIView):
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response(
                {"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        advice = simple_health_nlp(query)
        return Response({"query": query, "advice": advice}, status=status.HTTP_200_OK)
