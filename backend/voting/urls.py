from django.urls import path
from .views import CandidateListView, VoteCreateView, ResultsView, ImportDataView

urlpatterns = [
    path('candidates/', CandidateListView.as_view(), name='candidates-list'),
    path('vote/', VoteCreateView.as_view(), name='vote'),
    path('results/', ResultsView.as_view(), name='results'),
    path('import-data/', ImportDataView.as_view(), name='import-data'),
]
