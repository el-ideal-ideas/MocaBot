# -- Imports --------------------------------------------------------------------------

from twilio.rest import Client
from twilio.base.exceptions import TwilioException

# -------------------------------------------------------------------------- Imports --

# -- MocaTwilio --------------------------------------------------------------------------


class MocaTwilioSMS:
    """
    send SMS message.

    Attributes
    ----------
    _account_sid: str
        Your Account Sid from twilio.com/console
    _auth_token
        Your Auth Token from twilio.com/console
    _number: str
        Your phone number.
    _client: Client
        the client instance of twilio.
    """

    def __init__(self, account_sid: str, auth_token: str, self_number: str):
        """
        :param account_sid: # Your Account Sid from twilio.com/console
        :param auth_token: # Your Auth Token from twilio.com/console
        :param self_number: # Your phone number.
        """
        self._account_sid: str = account_sid
        self._auth_token: str = auth_token
        self._number: str = self_number
        self._client: Client = Client(account_sid, auth_token)

    @property
    def client(self) -> Client:
        return self._client

    def send_sms(self, message: str, to: str) -> bool:
        try:
            self._client.messages.create(body=message, to=to, from_=self._number)
            return True
        except TwilioException:
            return False

# -------------------------------------------------------------------------- MocaTwilio --
