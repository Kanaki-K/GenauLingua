"""Вычитка чешского, порция p015 (B1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    6828: (T + "«Šílený,» — род", {"example_cs": "Šílené, viděl jsi to?"}),
    6842: (T + "«uklízíme» — не тот вид", {"example_cs": "Před návštěvou důkladně uklidíme celý byt"}),
    6844: (T + "«děkuji za tvou pomoc» — тяжело", {"example_cs": "Mockrát díky za pomoc"}),
    6847: (T + "«velmi» — книжно", {"example_cs": "Ta židle je hodně stabilní"}),
    6850: (T + "«příliš» — книжно", {"example_cs": "To je na mě moc riskantní"}),
    6873: (T + "«obývacího pokoje» — книжно", {"example_cs": "Pojď prosím dolů do obýváku!"}),
    6880: (T + "«provádějí» — не тот вид", {"example_cs": "Zítra ve škole provedou cvičný poplach"}),
    6882: (T + "dazwischen — «между», не «mezitím»", {"example_cs": "Mezi tím mám ještě trochu času"}),
    6902: (T + "«Tento … velmi» — книжно", {"example_cs": "Tenhle prsten je pro mě hodně cenný"}),
    6914: (T + "«svou» — лишнее", {"example_cs": "Pes zahrabává kost na zahradě"}),
    6942: (T + "«Rozestavujeme» — не тот вид", {"example_cs": "Rozestavíme stoly na oslavu"}),
    6956: (T + "«Tento druh» — книжно", {"example_cs": "Tenhle druh zvířat je vážně ohrožený"}),
    6994: (T + "«na mém laně» — калька", {"example_cs": "Uzel na laně je moc utažený"}),
    7003: (T + "«Tyto» — книжно", {"example_cs": "Tyhle boty nejsou vhodné na hory"}),
    7012: (T + "«krátce» — калька", {"example_cs": "Chci se jen trochu porozhlédnout"}),
    7028: (T + "«krátili» — не тот вид", {"example_cs": "Hrajeme karty, abychom si ukrátili čas"}),
    7033: (T + "«Tento» — книжно", {"example_cs": "Tenhle týden jsem byl několikrát v posilovně"}),
    7049: (T + "«Tato … velmi» — книжно", {"example_cs": "Tahle značka je známá po celém světě a hodně oblíbená"}),
    7060: (T + "«Tato … nevrátí» — коряво", {"example_cs": "Taková příležitost je jedinečná a už se nebude opakovat"}),
    7100: (T + "«vzájemně» — слово карточки «nápodobně»", {"example_cs": "Hezký víkend! – Díky, nápodobně!"}),
    7140: (T + "«potřásá hlavou» — по-чешски «kroutí»", {"example_cs": "Jen kroutí hlavou"}),
    7224: (T + "«toto» — книжно", {"example_cs": "Na tohle téma máme rozdílné názory"}),
    7291: (T + "man verpackt — безлично", {"example_cs": "Každá sklenice se balí jednotlivě"}),
    7294: (T + "«Tuto» — книжно", {"example_cs": "Tuhle možnost nemůžeme vyloučit"}),
    7355: (T + "«Tato … velmi» — книжно", {"example_cs": "Tahle metoda je hodně účinná a šetří čas"}),
    7394: (T + "«kilogramů» — книжно", {"example_cs": "Miminko váží pět kil"}),
    7446: (T + "«obývacím pokoji» — книжно", {"example_cs": "Hračky leží rozházené všude po obýváku"}),
    7681: (T + "«Vyndávám» — не тот вид", {"example_cs": "Vyndám prádlo z pračky"}),
}

REPLACE = []

SPLIT_LATER = {}
