# Senet oyunu yerelleştirmesi

game-name-senet = Senet

# Oyun başlangıcı
senet-game-started = { $p1 } birinci oyuncu, { $p2 } ikinci oyuncu. { $first } ilk oynuyor.

# Çubuk atma
senet-throw = { $player } { $result } attı.{ $bonus ->
    [yes] {" "}Bonus atış!
   *[no] {""}
}

# Hareket
senet-move-you = { $from }. kareden { $to }. kareye hareket ettiniz.
senet-move-other = { $player }, { $from }. kareden { $to }. kareye hareket etti.
senet-swap-you = { $to }. karede { $opponent } ile yer değiştirdiniz. { $opponent }, { $from }. kareye geri döndü.
senet-swap-other = { $player }, { $to }. karede { $opponent } ile yer değiştirdi. { $opponent }, { $from }. kareye geri döndü.
senet-bearoff-you = { $from }. kareden taşınızı çıkardınız. { $remaining } taş kaldı.
senet-bearoff-other = { $player }, { $from }. kareden taşını çıkardı. { $remaining } taş kaldı.
senet-water-you = Su Evi'ne düştünüz! Taş { $dest }. kareye gönderildi.
senet-water-other = { $player } Su Evi'ne düştü! Taş { $dest }. kareye gönderildi.
senet-happiness-you = Mutluluk Evi'ne ulaştınız.
senet-happiness-other = { $player } Mutluluk Evi'ne ulaştı.

# Hamle yok
senet-no-moves-you = Geçerli hamleniz yok.
senet-no-moves-other = { $player }'ın geçerli hamlesi yok.

# Kare etiketleri
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, sizin
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, sizin
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Özel kare adları
senet-house-rebirth = Yeniden Doğuş
senet-house-happiness = Mutluluk
senet-house-water = Su
senet-house-three-truths = Üç Gerçek
senet-house-re-atum = Re-Atum

# Durum
senet-status = { $p1 }: { $off1 } çıktı. { $p2 }: { $off2 } çıktı.{ $phase ->
    [throwing] {" "}Atış bekleniyor.
   *[moving] {" "}Zar: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Henüz atış yapılmadı.

# Kazanma
senet-wins = { $player } kazandı! Tüm taşlar çıkarıldı.

# Eylem etiketleri
senet-check-status = Durum
senet-check-sticks = Çubuklar
senet-check-score = Puan
senet-score = { $p1 }: { $off1 } çıktı. { $p2 }: { $off2 } çıktı.

# Hatalar
senet-not-your-piece = Bu sizin taşınız değil.
senet-no-piece-there = Orada taş yok.
senet-no-moves-from-here = Bu kareden geçerli hamle yok.

# Seçenekler
senet-option-bot-difficulty = Bot zorluğu: { $bot_difficulty }
senet-option-select-bot-difficulty = Bot zorluğunu seç
senet-option-changed-bot-difficulty = Bot zorluğu { $bot_difficulty } olarak ayarlandı.
senet-difficulty-random = Rastgele
senet-difficulty-simple = Basit
