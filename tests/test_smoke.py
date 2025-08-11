def test_imports():
    import piano-fingering-placement
    from piano-fingering-placement.cli.main import _profile_from_name
    assert _profile_from_name("M").name == "M"
