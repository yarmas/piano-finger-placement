def test_imports():
    import piano_fingering
    from piano_fingering.cli.main import _profile_from_name
    assert _profile_from_name("M").name == "M"
