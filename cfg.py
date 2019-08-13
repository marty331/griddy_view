from decouple import UndefinedValueError, AutoConfig, config

class AutoConfigPlus(AutoConfig):  # pylint: disable=too-many-public-methods
    """
    thin wrapper around AutoConfig adding some extra features
    """

    @property
    def REPO_ROOT(self):
        """
        repo_root
        """
        return git("rev-parse --show-toplevel")

    @property
    def SETTLEMENT_POINT(self):
        """
        settlement_point
        """
        return self('SETTLEMENT_POINT', "LZ_SOMEWHERE")

    @property
    def METERID(self):
        """
        METERID
        """
        return self('METERID', '000000')

    @property
    def COST_PERIOD(self):
        """
        COST_PERIOD
        """
        return self('COST_PERIOD', '2019-08-01')

    @property
    def COST_INTERVAL(self):
        """
        COST_INTERVAL
        """
        return self('COST_INTERVAL', 'monthly')

    @property
    def ALERT_STATE_VALUE(self):
        """
        ALERT_STATE_VALUE
        """
        return self('ALERT_STATE_VALUE', 0.0)

    @property
    def ACCOUNT_SID(self):
        """
        ACCOUNT_SID
        """
        return self('ACCOUNT_SID', 'fake_account_sid')

    @property
    def AUTH_TOKEN(self):
        """
        AUTH_TOKEN
        """
        return self('AUTH_TOKEN', 'fake_auth_token')

    @property
    def FROM_NUMBER(self):
        """
        FROM_NUMBER
        """
        return self('FROM_NUMBER', '8005551212')

    @property
    def TO_NUMBERS(self):
        """
        TO_NUMBERS
        """
        return self('TO_NUMBERS', '18005551212,18885551212').split(",")

CFG = AutoConfigPlus()
