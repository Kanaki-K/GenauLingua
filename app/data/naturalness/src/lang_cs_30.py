"""Вычитка чешского, порция p030 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    10471: (T + "«Dívky» — книжно", {"example_cs": "Holky ječí radostí"}),
    10479: (T + "«svého» — лишнее", {"example_cs": "V šestnácti byla sestra až po uši zamilovaná do učitele kytary"}),
    10485: (T + "«potřebuji» — книжно", {"example_cs": "U domácích úkolů potřebuju hodně soustředění"}),
    10488: (T + "«tímto» — книжно", {"example_cs": "Jsem tím příběhem naprosto fascinovaný"}),
    10495: (T + "«Obdivuji» — книжно", {"example_cs": "Obdivuju její trpělivost s dětmi"}),
    10498: (T + "«tento» — книжно", {"example_cs": "Je naprosto neschopný ten úkol splnit"}),
    10508: (T + "«Moje sestra» — калька", {"example_cs": "Sestra pořád naříká, když musí dělat úkoly"}),
    10509: (T + "«velmi … moc» — книжно", {"example_cs": "Byla jím hodně okouzlená, moc se jí líbil"}),
    10510: (T + "«velmi» — книжно", {"example_cs": "Návod je hrozně matoucí, nerozumím mu"}),
    10512: (T + "«Dívky» — книжно", {"example_cs": "Holky se za mnou chichotají"}),
    10515: (T + "«potřeba vody velmi velká» — коряво", {"example_cs": "V horku má člověk velkou potřebu pít"}),
    10518: (T + "«Svěřuji své» — книжно", {"example_cs": "Svěřím ti tajemství"}),
    10522: (T + "«pro má umělecká díla» — книжно", {"example_cs": "Příroda je velkou inspirací pro moji tvorbu"}),
    10549: (T + "«velmi» — книжно", {"example_cs": "Je to hodně uzavřený člověk"}),
    10550: (T + "«velmi» — книжно", {"example_cs": "Je hodně mlčenlivý a nic nevypráví"}),
    10557: (T + "«Moje kočka» — калька", {"example_cs": "Kočka nemá ráda dotek na bříšku, hned škrábe"}),
    10559: (T + "«velmi» — книжно", {"example_cs": "Vnitřně byl hrozně smutný, ale usmíval se"}),
    10561: (T + "«velmi» — книжно", {"example_cs": "To byl hodně odvážný nápad"}),
    10580: (T + "«žertuji» — книжно", {"example_cs": "Jen s tebou žertuju"}),
    10588: (T + "«svou» — лишнее", {"example_cs": "Chtěl bych tu chybu napravit"}),
    10612: (T + "«Mnozí … tohoto» — книжно", {"example_cs": "Hodně lidí sílu toho týmu podceňuje"}),
    10614: (T + "«mnoho» — книжно", {"example_cs": "Válka přináší lidem spoustu neštěstí"}),
    10616: (T + "«Tento … mnoho» — книжно", {"example_cs": "Ten obraz ve mně probouzí spoustu vzpomínek"}),
    10618: (T + "«Přeji tvůj» — книжно", {"example_cs": "Přeju ti ten úspěch, opravdu"}),
    10641: (T + "«Při mé hodině» — калька", {"example_cs": "Ve svých hodinách netrpím mobily na lavici"}),
    10655: (T + "«Můj bratr» — книжно", {"example_cs": "Brácha je opravdu nadaný, umí skvěle kreslit"}),
    10675: (T + "«Mnoho» — книжно", {"example_cs": "Spousta učitelů si stěžuje, že děti skoro nečtou knihy"}),
    10683: (T + "«své» — лишнее", {"example_cs": "Komplimenty se snaží získat přízeň šéfové"}),
    10689: (T + "«velmi» — книжно", {"example_cs": "Dítě je hodně přizpůsobivé a nemá ve škole problémy"}),
    10692: (T + "порядок слов", {"example_cs": "Nic bychom neměli uspěchat"}),
    10695: (T + "«svému» — лишнее", {"example_cs": "Chová k bratrovi zášť"}),
    10707: (T + "«Potřebuji» — книжно", {"example_cs": "Potřebuju mít jasno v tvých plánech"}),
    10734: (T + "«svou» — лишнее", {"example_cs": "Láskyplně se stará o babičku"}),
    10746: (T + "«daroval» — книжно", {"example_cs": "Místo květin jí k narozeninám dal strom, docela originální"}),
    10755: (T + "«Moje intuice» — калька", {"example_cs": "Intuice mi napovídá, že něco nesedí"}),
}

REPLACE = []

SPLIT_LATER = {}
