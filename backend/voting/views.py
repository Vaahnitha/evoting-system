from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.db.models import Count
from .models import Candidate, Vote
from .serializers import CandidateSerializer, VoteSerializer


# List all candidates
class CandidateListView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Cast a vote
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if user has already voted
        if Vote.objects.filter(voter=self.request.user).exists():
            raise serializers.ValidationError("You have already voted.")
        
        serializer.save(voter=self.request.user)


# Show election results
class ResultsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Get all candidates with their vote counts
        candidates_data = (
            Candidate.objects.annotate(votes=Count("vote"))
            .values("id", "name", "department", "votes")
        )
        
        # Calculate total votes
        total_votes = sum(candidate['votes'] for candidate in candidates_data)
        
        # Calculate percentage for each candidate
        results = []
        for candidate in candidates_data:
            percentage = (candidate['votes'] / total_votes * 100) if total_votes > 0 else 0
            
            results.append({
                'id': candidate['id'],
                'name': candidate['name'],
                'department': candidate['department'],
                'votes': candidate['votes'],
                'percentage': round(percentage, 2)
            })
        
        return Response({
            'total_votes': total_votes,
            'candidates': results
        })
