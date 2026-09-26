from coursepilot.config import Settings


def test_generic_llm_environment_variable_names(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_BASE_URL", "https://llm.example.test/v1")
    monkeypatch.setenv("LLM_MODEL", "example-model")

    settings = Settings()

    assert settings.llm_api_key == "test-key"
    assert settings.llm_base_url == "https://llm.example.test/v1"
    assert settings.llm_model == "example-model"


def test_openai_environment_variable_names_remain_supported(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "legacy-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://legacy.example.test/v1")
    monkeypatch.setenv("OPENAI_MODEL", "legacy-model")

    settings = Settings()

    assert settings.llm_api_key == "legacy-key"
    assert settings.llm_base_url == "https://legacy.example.test/v1"
    assert settings.llm_model == "legacy-model"


def test_euv_file_is_loaded_and_overrides_env_file(tmp_path, monkeypatch):
    for name in (
        "LLM_API_KEY",
        "LLM_BASE_URL",
        "LLM_MODEL",
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / ".env").write_text("LLM_MODEL=old-model\n", encoding="utf-8")
    (tmp_path / ".euv").write_text(
        "LLM_API_KEY=euv-key\n"
        "LLM_BASE_URL=https://euv.example.test/v1\n"
        "LLM_MODEL=euv-model\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    settings = Settings()

    assert settings.llm_api_key == "euv-key"
    assert settings.llm_base_url == "https://euv.example.test/v1"
    assert settings.llm_model == "euv-model"
