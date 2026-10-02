# Çalıştırılmış kabul sonuçları

Python 3.12.14, sentetik `scenario.json`; yerel test sayısı **8**, tümü başarılı. Ham test günlüğü `test-log.txt`.

createInvoice: BLOCK, 2 kırıcı değişiklik; status: BLOCK, 1 kırıcı değişiklik

Sonuçlar yalnız bu örneğe aittir; üretim doğruluğu veya performans garantisi olarak yorumlanmamalıdır. Ölçülen iş sonucunu kontrol edin; örnek negatif vaka içeriyorsa ret beklenir. Tam çıktı `sample-report.json`.

## Sınanan davranışlar

| Test | Kontrol |
|---|---|
| `test_same` | same |
| `test_request_narrow` | request narrow |
| `test_response_expand` | response expand |
| `test_response_unbounded` | response unbounded |
| `test_unknown_review` | unknown review |
| `test_direction` | direction |
| `test_nested_array` | nested array |
| `test_request_enum_expansion` | request enum expansion |

## Gelişmiş deney planı

1. $ref çözümlemesini çevrim ve uzaktan dosya korumasıyla ekleyin.
2. Nullable alanların istek/yanıt yönlü uyumluluğunu formel kurallarla tanımlayın.
3. oneOf alternatiflerini yalnız anlamını doğrulayabildiğiniz durumda otomatik sınıflayın.
4. Gerçek OpenAPI sürüm çiftlerinden insan onaylı uyumluluk veri seti çıkarın.
