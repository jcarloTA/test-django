from django.urls import path
from .views import LicenseList, LisenceTrigger, ClientList, EmailsLogsList

urlpatterns = [
    path('licenses/', LicenseList.as_view(), name='lista-lisences'),
    path('licenses-trigger/', LisenceTrigger.as_view(), name='trigger-trigger'),
    path('clients/', ClientList.as_view(), name='lista-clients'),
    path('recent_emails/<int:num_emails>/', EmailsLogsList.as_view(), name='recent_emails'),

]