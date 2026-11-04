"""Optional third-party G2P adapters.

Adapters are deliberately lazy: importing this package never imports an
optional engine or downloads model/data files.
"""

__all__ = ["FastThaiG2PAdapter", "FastThaiG2PUnavailable"]


def __getattr__(name):
    if name in __all__:
        from .fastthaig2p import FastThaiG2PAdapter, FastThaiG2PUnavailable
        return {
            "FastThaiG2PAdapter": FastThaiG2PAdapter,
            "FastThaiG2PUnavailable": FastThaiG2PUnavailable,
        }[name]
    raise AttributeError(name)
