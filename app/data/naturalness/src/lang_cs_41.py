"""Вычитка чешского, порция p041 (C1), 23.10: кальки и книжные обороты → разговорный чешский"""

T = "вычитка чешского: "

FIXES = {
    11059: (T + "«propadali smutku» — книжно", {"example_cs": "Místo abychom v dešti jen smutnili, pečeme s dětmi v neděli prostě vafle"}),
    11074: (T + "«Učitelka mé dcery» — тяжело", {"example_cs": "Dceřina učitelka je tak inspirativní, že teď chce být taky učitelkou"}),
    11091: (T + "«dnes» → «dneska»", {"example_cs": "Buď rozumný a vezmi si deštník, má dneska pršet"}),
    11093: (T + "«své … oceňuji» — книжно", {"example_cs": "Na šéfové oceňuju upřímnost, i když někdy bolí"}),
    11096: (T + "«dnes» → «dneska»", {"example_cs": "Od narození miminka jsem tak roztržitá, že jsem dneska dala mléko do skříně"}),
    11106: (T + "«je každý týden větší» — коряво", {"example_cs": "Město zůstává nečinné, i když se díra před domem každý týden zvětšuje"}),
    11114: (T + "«Moje tolerance» — калька", {"example_cs": "Po desáté večer mám toleranci k hlasité hudbě nulovou"}),
    11115: (T + "«Moje neschopnost mi přináší» — калька", {"example_cs": "Kvůli neschopnosti říct ne mám každý víkend nové úkoly"}),
    11123: (T + "«Naše» — лишнее", {"example_cs": "Dvouletá dcera teď vzdoruje všemu, co řekneme"}),
    11127: (T + "«působí přitažlivostí» — калька", {"example_cs": "Lednička má na mě v noci magickou přitažlivost"}),
    11132: (T + "«Moje nechuť je známá» — калька", {"example_cs": "O mé nechuti k ranním schůzkám ví celá kancelář"}),
    11137: (T + "«Můj … velmi» — книжно", {"example_cs": "Přítel je hodně nápaditý, když jde o výmluvy, proč nemůže tančit"}),
    11138: (T + "«v mé firmě» — лишнее", {"example_cs": "Dřív bylo nemyslitelné, aby muži šli na rodičovskou, dneska to u nás ve firmě dělá každý druhý"}),
    11145: (T + "«Můj» — лишнее", {"example_cs": "Bývalý šéf mě pořád šikanoval nesmyslnými tabulkami v Excelu"}),
    11146: (T + "«Po mém pádu» — калька", {"example_cs": "Když jsem upadl na ledě, neměl posměch kamarádů konce"}),
    11148: (T + "«zachází tak daleko» — книжно", {"example_cs": "Uctívání zpěváka je u fanoušků takové, že stanují před jeho hotelem"}),
    11182: (T + "«Moje heslo» — калька", {"example_cs": "Heslo mám zkompromitované, musím všude nastavit nové"}),
    11187: (T + "«na základě» — канцелярит", {"example_cs": "Byt jsem vzala podle intuice a bylo to správné rozhodnutí"}),
    11199: (T + "«pokus … bylo» — согласование", {"example_cs": "První pokus vytapetovat si obývák sami byl naprosté fiasko"}),
    11241: (T + "«Můj» — лишнее", {"example_cs": "Kocour se cítí nade vše povznesený a ignoruje nás, když ho voláme"}),
    11458: (T + "«upadl v nevážnost» — книжно", {"example_cs": "Kvůli jediné špatné recenzi získal malý hotel úplně neprávem špatnou pověst"}),
    11461: (T + "«mou» — лишнее", {"example_cs": "Pro italskou švagrovou je smetana v carbonaře zvrácenost"}),
    11490: (T + "«Obdivuji» → «Obdivuju»", {"example_cs": "Obdivuju klid, s jakým máma hlídá pět vnoučat najednou"}),
    11815: (T + "«bobule» в лесу — не то", {"example_cs": "V létě chodíme do lesa na lesní plody a vaříme z nich marmeládu"}),
    11830: (T + "порядок слов", {"example_cs": "Kdo u babičky nesní všechno z talíře, nedostane dezert"}),
    11848: (T + "«cibuli v ní» — порядок", {"example_cs": "Babiččina sekaná je tak dobrá, že v ní děti jedí i cibuli"}),
    11856: (T + "«mé babičky» — тяжело", {"example_cs": "U babičky na vesnici děti na Halloween nevyřezávají dýně, ale řepy"}),
    11896: (T + "«svá» — лишнее", {"example_cs": "V budce na balkoně teď sýkorky krmí mláďata"}),
    12284: (T + "«můj táta syna» — коряво", {"example_cs": "„Tak co, kámo, zase jsi kopl míč k sousedům na zahradu?“ ptá se táta vnuka"}),
    12288: (T + "«svůj» — лишнее", {"example_cs": "Manžel na podzim běží první maraton a já s dětmi stojím u trati s banány"}),
    12294: (T + "«běží olympiáda» — калька", {"example_cs": "Od té doby, co v televizi dávají olympiádu, chce dcera být gymnastka a všude dělá hvězdy"}),
    12301: (T + "«utkání» — книжно", {"example_cs": "O poločase rychle donesu pivo ze sklepa, abych ze zápasu nic nezmeškal"}),
    12315: (T + "«svou» — лишнее", {"example_cs": "Kolega každé ráno ve vlaku plete šálu pro přítelkyni"}),
    12757: (T + "«mého» — лишнее", {"example_cs": "Prvním příznakem nachlazení je u manžela vždycky špatná nálada"}),
    12766: (T + "«Můj dědeček» — лишнее", {"example_cs": "Děda má cukrovku a musí si hlídat stravu"}),
    12808: (T + "«svou» — лишнее", {"example_cs": "Hlasitým odkašláním dává děda najevo, že teď chce pronést řeč"}),
}

REPLACE = []

SPLIT_LATER = {}
