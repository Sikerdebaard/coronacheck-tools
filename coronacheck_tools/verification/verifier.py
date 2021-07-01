from coronacheck_tools.verification.mobilecore import validate as mobilecore_validate

# there's only one strategy at the moment
# mobilecore: a thin wrapper around the mobilecore validator from the coronacheck.nl app
strategies = ('mobilecore')


def validate_raw(raw: str, strategy='mobilecore', *args, **kwargs):
    """
    Validate the RAW data from the QR Code.

    :param raw: RAW data as a str
    :param strategy: the validator strategy, available: mobilecore default: mobilecore
    :param args: extra strategy specific parameters (if any)
    :param kwargs: extra strategy specific parameters (if any)
    :return: tuple: valid True/False, extra info
    """

    if strategy.lower() not in strategies:
        raise ValueError(f'Invalid strategy choose one of: {", ".join(strategies)}')

    if strategy == 'mobilecore':
        return mobilecore_validate(raw, *args, **kwargs)

