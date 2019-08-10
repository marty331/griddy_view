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

CFG = AutoConfigPlus()
