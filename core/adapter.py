from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoNewUsersAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True  # Allow automatic signup

    def pre_social_login(self, request, sociallogin):
        # Skip confirmation page
        pass
