"""Test auto-contenu de ProviderCoinalyze (sans dependance au vrai access.json).

Construit le provider directement et verifie : expose la cle, ne la fuite pas
(repr/str), validite permanente si duration<=0.
"""
from AccessMgr._modCoinalyze import ProviderCoinalyze, AccessEnvironment


def _provider(api_key: str = "SECRET_COINALYZE_123", duration: int = 0) -> dict:
    return {
        "id": "test",
        "type": "provider",
        "duration": duration,
        "name": "CoinalyzeTest",
        "user_id": "user@example.com",
        "api_key": api_key,
    }


def test_coinalyze_expose_la_cle() -> None:
    p = ProviderCoinalyze(provider=_provider(), an_environment=AccessEnvironment.PROD,
                          st_sub_name="prod")
    assert p.type == "provider"
    assert p.user_id == "user@example.com"
    assert p.api_key() == "SECRET_COINALYZE_123"


def test_coinalyze_ne_fuite_pas_le_secret() -> None:
    p = ProviderCoinalyze(provider=_provider(api_key="TOP_SECRET_XYZ"),
                          an_environment=AccessEnvironment.PROD, st_sub_name="prod")
    assert "TOP_SECRET_XYZ" not in repr(p)
    assert "TOP_SECRET_XYZ" not in str(p)


def test_coinalyze_validite_permanente_si_duration_nulle() -> None:
    p = ProviderCoinalyze(provider=_provider(duration=0), an_environment=AccessEnvironment.PROD,
                          st_sub_name="prod")
    assert p.is_alive() is True
    assert p.validity_end is None
