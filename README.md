# trendyol-pazaryeri-sticker-generator
Trendyol Pazaryeri siparişleri için sticker oluşturmaya yarar. <br>

<h2>📄 İçerik</h2>
<b>barcodes:</b> <br>
<i>Barkodların oluşturulup kullanıldıktan sonra temizlendiği klasör.</i> <br><br>

<b>stickers:</b> <br>
<i>Oluşturulan barkodlar bu klasörde yer alacak.</i>

<b>createSticker.py:</b> <br>
<i>İçinde "generateBarcodes(cargoTrackingNumber)" fonksiyonunu da bulunduran, sticker oluşturmaya yarayan script dosyası.</i>

<b>response.log:</b> <br>
<i>Fonksiyonların verebileceği olası hataların kaydedileceği log dosyası.</i>

<b>tr-arial.ttf:</b> <br>
<i>Sticker'da kullanılacak font.</i> <br>
https://copyfonts.com/fonts/tr-arial.html

<h2>🤖 Kullanım</h2>
"createStickers.py" dosyasında kullanılan tüm kütüphanelerin sisteminizde bulunduğundan emin olun. <br>
Trendyol API ile çekilen siparişleri "createSticker(order)" fonksiyonunda çağırarak (order) işleme alın. <br>
Oluşturulan sticker'ı <b>stickers</b> klasörü içinde bulabilirsiniz.
