from django.urls import path
from .views import CandidateListView, VoteCreateView, ResultsView, ImportDataView, ResetAdminPasswordView, TestView

urlpatterns = [
    path('candidates/', CandidateListView.as_view(), name='candidates-list'),
    path('vote/', VoteCreateView.as_view(), name='vote'),
    path('results/', ResultsView.as_view(), name='results'),
    path('import-data/', ImportDataView.as_view(), name='import-data'),
    path('reset-admin-password/', ResetAdminPasswordView.as_view(), name='reset-admin-password'),
    path('test/', TestView.as_view(), name='test'),
]
