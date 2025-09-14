from rest_framework import serializers
from .models import User, Candidate, Vote

class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'department']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id','candidate','timestamp']
    
    def create(self, validated_data):
        # The voter will be automatically assigned in the view
        return Vote.objects.create(**validated_data)
