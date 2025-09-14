from django.urls import path
from .views import CandidateListView, VoteCreateView, ResultsView

urlpatterns = [
    path('candidates/', CandidateListView.as_view(), name='candidates-list'),
    path('vote/', VoteCreateView.as_view(), name='vote'),
    path('results/', ResultsView.as_view(), name='results'),
]
