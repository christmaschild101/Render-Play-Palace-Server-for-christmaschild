# Lokalisasi Senet

game-name-senet = Senet

# Mulai permainan
senet-game-started = { $p1 } adalah pemain 1, { $p2 } adalah pemain 2. { $first } jalan lebih dulu.

# Lempar tongkat
senet-throw = { $player } melempar { $result }.{ $bonus ->
    [yes] {" "}Lemparan bonus!
   *[no] {""}
}

# Pergerakan
senet-move-you = Anda bergerak dari kotak { $from } ke kotak { $to }.
senet-move-other = { $player } bergerak dari kotak { $from } ke kotak { $to }.
senet-swap-you = Anda bertukar dengan { $opponent } di kotak { $to }. { $opponent } kembali ke kotak { $from }.
senet-swap-other = { $player } bertukar dengan { $opponent } di kotak { $to }. { $opponent } kembali ke kotak { $from }.
senet-bearoff-you = Anda melepas bidak dari kotak { $from }. Tersisa { $remaining }.
senet-bearoff-other = { $player } melepas bidak dari kotak { $from }. Tersisa { $remaining }.
senet-water-you = Anda mendarat di Rumah Air! Bidak dikirim ke kotak { $dest }.
senet-water-other = { $player } mendarat di Rumah Air! Bidak dikirim ke kotak { $dest }.
senet-happiness-you = Anda mencapai Rumah Kebahagiaan.
senet-happiness-other = { $player } mencapai Rumah Kebahagiaan.

# Tidak ada langkah
senet-no-moves-you = Anda tidak memiliki langkah yang sah.
senet-no-moves-other = { $player } tidak memiliki langkah yang sah.

# Label kotak
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, milik Anda
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, milik Anda
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nama kotak khusus
senet-house-rebirth = Kelahiran Kembali
senet-house-happiness = Kebahagiaan
senet-house-water = Air
senet-house-three-truths = Tiga Kebenaran
senet-house-re-atum = Re-Atum

# Status
senet-status = { $p1 }: { $off1 } keluar. { $p2 }: { $off2 } keluar.{ $phase ->
    [throwing] {" "}Menunggu lemparan.
   *[moving] {" "}Hasil lempar: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Belum melempar.

# Menang
senet-wins = { $player } menang! Semua bidak telah dilepas.

# Label aksi
senet-check-status = Status
senet-check-sticks = Tongkat
senet-check-score = Skor
senet-score = { $p1 }: { $off1 } keluar. { $p2 }: { $off2 } keluar.

# Kesalahan
senet-not-your-piece = Itu bukan bidak Anda.
senet-no-piece-there = Tidak ada bidak di kotak ini.
senet-no-moves-from-here = Tidak ada langkah sah dari kotak ini.

# Opsi
senet-option-bot-difficulty = Tingkat kesulitan bot: { $bot_difficulty }
senet-option-select-bot-difficulty = Pilih tingkat kesulitan bot
senet-option-changed-bot-difficulty = Tingkat kesulitan bot diatur ke { $bot_difficulty }.
senet-difficulty-random = Acak
senet-difficulty-simple = Sederhana
