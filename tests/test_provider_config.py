import json

from utils.config import AccountConfig, AppConfig, ProviderConfig


def test_builtin_provider_profile_persistence_defaults(monkeypatch):
	monkeypatch.delenv('PROVIDERS', raising=False)

	config = AppConfig.load_from_env()

	assert config.providers['anyrouter'].persist_profile is True
	assert config.providers['agentrouter'].persist_profile is False


def test_provider_profile_persistence_can_override_builtin(monkeypatch):
	monkeypatch.setenv(
		'PROVIDERS',
		json.dumps(
			{
				'anyrouter': {'domain': 'https://anyrouter.top', 'persist_profile': False},
				'agentrouter': {'domain': 'https://agentrouter.org', 'persist_profile': True},
			}
		),
	)

	config = AppConfig.load_from_env()

	assert config.providers['anyrouter'].persist_profile is False
	assert config.providers['agentrouter'].persist_profile is True


def test_custom_provider_profile_persistence_defaults_to_false(monkeypatch):
	monkeypatch.setenv('PROVIDERS', json.dumps({'custom': {'domain': 'https://custom.example.com'}}))

	config = AppConfig.load_from_env()

	assert config.providers['custom'].persist_profile is False


def test_provider_from_dict_inherits_profile_persistence_from_defaults():
	defaults = ProviderConfig(name='custom', domain='https://old.example.com', persist_profile=True)

	provider = ProviderConfig.from_dict(
		'custom',
		{'domain': 'https://new.example.com'},
		defaults=defaults,
	)

	assert provider.persist_profile is True


def test_legacy_custom_provider_default_checkin_path_is_unchanged():
	provider = ProviderConfig.from_dict('custom', {'domain': 'https://custom.example.com'})

	assert provider.sign_in_path == '/api/user/sign_in'


def test_known_newapi_providers_are_builtin(monkeypatch):
	monkeypatch.delenv('PROVIDERS', raising=False)
	monkeypatch.delenv('ANYROUTER_ACCOUNTS', raising=False)

	config = AppConfig.load_from_env()

	assert config.providers['gorouter'].domain == 'https://gorouter.app'
	assert config.providers['tabitoken'].domain == 'https://tabitoken.com'
	assert config.providers['docode'].domain == 'https://docode.cc'
	assert config.providers['jianzhile'].domain == 'https://jianzhile.vip'
	assert config.providers['shawn'].domain == 'https://api.supxh.xin'
	assert config.providers['api456'].domain == 'https://api456.me'
	assert config.providers['jun'].domain == 'https://muyuan.do'
	assert config.providers['jun'].login_path == '/auth/login'
	assert config.providers['gorouter'].sign_in_path == '/api/user/checkin'


def test_account_with_domain_gets_direct_newapi_provider_name():
	account = AccountConfig.from_dict(
		{
			'domain': 'https://example.com',
			'email': 'a@example.com',
			'password': 'secret',
		},
		0,
	)

	assert account.provider == 'newapi_1'
	assert account.domain == 'https://example.com'


def test_domain_account_creates_standard_newapi_provider(monkeypatch):
	monkeypatch.delenv('PROVIDERS', raising=False)
	monkeypatch.setenv(
		'ANYROUTER_ACCOUNTS',
		json.dumps(
			[
				{
					'domain': 'https://example.com',
					'email': 'a@example.com',
					'password': 'secret',
				}
			]
		),
	)

	config = AppConfig.load_from_env()

	assert config.providers['newapi_1'].domain == 'https://example.com'
	assert config.providers['newapi_1'].sign_in_path == '/api/user/checkin'
