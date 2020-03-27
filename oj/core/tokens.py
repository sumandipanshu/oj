from django.contrib.auth.tokens import PasswordResetTokenGenerator
from binascii import hexlify
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            "somestring"
                )


account_activation_token = AccountActivationTokenGenerator()
