import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from .models import (
    NewsLetter
)
from .serializers import (
    NewsLetterListSerializer,
    NewsLetterSubscriberSerializer
)

logger = logging.getLogger("newsletter_app")


class NewsLetterViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterListSerializer

    def get_serializer_class(self):
        if self.action == "sign_to_newsletter":
            return NewsLetterSubscriberSerializer
        return NewsLetterListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # get from cookies date when user have subscribed to newsletter
        news_subscribed_email = self.request.COOKIES.get(
            settings.COOKIE_NEWS_SUBSCRIBED_EMAIL, None
        )
        context[settings.COOKIE_NEWS_SUBSCRIBED_EMAIL] = news_subscribed_email

        return context

    @method_decorator(cache_page(60 * 60))  # cache for 1 hour
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=["POST"], url_path="sign", detail=False, url_name="sign")
    def sign_to_newsletter(self, request: Request):
        """
        Sign users to newsletter email notification at the end of week
        relative from the day user has signed.
        :param request:
        :return:
        """
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # since we are not using any authentication system
        # we are going to use cookies to store when user subscribed email.
        response = Response(status=status.HTTP_201_CREATED)

        response.set_cookie(
            settings.COOKIE_NEWS_SUBSCRIBED_EMAIL,  # cookie name
            serializer.validated_data["email"],
            httponly=True
        )

        return response
