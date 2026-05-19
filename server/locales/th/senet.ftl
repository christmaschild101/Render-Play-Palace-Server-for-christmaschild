# การแปลเกม Senet

game-name-senet = เซเนต

# เริ่มเกม
senet-game-started = { $p1 } คือผู้เล่นที่ 1, { $p2 } คือผู้เล่นที่ 2 { $first } เริ่มก่อน

# การทอยไม้
senet-throw = { $player } ทอยได้ { $result }{ $bonus ->
    [yes] {" "}ทอยโบนัส!
   *[no] {""}
}

# การเคลื่อนที่
senet-move-you = คุณเคลื่อนจากช่อง { $from } ไปช่อง { $to }
senet-move-other = { $player } เคลื่อนจากช่อง { $from } ไปช่อง { $to }
senet-swap-you = คุณสลับที่กับ { $opponent } ที่ช่อง { $to } { $opponent } ถอยกลับไปช่อง { $from }
senet-swap-other = { $player } สลับที่กับ { $opponent } ที่ช่อง { $to } { $opponent } ถอยกลับไปช่อง { $from }
senet-bearoff-you = คุณนำตัวหมากออกจากช่อง { $from } เหลืออีก { $remaining } ตัว
senet-bearoff-other = { $player } นำตัวหมากออกจากช่อง { $from } เหลืออีก { $remaining } ตัว
senet-water-you = คุณตกลงในบ้านแห่งน้ำ! หมากถูกส่งไปช่อง { $dest }
senet-water-other = { $player } ตกลงในบ้านแห่งน้ำ! หมากถูกส่งไปช่อง { $dest }
senet-happiness-you = คุณมาถึงบ้านแห่งความสุขแล้ว
senet-happiness-other = { $player } มาถึงบ้านแห่งความสุขแล้ว

# ไม่มีการเคลื่อนที่
senet-no-moves-you = คุณไม่มีการเคลื่อนที่ที่ถูกกฎ
senet-no-moves-other = { $player } ไม่มีการเคลื่อนที่ที่ถูกกฎ

# ป้ายช่อง
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, หมากของคุณ
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, หมากของคุณ
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# ชื่อช่องพิเศษ
senet-house-rebirth = บ้านแห่งการเกิดใหม่
senet-house-happiness = บ้านแห่งความสุข
senet-house-water = บ้านแห่งน้ำ
senet-house-three-truths = บ้านแห่งสามความจริง
senet-house-re-atum = บ้านเร-อาตุม

# สถานะ
senet-status = { $p1 }: นำออก { $off1 } ตัว { $p2 }: นำออก { $off2 } ตัว{ $phase ->
    [throwing] {" "}รอการทอย
   *[moving] {" "}ผลทอย: { $roll }
}
senet-sticks = { $result }
senet-sticks-none = ยังไม่ได้ทอย

# ชนะ
senet-wins = { $player } ชนะ! นำหมากออกครบทุกตัวแล้ว

# ป้ายการกระทำ
senet-check-status = สถานะ
senet-check-sticks = ผลการทอย
senet-check-score = คะแนน
senet-score = { $p1 }: { $off1 } ตัว { $p2 }: { $off2 } ตัว

# ข้อผิดพลาด
senet-not-your-piece = นี่ไม่ใช่หมากของคุณ
senet-no-piece-there = ไม่มีหมากในช่องนี้
senet-no-moves-from-here = ไม่มีการเคลื่อนที่ที่ถูกกฎจากช่องนี้

# ตัวเลือก
senet-option-bot-difficulty = ความยากของบอต: { $bot_difficulty }
senet-option-select-bot-difficulty = เลือกความยากของบอต
senet-option-changed-bot-difficulty = ตั้งค่าความยากของบอตเป็น { $bot_difficulty } แล้ว
senet-difficulty-random = สุ่ม
senet-difficulty-simple = ง่าย
