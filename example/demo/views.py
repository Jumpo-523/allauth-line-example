# import the logging library
import logging, os
# Get an instance of a logger
logger = logging.getLogger(__name__)

# from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
# Create your views here.
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.http.response import JsonResponse

def get_social_account_user(request):
    try:
        social_account = SocialAccount.objects.get(user=request.user)
        return social_account
    except SocialAccount.DoesNotExist:
        return None

# For Handling DoesNotExist Error.
# from allauth.socialaccount.models.SocialAccount import DoesNotExist
class ProfileFormView(TemplateView):
    form_class = None
    social_account = None
    template_name = "profile.html"
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        # import pdb; pdb.set_trace()
        self.social_account = get_social_account_user(request)
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["social_account"] = self.social_account
        return context

profile = ProfileFormView.as_view() 


def notify_by_message_api(request):
    user = get_social_account_user(request)
    if user is None:
        return JsonResponse({"error": "You don't have social account."}, status=400)
    # TODO: develop push notifications using user_id.
    # https://developers.line.biz/ja/reference/messaging-api/#send-push-message
    from linebot import LineBotApi
    from linebot.models import TextSendMessage
    from linebot.exceptions import LineBotApiError
    import pdb; pdb.set_trace()
    try:
        line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
        line_bot_api.push_message(f'{user.uid}', TextSendMessage(text='初めまして、webサイトへの登録ありがとうございます。'))
    except (LineBotApiError, KeyError) as e:
        # error handle
        logger.error(f'Something went wrong! {e}')
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    # social_account.uid
    # messageだけclientに返したい。
    # ajaxの使い方を復習する。
    return JsonResponse({"success": True, 'message':"I correctly sent messages"})


    