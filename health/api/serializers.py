from rest_framework import serializers
from ..models import HealthRecord, HealthPlan, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ["id", "user", "record_date", "symptoms", "condition"]
        read_only_fields = ("user",)


class HealthRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ["record_date", "symptoms", "condition"]


class HealthPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthPlan
        fields = ["plan_id", "user", "created_at", "plan_details", "valid_until"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        # Ensure the user is saved correctly when creating a new plan
        user = self.context["request"].user
        return HealthPlan.objects.create(user=user, **validated_data)
