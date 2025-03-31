from django.urls import path
from django.views.decorators.cache import cache_page
from mailing_service.apps import MailingServiceConfig
from .views import AttemptMailingCreateView, AttemptMailingListView
from .views import HomeView
from .views import MailingCreateView, MailingDeleteView, MailingListView, MailingUpdateView
from .views import MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView
from .views import RecipientCreateView, RecipientDeleteView, RecipientListView, RecipientUpdateView


app_name = MailingServiceConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recipient_home/", cache_page(1)(RecipientListView.as_view()), name="recipient_home"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),

    path(
        "recipient_update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient_delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("message_home/", cache_page(10)(MessageListView.as_view()), name="message_home"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_detail/<int:pk>/", cache_page(10)(MessageDetailView.as_view()), name="message_detail"
    ),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailing_home/", cache_page(1)(MailingListView.as_view()), name="mailing_home"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),

    path(
        "mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path(
        "attempt_mailing_home/",
        cache_page(5)(AttemptMailingListView.as_view()),
        name="attempt_mailing_home",
    ),
    path(
        "attempt_mailing_create/",
        AttemptMailingCreateView.as_view(),
        name="attempt_mailing_create",
    ),

]
