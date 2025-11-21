"""
Vista de debugging para el callback de GitHub
"""
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView

class DebugGitHubOAuth2CallbackView(OAuth2CallbackView):
    """Vista de callback con debugging"""
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

oauth2_login = OAuth2LoginView.adapter_view(GitHubOAuth2Adapter)
oauth2_callback = DebugGitHubOAuth2CallbackView.adapter_view(GitHubOAuth2Adapter)
