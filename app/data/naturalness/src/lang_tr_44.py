"""Вычитка турецкого, порция p044 (C1), 23.10: право, транспорт, техника, экономика, наука, дом — кальки → разговорный турецкий"""

T = "вычитка турецкого: "

FIXES = {
    16563: (T + "«otobüsün kadın şoförüne» — тяжело", {"example_tr": "Bir yolcu otobüs şoförüne hakaret edince iş arkadaşım herkesin önünde ona ırkçı dedi"}),
    16590: (T + "«üç randevu gerekiyor» — тяжело", {"example_tr": "Yeni bir kimlik kartı için üç ayrı randevu lazım, buradaki bürokrasi inanılmaz"}),
    16609: (T + "«korunmasını … üstleniyor» — канцелярит", {"example_tr": "Bahçemizi artık herkese tıslayan bir kaz koruyor"}),
    16929: (T + "«izin almam gerekiyor» → «lazım»", {"example_tr": "Arkadan çarpma kazası yüzünden mahkeme beni tanık olarak çağırdı, şimdi izin almam lazım"}),
    17218: (T + "«Denizaşırı teyzemden» — коряво", {"example_tr": "Teyzemin denizaşırıdan gönderdiği paket altı haftada geldi ve çikolata erimişti"}),
    17230: (T + "«girmesine izin verildi» — канцелярит", {"example_tr": "İnişten sonra oğlum kısa bir süre kokpite girebildi ve kadın pilotla fotoğraf çektirdi"}),
    17254: (T + "«oturmalarına izin verildi» — канцелярит", {"example_tr": "Havalimanının açık kapı gününde çocuklar hangara girip kokpite oturabildi"}),
    17261: (T + "«annemlerle babam» — ошибка", {"example_tr": "Emekli olduktan sonra annemle babam karavanla İskandinavya'yı turluyor ve her gün fotoğraf gönderiyor"}),
    17266: (T + "«binmesine izin verildi» — канцелярит", {"example_tr": "Oğlum buharlı trende öndeki lokomotife binebildi, şimdi yüzü baştan aşağı is içinde"}),
    17287: (T + "«ödememiz gerekiyormuş» — коряво", {"example_tr": "Kiralık arabada bizim yapmadığımız bir göçük var ve şimdi bizden para istiyorlar"}),
    17601: (T + "«basmasına izin verildi» — канцелярит", {"example_tr": "Televizyon stüdyosu ziyaretinde oğlum kontrol odasına girip bir düğmeye basabildi"}),
    17602: (T + "«adaptöre ihtiyacım oluyor» — калька", {"example_tr": "Yeni dizüstü bilgisayarımın sadece iki portu var ve sürekli adaptör lazım oluyor"}),
    17650: (T + "«izlemelerine rağmen» — тяжело", {"example_tr": "Annemler sadece iki kanal izlediği hâlde hâlâ kablolu televizyona para ödüyor"}),
    17653: (T + "«Bir geri çağırma nedeniyle» — канцелярит", {"example_tr": "Üretici geri çağırma yaptığı için arabamız gelecek hafta servise gidecek"}),
    17850: (T + "«hakkında tahminde bulunuyor» — канцелярит", {"example_tr": "Ofiste herkes patronun neden birden bu kadar keyifli olduğuna dair tahmin yürütüyor"}),
    18006: (T + "«Benim hipotezim, … aşırdığı» — оборвано", {"example_tr": "Benim hipotezim şu: ekmeği masadan kedi değil köpek aşırdı"}),
    18025: (T + "«kalıba ihtiyacın var» — калька", {"example_tr": "Pasta için 26 santimetre çapında bir kalıp lazım"}),
    18332: (T + "«Çocuk doğum gününde» — коряво", {"example_tr": "Doğum günü partisinde bodrum bizim zindanımız oluyor, yakalanan bir şarkı söylemek zorunda"}),
    18359: (T + "«gerekiyor» → «lazım»", {"example_tr": "Tatilden önce alışveriş merakımı biraz dizginlemem lazım"}),
    18370: (T + "«çıkması gerekiyor» — тяжело", {"example_tr": "Okulda yangın alarmı çalınca bütün çocuklar spor sahasına çıkmak zorunda"}),
}

REPLACE = []

SPLIT_LATER = {}
