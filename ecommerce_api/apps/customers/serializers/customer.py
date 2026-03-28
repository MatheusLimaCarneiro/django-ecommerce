from rest_framework import serializers
from ..models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    def validate_phone(self, value):
        if value:
            value = value.strip()
            if len(value) > 20:
                raise serializers.ValidationError("The phone number must be at most 20 characters long.")
            
            if len(value) < 5:
                raise serializers.ValidationError("The phone number must be at least 5 characters long.")

            if not value.isdigit():
                raise serializers.ValidationError("The phone must only contain numbers.")
        return value

    def validate_address(self, value):
        if value:
            value = value.strip()

            if len(value) < 5:
                raise serializers.ValidationError("The address must be at least 5 characters long.")
        return value

    def validate_city(self, value):
        if value:
            value = value.strip()

            if any(char.isdigit() for char in value):
                raise serializers.ValidationError("The city cannot contain numbers.")
            
        return value

    def validate_state(self, value):
        if value:
            value = value.strip()

            if any(char.isdigit() for char in value):
                raise serializers.ValidationError("The state cannot contain numbers.")
        
            if len(value) != 2:
                raise serializers.ValidationError("The state must be a 2-letter abbreviation.")
        
            return value.upper()

        return value 

    class Meta:
        model = CustomerProfile
        fields = ['id','username','email','phone','address','city','state','created_at']
        read_only_fields = ['created_at', 'username', 'email']