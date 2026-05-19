# सेनेत खेल का स्थानीयकरण

game-name-senet = सेनेत

# खेल की शुरुआत
senet-game-started = { $p1 } खिलाड़ी एक हैं, { $p2 } खिलाड़ी दो हैं। { $first } पहले खेलेंगे।

# लकड़ियाँ फेंकना
senet-throw = { $player } ने { $result } फेंका।{ $bonus ->
    [yes] {" "}बोनस थ्रो!
   *[no] {""}
}

# चाल
senet-move-you = आप घर { $from } से घर { $to } पर गए।
senet-move-other = { $player } घर { $from } से घर { $to } पर गए।
senet-swap-you = आपने घर { $to } पर { $opponent } से जगह बदली। { $opponent } घर { $from } पर वापस गए।
senet-swap-other = { $player } ने घर { $to } पर { $opponent } से जगह बदली। { $opponent } घर { $from } पर वापस गए।
senet-bearoff-you = आपने घर { $from } से गोटी बाहर निकाली। { $remaining } गोटियाँ बची हैं।
senet-bearoff-other = { $player } ने घर { $from } से गोटी बाहर निकाली। { $remaining } गोटियाँ बची हैं।
senet-water-you = आप जल-गृह में पहुँचे! गोटी घर { $dest } पर भेजी गई।
senet-water-other = { $player } जल-गृह में पहुँचे! गोटी घर { $dest } पर भेजी गई।
senet-happiness-you = आप सुख-गृह पर पहुँचे।
senet-happiness-other = { $player } सुख-गृह पर पहुँचे।

# कोई चाल नहीं
senet-no-moves-you = आपके पास कोई वैध चाल नहीं है।
senet-no-moves-other = { $player } के पास कोई वैध चाल नहीं है।

# घर के लेबल
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, आपकी
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, आपकी
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# विशेष घरों के नाम
senet-house-rebirth = पुनर्जन्म
senet-house-happiness = सुख
senet-house-water = जल
senet-house-three-truths = तीन सत्य
senet-house-re-atum = रे-आतुम

# स्थिति
senet-status = { $p1 }: { $off1 } बाहर। { $p2 }: { $off2 } बाहर।{ $phase ->
    [throwing] {" "}फेंकने की प्रतीक्षा।
   *[moving] {" "}पासा: { $roll }।
}
senet-sticks = { $result }
senet-sticks-none = अभी तक फेंक नहीं हुई।

# जीत
senet-wins = { $player } जीते! सभी गोटियाँ बाहर हो गईं।

# क्रिया लेबल
senet-check-status = स्थिति
senet-check-sticks = लकड़ियाँ
senet-check-score = स्कोर
senet-score = { $p1 }: { $off1 } बाहर। { $p2 }: { $off2 } बाहर।

# त्रुटियाँ
senet-not-your-piece = यह आपकी गोटी नहीं है।
senet-no-piece-there = वहाँ कोई गोटी नहीं है।
senet-no-moves-from-here = इस घर से कोई वैध चाल नहीं है।

# विकल्प
senet-option-bot-difficulty = बॉट कठिनाई: { $bot_difficulty }
senet-option-select-bot-difficulty = बॉट कठिनाई चुनें
senet-option-changed-bot-difficulty = बॉट कठिनाई { $bot_difficulty } पर सेट की गई।
senet-difficulty-random = यादृच्छिक
senet-difficulty-simple = सरल
