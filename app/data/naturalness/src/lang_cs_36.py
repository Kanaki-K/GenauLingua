"""Вычитка чешского, порция p036 (B2), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    16277: (T + "«velmi» — книжно", {"example_cs": "Oddělení vražd vyšetřuje případ hodně pečlivě"}),
    16287: (T + "«Odkazem mého dědečka» — тяжело", {"example_cs": "Dědovým odkazem byl jeho starý deník"}),
    16310: (T + "«Můj strýc» — книжно", {"example_cs": "Strýc byl dřív pilotem u letectva"}),
    16337: (T + "«Můj strýc» — книжно", {"example_cs": "Strýc byl v armádě velitelem skoro tisíce vojáků"}),
    16342: (T + "«Můj strýc» — книжно", {"example_cs": "Strýc v Texasu už čtyřicet let volí republikány"}),
    16357: (T + "«Můj praděda» — книжно", {"example_cs": "Praděda byl přesvědčený komunista a každou neděli se hádal s farářem"}),
    16380: (T + "«Moje malá sestra» — книжно", {"example_cs": "Sestřička si hraje na královnu a my ostatní musíme být její poddaní"}),
    16396: (T + "«Můj praděda» — книжно", {"example_cs": "Praděda sloužil za války u pěchoty a nikdy o tom nedokázal mluvit"}),
    16580: (T + "«Ve straně mé babičky» — тяжело", {"example_cs": "V babiččině straně si všichni pořád říkají soudružko a soudruhu"}),
    16642: (T + "«velmi» — книжно", {"example_cs": "Policista mi moc vlídně vysvětlil, že tady nesmím parkovat"}),
    16769: (T + "«Můj malý syn» — книжно", {"example_cs": "Malý syn salutuje pokaždé, když kolem nás projede policejní auto"}),
    16796: (T + "«Moje teta» — книжно", {"example_cs": "Teta z Ohia napsala dopis svému kongresmanovi, protože silnice před jejím domem je samá díra"}),
    16979: (T + "«Můj soused» — книжно", {"example_cs": "Soused sedí v obecním zastupitelstvu a chce konečně prosadit semafor před školou"}),
    17146: (T + "«Můj odjezd je» — калька", {"example_cs": "Odjezd mám zítra ráno v sedm"}),
    17153: (T + "«než se čekalo» — книжно", {"example_cs": "Cesta zpět byla delší, než jsme čekali"}),
    17164: (T + "«na mém kole» — калька", {"example_cs": "Na kole mám moc vysoko sedlo, nedosáhnu nohama na zem"}),
    17165: (T + "«celá moje» — калька", {"example_cs": "Po pádu počítače byla celá seminárka pryč"}),
}

REPLACE = []

SPLIT_LATER = {}
