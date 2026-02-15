from wheke import Wheke, WhekeSettings

from wheke_ladybug import ladybug_pod

from .pod import social_pod


def build_wheke(settings: WhekeSettings) -> Wheke:
    wheke = Wheke(settings)

    wheke.add_pod(ladybug_pod)
    wheke.add_pod(social_pod)

    return wheke
