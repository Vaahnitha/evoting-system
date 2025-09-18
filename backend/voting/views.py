from django.shortcuts import render
from django.utils import timezone

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


# Test endpoint for debugging
class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Test endpoint to verify API connectivity"""
        return Response({
            'message': 'API is working!',
            'timestamp': timezone.now().isoformat(),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
            'origin': request.META.get('HTTP_ORIGIN', 'Unknown'),
        })

    def post(self, request):
        """Test POST endpoint"""
        return Response({
            'message': 'POST request received!',
            'data': request.data,
            'timestamp': timezone.now().isoformat(),
        })


# Reset admin password endpoint
class ResetAdminPasswordView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """Reset admin password to defaultpassword123"""
        try:
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Find admin user
            admin_user = User.objects.filter(username='admin').first()
            if not admin_user:
                return Response({
                    'error': 'Admin user not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Reset password
            admin_user.set_password('defaultpassword123')
            admin_user.save()
            
            return Response({
                'message': 'Admin password reset successfully',
                'username': 'admin',
                'password': 'defaultpassword123'
            })
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Manual data import endpoint (for debugging)
class ImportDataView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """Manually trigger data import"""
        try:
            from django.db import transaction
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Check if candidates exist
            candidate_count = Candidate.objects.count()
            
            if candidate_count > 0:
                return Response({
                    'message': f'Data already exists ({candidate_count} candidates)',
                    'candidate_count': candidate_count
                })
            
            # Import candidates
            candidates_data = [
                {'id': 1, 'name': 'john doe', 'department': 'eng'},
                {'id': 2, 'name': 'jane doe', 'department': 'hr'},
                {'id': 3, 'name': 'alex b', 'department': 'pm'},
                {'id': 4, 'name': 'cow', 'department': 'moo'},
            ]
            
            imported_candidates = 0
            with transaction.atomic():
                for candidate_data in candidates_data:
                    candidate, created = Candidate.objects.get_or_create(
                        id=candidate_data['id'],
                        defaults={
                            'name': candidate_data['name'],
                            'department': candidate_data['department'],
                        }
                    )
                    if created:
                        imported_candidates += 1
                
                # Import users
                users_data = [
                    {
                        'id': 1, 'username': 'Vaahnitha', 'email': 'vaahnithachowdary.ch@gmail.com',
                        'first_name': '', 'last_name': '', 'role': 'employee',
                        'is_staff': True, 'is_active': True,
                    },
                    {
                        'id': 7, 'username': 'employee1', 'email': '',
                        'first_name': '', 'last_name': '', 'role': 'employee',
                        'is_staff': False, 'is_active': True,
                    },
                    {
                        'id': 8, 'username': 'Admin', 'email': 'admin@gmail.com',
                        'first_name': '', 'last_name': '', 'role': 'employee',
                        'is_staff': True, 'is_active': True,
                    },
                    {
                        'id': 9, 'username': 'localadmin', 'email': 'localadmin@example.com',
                        'first_name': '', 'last_name': '', 'role': 'employee',
                        'is_staff': True, 'is_active': True,
                    },
                    {
                        'id': 10, 'username': 'admin', 'email': 'admin@example.com',
                        'first_name': '', 'last_name': '', 'role': 'employee',
                        'is_staff': True, 'is_active': True,
                    },
                ]
                
                imported_users = 0
                for user_data in users_data:
                    if not User.objects.filter(username=user_data['username']).exists():
                        user = User.objects.create_user(
                            username=user_data['username'],
                            email=user_data['email'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            role=user_data['role'],
                            is_staff=user_data['is_staff'],
                            is_active=user_data['is_active'],
                        )
                        user.set_password('defaultpassword123')
                        user.save()
                        imported_users += 1
                
                # Import votes
                votes_data = [
                    {'voter_id': 7, 'candidate_id': 1},  # employee1 -> john doe
                    {'voter_id': 1, 'candidate_id': 1},  # Vaahnitha -> john doe
                    {'voter_id': 9, 'candidate_id': 2},  # localadmin -> jane doe
                ]
                
                imported_votes = 0
                for vote_data in votes_data:
                    try:
                        voter = User.objects.get(id=vote_data['voter_id'])
                        candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                        
                        if not Vote.objects.filter(voter=voter).exists():
                            Vote.objects.create(voter=voter, candidate=candidate)
                            imported_votes += 1
                    except (User.DoesNotExist, Candidate.DoesNotExist):
                        pass
            
            return Response({
                'message': 'Data import completed successfully!',
                'imported_candidates': imported_candidates,
                'imported_users': imported_users,
                'imported_votes': imported_votes
            })
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)