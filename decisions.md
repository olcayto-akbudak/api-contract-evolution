# Tasarım kararları

## Alan motorunu CLI'dan ayırmak

`run(config)` orkestrasyonu kaynak kodun doğrudan test edilebilmesini sağlar. JSON arayüz taşınabilirliği artırır; bu sürüm kullanıcı arayüzü barındırmaz.

## Seçilen yöntem

İstek/yanıt uyumluluğu, değişiklik kapısı. JSON Schema alt kümesi desteklenir; bilinmeyen anahtarlar manuel incelemeye yönlendirilir.

## Bilinçli sınır

Tam OpenAPI çözümleyicisi değildir; $ref, oneOf ve tüm validator semantiği ayrıca gerekir.

## Önerilen sonraki doğrulama

Gerçek kullanım hacmiyle testten önce mevcut kabul ve ret örneklerinin alan uzmanı tarafından onaylanması gerekir. Sonraki sürüm performans ölçümleri, dış adaptör sözleşmesi ve üretim gözlemlenebilirliğini ayrı karar kayıtlarında ele almalıdır.
