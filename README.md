# LogLens

[![CI](https://github.com/yeldaayd/loglens/actions/workflows/ci.yml/badge.svg)](https://github.com/yeldaayd/loglens/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

SSH ve web sunucusu loglarından saldırı belirtilerini tespit eden, hafif ve savunma amaçlı (blue team) bir log analiz aracı. Yalnızca Python standart kütüphanesini kullanır, ek paket gerektirmez. Her bulgu bir MITRE ATT&CK tekniğiyle eşleştirilir.

## Özellikler

- sshd (`auth.log`) ve nginx/Apache (combined format) loglarını okur
- 6 tespit kuralı, her biri MITRE ATT&CK tekniğine bağlı
- Önem derecesine göre sıralı konsol raporu ve JSON çıktısı
- Güvenilir IP'ler için allowlist (`--allow`)
- Bulgu olduğunda çıkış kodu `1`: CI veya cron akışına bağlanabilir
- Sıfır bağımlılık, 13 birim test, GitHub Actions ile otomatik test

## Tespit kuralları

| Kural | Ne yakalar | MITRE ATT&CK | Önem |
| --- | --- | --- | --- |
| `ssh_brute_force` | 5 dk içinde tek IP'den çok sayıda başarısız SSH girişi | T1110.001 | medium / high |
| `ssh_password_spraying` | Tek IP'den çok sayıda farklı kullanıcı adı denemesi | T1110.003 | high |
| `ssh_success_after_failures` | Çok sayıda başarısız denemeden sonra aynı IP'den başarılı giriş (olası hesap ele geçirme) | T1078 | critical |
| `web_scanning` | Kısa sürede çok sayıda 403/404 yanıtı (otomatik tarama) | T1595.002 | medium |
| `web_sensitive_path_probe` | `/.env`, `/.git`, `/phpmyadmin` gibi hassas yolların aranması | T1595.003 | high |
| `web_attack_payload` | URL'de SQL injection, XSS ve path traversal kalıpları | T1190 | high |

## Kurulum ve kullanım

```bash
git clone https://github.com/yeldaayd/loglens.git
cd loglens

# Repodaki örnek loglar üzerinde çalıştır
python3 -m loglens --auth samples/sample_auth.log --access samples/sample_access.log --year 2026

# Kendi loglarında, güvenilir IP'leri hariç tutarak, JSON rapor ile
python3 -m loglens --auth /var/log/auth.log --allow 192.168.1.10 --year 2026 --json rapor.json

# Eşiği değiştir
python3 -m loglens --auth auth.log --year 2026 --brute-threshold 20
```

Syslog satırlarında yıl bulunmadığı için `--year` ile verilir.

### Örnek çıktı (sentetik veri)

```
9 bulgu tespit edildi

[CRITICAL] ssh_success_after_failures  ip=203.0.113.99  adet=15
           2026-11-17 14:40:00 -> 2026-11-17 14:42:10  |  T1078 Valid Accounts
           15 basarisiz denemeden sonra 'deploy' hesabiyla basarili giris: hesap ele gecirilmis olabilir

[HIGH    ] ssh_brute_force  ip=203.0.113.45  adet=60
           2026-11-17 03:12:00 -> 2026-11-17 03:14:57  |  T1110.001 Password Guessing
           5 dk icinde 60 basarisiz SSH girisi. Hedef hesaplar: admin, root, ubuntu
```

Tam çıktı için [`samples/sample_report.json`](samples/sample_report.json) dosyasına bak.

## Testler

```bash
python3 -m unittest discover -s tests -t . -v
```

## Örnek veri üretimi

`samples/` içindeki loglar sentetiktir; gerçek kişi veya sistem verisi içermez ve yalnızca RFC 5737 belge amaçlı IP bloklarını kullanır. Dört saldırı senaryosu bilerek gömülüdür. Yeniden üretmek için:

```bash
python3 scripts/generate_sample_logs.py
```

## Proje yapısı

```
loglens/
├── loglens/
│   ├── core.py        # ayrıştırıcılar, tespit kuralları, CLI
│   ├── __init__.py
│   └── __main__.py    # python -m loglens
├── tests/test_loglens.py
├── scripts/generate_sample_logs.py
├── samples/           # sentetik loglar ve örnek rapor
└── .github/workflows/ci.yml
```

## Sınırlamalar

- Kural tabanlıdır; makine öğrenmesi veya davranışsal profil kullanmaz.
- Yalnızca IPv4 ayrıştırır.
- Bilinen kalıplara bakar; çift kodlanmış (double-encoded) payload'ları kaçırabilir.
- Gerçek ortamda önce `--allow` ile kendi altyapı IP'lerini hariç tutmak yanlış pozitifleri azaltır.

## Yol haritası

- [ ] IPv6 desteği
- [ ] GeoIP zenginleştirme
- [ ] Windows Event Log (4625/4624) ayrıştırıcısı
- [ ] Flask tabanlı bulgu paneli
- [ ] E-posta / webhook uyarıları

## Lisans

[MIT](LICENSE)
