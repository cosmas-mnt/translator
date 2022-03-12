import re
import collections

CU_CHARS = '-\u0300\u0301\u0308\u0311\u033e\u0400\u0404\u0405\u0406\u040d\u0410\u0411\u0412\u0413\u0414\u0415\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f\u0430\u0431\u0432\u0433\u0434\u0435\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f\u0450\u0454\u0455\u0456\u0457\u045d\u0460\u0461\u0462\u0463\u0466\u0467\u046a\u046b\u046e\u046f\u0470\u0471\u0472\u0473\u0474\u0475\u0476\u0477\u047a\u047b\u047c\u047d\u047e\u047f\u0482\u0483\u0486\u0487\u1c81\u1c82\u2020\u2de0\u2de1\u2de2\u2de3\u2de4\u2de6\u2de7\u2de8\u2de9\u2dea\u2dec\u2ded\u2def\u2df1\u2df4\ua64a\ua64b\ua656\ua657\ua673\ua67e'
CU_CHARS = set(CU_CHARS)

C_EROK = '\u033e'
C_GRAVE = '\u0300'
C_ACUTE = '\u0301'
C_DIAERESIS = '\u0308'
C_CAP = '\u0311'

TITLO = '\u0483'

TITLO_REX = {
    '^а҆пⷭ҇л': 'апо\u0301стол',
    '^а҆пⷭ҇т': 'апо\u0301ст',
    '^а҆́гг҃єлъ': 'а\u0301нгелъ',
    '^а҆́г҃гл': 'а\u0301нгел',
    '^бг҃омъ$': 'бо\u0301гом',
    '^бг҃обл҃': 'богобла',
    '^бг҃ови$': 'бо\u0301гови',
    '^бг҃овии҆': 'бо\u0301говии',
    '^бг҃овлⷣчц': 'боговлады\u0301чиц',
    '^бг҃огл҃го́л': 'богоглаго\u0301л',
    '^бг҃зва́ннїи$': 'богозва\u0301ннии',
    '^бг҃оѻц҃ъ$': 'богооте\u0309ц',
    '^бг҃оѻц҃а̀': 'богоотца\u0301',
    '^богоѻц҃є́въ$': 'богоотце\u0301въ',
    '^богоѻч҃ес': 'богооте\u0301чес',
    '^богоѻ́ч҃е': 'богоо\u0301тче',
    '^бг҃омт҃р': 'богома\u0301тер',
    '^богомт҃': 'богома\u0301т',
    '^богочл҃в': 'богочелов',
    '^без̾ѻ́ч҃': 'безо\u0301тч',
    '^безбл҃года́т': 'безблагода\u0301т',
    '^безмт҃р': 'безма\u0301тер',
    '^безсм҃рт': 'безсме\u0301рт',
    '^безѻ́ч҃а$': 'безо\u0301тча',
    '^бг҃ѡ'  : 'бого',
    '^бг҃о'  : 'бого',
    '^бг҃'   : 'бо\u0301г',
    '^бжⷭ҇тв': 'боже\u0301ств',
    '^бж҃т'  : 'боже\u0301ст',
    '^бж҃е$' : 'бо\u0301же',
    '^бж҃еск': 'бо\u0301жеск',
    '^бж҃ї'  : 'бо\u0301жи',
    '^бж҃'   : 'бож',
    '^бз҃ѣ'  : 'бо\u0301зе',
    '^блгⷭ҇в': 'благослов',
    '^бл҃г\\b': 'бла\u0301г',
    '^бл҃га$': 'бла\u0301га',
    '^бл҃ги$': 'бла\u0301ги',
    '^бл҃гоже$': 'бла\u0301гоже',
    '^бл҃гомлⷭ҇т': 'благоми\u0301лост',
    '^бл҃гости$': 'бла\u0301гости',
    '^бл҃гость$': 'бла\u0301гость',
    '^бл҃гост': 'благост',
    '^бл҃го$': 'бла\u0301го',
    '^бл҃гъ$': 'бла\u0301г',
    '^бл҃гꙋ$': 'бла\u0301гу',
    '^бл҃гѡсти$': 'бла\u0301гости',
    '^бл҃же$': 'бла\u0301же',
    '^бл҃г'  : 'благ',
    '^бл҃ж'  : 'блаж',
    '^богобл҃': 'богобла',
    '^боговочл҃в': 'боговочелов',
    '^богомт҃ер': 'богома\u0301тер',
    '^богомт҃': 'богома\u0301т',
    '^богочл҃в': 'богочелов',
    '^богоѻ́ч҃е': 'богоо\u0301тче',
    '^богоѻц҃\\b': 'богоо\u0301тец',
    '^бцⷣ': 'богоро\u0301диц',
    '^великомч҃н': 'великому\u0301чен',
    '^влⷣ': 'влады\u0301',
    '^водоѡсщ҃': 'водоосвящ',
    '^водоосщ҃': 'водоосвящ',
    '^возбл҃г': 'возблаг',  # FIXME
    '^возгл҃г': 'возглаг',
    '^возгл҃': 'возглаго\u0301л',
    '^воскр҃съ': 'воскре\u0301съ',
    '^воскр҃сн': 'воскре\u0301сн',
    '^воскр҃сн': 'воскре\u0301сн',
    '^воскрⷭ҇н': 'воскре\u0301сн',
    '^воскрⷭ҇л': 'воскре\u0301сл',
    '^воскрⷭ҇ш': 'воскре\u0301сш',
    '^воскр҃ш': 'воскре\u0301сш',
    '^воскрⷭ҇ъ': 'воскре\u0301съ',
    '^вокр҃се́н': 'воскресе\u0301н',
    '^воскр҃сенъ': 'воскре\u0301сен',
    '^воскр҃се$': 'воскре\u0301се',
    '^воскр҃слъ': 'воскре\u0301сл',
    '^воскр҃сш': 'воскре\u0301сш',
    '^воскр҃с': 'воскрес',
    '^воскрⷭ҇': 'воскрес', # FIXME
    '^воцр҃': 'воцар',
    '^вочл҃овѣ́ч': 'вочелове\u0301ч',
    '^воч҃лвѣ́ч': 'вочелове\u0301ч',
    '^вочл҃в': 'вочелов',
    '^всебл҃же$': 'всебла\u0301же',
    '^всебл҃': 'всебла',
    '^всебж҃е́ст': 'всебоже\u0301ст',
    '^всепребл҃гі́й$': 'всепреблаги\u0301й',
    '^всепречⷭ҇т': 'всепречи\u0301ст',
    '^всесп҃си́т': 'всеспаси\u0301т',
    '^всеѡсщ҃': 'всеосвящ',
    '^всест҃е$': 'всесвя\u0301те',
    '^всест҃ъ$': 'всесвя\u0301тъ',
    '^всест҃ѡ$': 'всесвя\u0301то',
    '^всест҃': 'всесвят',
    '^всесщ҃е': 'всесвяще',
    '^всецр҃ц': 'всецари\u0301ц',
    '^всецр҃': 'всецар',
    '^всечⷭ҇та': 'всечи\u0301ста',
    '^всечⷭ҇тне$': 'всече\u0301стне',
    '^всечⷭ҇то': 'всечи\u0301сто',
    '^всечⷭ҇ты': 'всечи\u0301сты',
    '^всечⷭ҇тꙋ': 'всечи\u0301сту',
    '^всечⷭ҇т': 'всечест',
    '^всн҃овле́н': 'всыновле\u0301н',
    'гг҃л': 'нгел',
    '^гл҃а': 'глаго\u0301ла',
    '^гл҃ю': 'глаго\u0301лю',
    '^гл҃г': 'глаг',
    '^гл҃е': 'глаго\u0301ле',
    '^гл҃': 'глаг\u0301ол',
    '^гдⷭ҇и́н': 'господи\u0301н',
    '^гдⷭ҇и́н': 'господи\u0301н',
    '^гдⷭ҇ен': 'госпо\u0301ден',
    '^гдⷭ҇ви$': 'го\u0301сподеви',
    '^гдⷭ҇е́нь$': 'господе\u0301нь',
    '^гдⷭ҇ень$': 'господе\u0301нь',
    '^гдⷭ҇енъ$': 'господе\u0301нъ',
    '^гдⷭ҇к$': 'госпо\u0301дски',
    '^гдⷭ҇н': 'госпо\u0301дн',
    '^гдⷭ҇омъ': 'го\u0301сподомъ',
    '^гдⷭ҇о': 'господо',
    '^гдⷭ҇рн': 'господа\u0301рн',
    '^гдⷭ҇р': 'го\u0301сподар',
    '^гдⷭ҇ск': 'госпо\u0301дск',
    '^гдⷭ҇ст': 'госпо\u0301дст',
    '^гдⷭ҇': 'госпо\u0301д', # FIXME
    '^гпⷭ҇ж': 'госпож',
    '^гпⷭ҇': 'го\u0301сп',  # FIXME
    '^дв҃и̑чꙋ$': 'де\u0301вичу',
    '^дв҃а': 'де\u0301ва',
    '^дв҃д': 'дав\u0301ид',
    '^дв҃и́ц': 'деви\u0301ц',
    '^дв҃и́ч': 'деви\u0301ч',
    '^дв҃ома́т': 'девома\u0301т',
    '^дв҃омт҃и': 'девома\u0301ти',
    '^дв҃о': 'де\u0301во',
    '^дв҃ц': 'де\u0301виц',
    '^дв҃ст': 'де\u0301вст',
    '^дв҃ч': 'деви\u0301ч',
    '^дв҃ы': 'де\u0301вы',
    '^дв҃ѣ': 'де\u0301вѣ',
    '^дв҃ꙋ': 'де\u0301вꙋ',
    '^двⷭ҇т': 'де\u0301вст',
    '^добродв҃о$': 'доброде\u0301во',
    '^добромч҃н': 'доброму\u0301чен',
    '^девомт҃и': 'девома\u0301ти',
    '^достобл҃ж': 'достоблаж',
    '^достойнобж҃е́с': 'достойнобоже\u0301с',
    '^дх҃о́в': 'духо\u0301в',
    '^дх҃ови$': 'ду\u0301хови',
    '^дх҃овꙋ$': 'ду\u0301хову',
    '^дх҃ов': 'духов',
    '^дх҃обо́р': 'духобо\u0301р',
    '^дх҃ог': 'духог',
    '^дх҃од': 'духод',
    '^дх҃он': 'духон',
    '^дх҃ор': 'духор',
    '^дх҃$': 'ду\u0301х',
    '^дх҃ъ': 'ду\u0301х',
    '^дх҃а': 'ду\u0301ха',
    '^дх҃о': 'ду\u0301хо',
    '^дх҃ꙋ': 'ду\u0301хꙋ',
    '^дш҃е$': 'ду\u0301ше',
    '^дш҃е': 'душе',
    '^дс҃ѣ': 'ду\u0301се',
    '^дꙋшесп҃с': 'душеспас',
    '^дх҃н': 'духн',
    '^дх҃ѣ$': 'ду\u0301хе',
    '^дх҃ѡ́в': 'духо\u0301в',
    '^дш҃': 'ду\u0301ш',
    '^дѣвомч҃н': 'девому\u0301чен',
    '^заⷱ҇': 'зач',
    '^и҆́мⷬ҇к$': 'имяре\u0301к',
    '^кн҃же$': 'кня\u0301же',
    '^кн҃жескꙋю$': 'кня\u0301жескую',
    '^кн҃з': 'кня\u0301з',  # FIXME
    '^крестобг҃о': 'крестобого',
    '^крестовоскрⷭ҇': 'крестовоскре\u0301с',
    '^кр҃сти́с': 'крести\u0301с',
    '^кр҃щ': 'крещ',
    '^крⷭ҇ти́т': 'крести\u0301т',
    '^крⷭ҇тобг҃о': 'крестобого',
    '^крⷭ҇то́мъ$': 'крестом',
    '^крⷭ҇товоскрⷭ҇нъ$': 'крестовоскресе\u0301н',
    '^крⷭ҇товоскрⷭ҇н': 'крестовоскре\u0301сн',
    '^крⷭ҇тъ': 'кре\u0301ст',
    '^крⷭ҇то́мъ$': 'кресто\u0301м',
    '^крⷭ҇тон': 'крестон',
    '^крⷭ҇тн': 'кре\u0301стн',
    '^крⷭ҇т': 'крест',
    '^кн҃г': 'княг',
    '^любобл҃же$': 'любобла\u0301же',
    '^любобж҃е́с': 'любобоже\u0301ст',
    '^любобл҃': 'любобла',
    '^ма́теродв҃о': 'ма\u0301теродево',
    '^мл҃твома́с': 'молитвома\u0301с',
    '^мл҃твосло́в': 'молитвосло\u0301в',
    '^мл҃т': 'моли\u0301т',
    '^млⷣн': 'младе\u0301н',
    '^мл҃и́т': 'моли\u0301т',
    '^млⷭ҇рд': 'милосе\u0301рд',
    '^млⷭ҇т': 'ми\u0301лост',  # FIXME
    '^многомлⷭ҇т': 'многоми\u0301лост',
    '^многобл҃го': 'многоблаго',
    '^мр҃': 'мари', # FIXME
    '^мт҃редв҃ꙋ': 'матереде\u0301ву',
    '^мт҃родв҃о': 'матереде\u0301во',
    '^мт҃родѣ́в': 'матероде\u0301в',
    '^мт҃ролѣ́п': 'матероле\u0301п',
    '^мт҃и$': 'ма\u0301ти',
    '^мт҃ер':'ма\u0301тер',
    '^мт҃р': 'ма\u0301тер',
    '^мцⷭ҇а': 'ме\u0301сяца',
    '^мч҃николю́б': 'мучениколю\u0301б',
    '^мч҃нц': 'му\u0301чениц',
    '^мч҃нч': 'му\u0301ченич',
    '^мч҃ен': 'му\u0301чен',
    '^мч҃н': 'му\u0301чен',
    '^мч҃є': 'му\u0301че',
    '^мѷробл҃гоꙋха̑н': 'мироблагоуха\u0301н',
    '^нб҃омъ$': 'не\u0301бом',
    '^нб҃о$': 'не\u0301бо',
    '^нб҃а$': 'не\u0301ба',
    '^нб҃се$': 'небе\u0301се',
    '^нб҃сн': 'небе\u0301сн',
    '^нб҃съ$': 'небе\u0301с',
    '^нб҃ѣ$': 'не\u0301бе',
    '^нб҃ꙋ$': 'не\u0301бу',
    '^нб҃с': 'небес',  # FIXME
    '^нб҃': 'неб',
    '^нбⷭ҇ножи́т': 'небесножи\u0301т',
    '^нбⷭ҇нотаи́н': 'небеснотаи\u0301н',
    '^нбⷭ҇н': 'небе\u0301сн', # FIXME
    '^нбⷭ҇': 'небес', # FIXME
    '^небл҃г': 'неблаг',
    '^небг҃обоѧ́з': 'небогобоя\u0301з',
    '^неизгл҃го́л': 'неизглаго\u0301л',
    '^немлⷭ҇т': 'неми\u0301лост',
    '^несщ҃е́н': 'несвяще\u0301н',
    '^неѡсщ҃е́н': 'неосвяще\u0301н',
    '^новомч҃н': 'новому\u0301чен',
    '^нн҃ѣ$': 'ны\u0301не',
    '^нн҃ѣш': 'ны\u0301неш',
    '^оу҆ч҃нкъ$': 'учени\u0301к',
    '^оу҆ч҃нк': 'ученик',
    '^оу҆чн҃ц': 'учениц',
    '^оу҆ч҃тл': 'учи\u0301тел',
    '^оу҆чн҃икѡ́м': 'ученико\u0301м',
    '^оу҆ч҃н': 'учен',
    '^оу҆бл҃ж': 'ублаж',
    '^о҆бл҃г': 'облаг',
    '^о҆ст҃': 'освят',
    '^о҆сщ҃': 'освящ',
    '^первомч҃н': 'первому\u0301чен',
    '^первост҃и́т': 'первосвяти\u0301т',
    '^первосщ҃е́н': 'первосвяще\u0301н',
    '^первосщ҃енно': 'первосвященно',
    '^первост҃а́ѧ': 'первосвята\u0301я',
    '^пл҃т': 'пло\u0301т',
    '^посщ҃е́н': 'посвяще\u0301н',
    '^пра́ѻц҃ъ$': 'пра\u0301отец',
    '^пра́ѻц҃а': 'пра\u0301отца',
    '^пра́ѻц҃': 'пра\u0301отц',
    '^пра̑ѻц҃': 'праоте\u0301ц',
    '^пра́ѻч҃е': 'пра\u0301отече',
    '^прамт҃и$': 'прама\u0301ти',
    '^прамт҃р': 'прама\u0301тер',
    '^првⷣн': 'пра\u0301ведн',
    '^пребж҃': 'пребож',
    '^пребжⷭ҇т': 'пребоже\u0301ст',
    '^пребл҃га$': 'пребла\u0301га',
    '^пребл҃гъ$': 'пребла\u0301гъ',
    '^пребл҃гꙋ$': 'пребла\u0301гу',
    '^пребл҃г': 'преблаг',
    '^пребл҃же$': 'пребла\u0301же',
    '^пребл҃ж': 'преблаж',
    '^пред̾ѡсщ҃е́н': 'предосвяще\u0301н',
    '^преждеѡсщ҃є́н': 'преждеосвяще\u0301н',
    '^преждеосщ҃': 'преждеосвящ',
    '^преждесщ҃': 'преждесвящ',
    '^преждеѡсщ҃е́н': 'преждеосвящен',
    '^пренб҃': 'пренеб',
    '^пренбⷭ҇н': 'пренебе\u0301сн',
    '^пресщ҃е́н': 'пресвяще\u0301н',
    '^пресщ҃є́н': 'пресвяще\u0301н',
    '^преѡсщ҃е́н': 'пресвяще\u0301н',
    '^прест҃ъ$': 'пресвя\u0301т',
    '^прест҃': 'пресвят',
    '^преподобномч҃нц': 'преподобному\u0301чениц',
    '^преподобномч҃нк': 'преподобному\u0301ченик',
    '^преподобномч҃нче': 'преподобнрму\u0301чениче',
    '^преподобномч҃ни': 'преподобному\u0301чени',
    '^преподобномч҃н': 'преподобному\u0301чен',
    '^пречтⷭ҇н': 'пречестн',
    '^пречⷭ҇т': 'пречест',
    '^пречтⷭ҇': 'пречи\u0301ст',
    '^приснобл҃го': 'присноблаго',
    '^приснобл҃ж': 'присноблаж',
    '^приснод҃в': 'присноде\u0301в',
    '^приснодв҃': 'присноде\u0301в',
    '^прпⷣбноисповѣ́дн': 'преподобноиспове\u0301дн',
    '^прпⷣбномꙋ$': 'преподо\u0301бному',
    '^прпⷣбною$': 'преподо\u0301бною',
    '^преподобномч҃н': 'преподобному\u0301чен',
    '^прпⷣбно': 'преподобно',
    '^прпⷣб': 'преподо\u0301б',
    '^прст҃ы́ѧ$': 'пресвяты\u0301я',
    '^прст҃ꙋ́ю$': 'пресвяту\u0301ю',
    '^прⷣтча$': 'предте\u0301ча',
    '^прⷣт': 'предт',
    '^прⷪ҇рк': 'прор\u0301ок',
    '^прⷪ҇': 'про',
    '^прⷭ҇нодв҃': 'присноде\u0301в',
    '^прⷭ҇на$': 'при\u0301сна',
    '^прⷭ҇ное$': 'при\u0301сное',
    '^прⷭ҇номꙋ$': 'при\u0301сному',
    '^прⷭ҇нѣе$': 'при\u0301снее',
    '^прⷭ҇ны': 'при\u0301сны',
    '^прⷭ҇нї': 'при\u0301сни',
    '^прⷭ҇нѡ$': 'при\u0301сно',
    '^прⷭ҇н': 'присн',
    '^прⷭ҇т': 'прест',
    '^равноа́гг҃еленъ$': 'равноа\u0301нгелен',
    '^ржⷭ҇твен': 'рожде\u0301ствен',
    '^ржⷭ҇': 'рождес',
    '^самобл҃гі́й$': 'самоблаги\u0301й',
    '^сбг҃осло́в': 'сблагосло\u0301в',
    '^священномч҃нч': 'священному\u0301ченич',
    '^священномч҃нк': 'священному\u0301ченик',
    '^священномч҃нц': 'священному\u0301чениц',
    '^священномч҃нч': 'священному\u0301ченич',
    '^свѧщенномч҃н': 'священному\u0301чен',
    '^свѧщенност҃и́т': 'священносвяти\u0301т',
    '^сл҃нцез': 'солнцез',
    '^сл҃н': 'со\u0301лн',
    '^см҃рт': 'сме\u0301рт',
    '^совоскр҃с': 'совоскрес',
    '^сн҃а$': 'сы\u0301на',
    '^сн҃ове$': 'сы\u0301нове',
    '^сн҃ови$': 'сы\u0301нови',
    '^сн҃омъ$': 'сы\u0301ном',
    '^сн҃ъ$': 'сын',
    '^сн҃ы$': 'сы\u0301ны',
    '^сн҃є$': 'сы\u0301не',
    '^сн҃ѣ$': 'сы\u0301не',
    '^согл҃': 'соглаго\u0301л',
    '^содх҃нове́н': 'содучнове\u0301н',
    '^сп҃са$': 'спа\u0301са',
    '^сп҃се$': 'спа\u0301се',
    '^сп҃сѣ$': 'спа\u0301се',
    '^сп҃сꙋ$': 'спа\u0301су',
    '^сп҃сов': 'спа\u0301сов',
    '^сп҃сомъ$': 'спа\u0301сом',
    '^сп҃ссѧ$': 'спа\u0301сся',
    '^сп҃слъ$': 'спа\u0301сл',
    '^сп҃сш': 'спа\u0301сш',
    '^сп҃съ$': 'спа\u0301съ',
    '^сн҃': 'сын',
    '^сп҃сѡва$': 'спа\u0301сова',
    '^сп҃сѡвы$': 'спа\u0301совы',
    '^сп҃с': 'спас',
    '^стрⷭ҇ти$': 'стра\u0301сти',
    '^стрⷭ҇тнꙋю$': 'стра\u0301стную',
    '^стрⷭ҇ть$': 'стра\u0301сть',
    '^стрⷭ҇тїю$': 'стра\u0301стию',
    '^стрⷭ҇т': 'страст',
    '^ст҃а$': 'свя\u0301та',
    '^ст҃льства$': 'сто\u0301льства',
    '^ст҃лю$': 'святи\u0301телю',
    '^ст҃о$': 'свя\u0301то',
    '^ст҃е$': 'свято\u0301е',
    '^ст҃и': 'свя\u0301ти',
    '^ст҃ост': 'свя\u0301тост',
    '^ст҃ъ$': 'свя\u0301т',
    '^ст҃ы$': 'свя\u0301ты',
    '^ст҃ѡ$': 'свя\u0301то',
    '^ст҃ѣ$': 'свя\u0301те',
    '^ст҃ꙋ$': 'свя\u0301ту',
    '^ст҃тел': 'святи\u0301тел',
    '^ст҃': 'свят',
    '^сщ҃енно$': 'свяще\u0301нно',
    '^сщ҃': 'свящ',
    '^тетроєѵⷢ҇л': 'тетроева\u0301нгел',
    '^требл҃ж': 'треблаж',
    '^трист҃е$': 'трисвято\u0301е',
    '^трист҃': 'трисвят',
    '^трисл҃н': 'трисо\u0301лн',
    '^трⷪ҇ц': 'тро\u0301иц',
    '^трⷪ҇ч': 'тро\u0301ич',
    '^трⷭ҇т': 'трисвят',
    '^у҆бл҃ж': 'ублаж',
    '^у҆млⷭ҇р': 'умилосе\u0301р',
    '^у҆чн҃к': 'учени\u00301к',
    '^у҆ч҃н': 'учен',
    '^у҆ч҃тел': 'учи\u0301тел',
    '^у҆ч҃тл': 'учи\u0301тел',
    '^ᲂу҆ч҃тл': 'учи\u0301тел',
    '^ᲂу҆ч҃т': 'учи\u0301т',
    '^ᲂу҆ч҃нц': 'учени\u0301ц',
    '^ᲂу҆чн҃ц': 'учени\u0301ц',
    '^ᲂу҆ч҃нч': 'учени\u0301ч',
    '^ᲂу҆ч҃н': 'уче\u0301н',
    '^ᲂу҆чт҃л': 'учи\u0301тел',
    '^ᲂу҆бл҃ж': 'ублаж',
    '^ᲂу҆чн҃къ$': 'учени\u0301к',
    '^ᲂу҆чн҃к': 'ученик',
    '^ᲂуч҃нкѡ́м': 'ученико\u0301м',
    '^ᲂу҆чн҃и́к': 'учени\u0301к',
    '^ᲂу҆млⷭ҇тив': 'умилостив',
    '^хрⷭ҇томч҃нц': 'христому\u0301чениц',
    '^хрⷭ҇': 'хрис',
    '^цр҃кве́й$': 'церкве\u0301й',
    '^цр҃кво': 'церкво',
    '^цр҃ко́в': 'церко\u0301в',
    '^цр҃кѡ́в': 'церко\u0301в',
    '^цр҃к': 'це\u0301рк',
    '^цр҃ск': 'ца\u0301рск',
    '^цр҃ц': 'цари\u0301ц',
    '^цр҃ь$': 'ца\u0301рь',
    '^цр҃їе$': 'ца\u0301рие',
    '^цр҃': 'цар',
    '^црⷭ҇': 'ца\u0301рс',
    '^чл҃колю́б': 'человеколю\u0301б',
    '^чл҃кѡмъ': 'челове\u0301комъ',
    '^чл҃в': 'челов',
    '^чⷭ҇та$': 'чи\u0301ста',
    '^чⷭ҇таг': 'чи\u0301стаг',
    '^чтⷭ҇ѣ́й': 'чисте\u0301й',
    '^чⷭ҇тна$': 'че\u0301стна',
    '^чⷭ҇тни$': 'че\u0301стни',
    '^чⷭ҇тно$': 'че\u0301стно',
    '^чтⷭ҇нѡ'
    '^чⷭ҇тны$': 'че\u0301стны',
    '^чⷭ҇тнѡ$': 'че\u0301стнѡ',
    '^чⷭ҇тнѣй$': 'че\u0301стней',
    '^чⷭ҇тнꙋ$': 'че\u0301стну',
    '^чтⷭ҇нꙋ$': 'че\u0301стну',
    '^чтⷭ҇на$': 'че\u0301стна',
    '^чтⷭ҇нѡ$': 'че\u0301стно',
    '^чтⷭ҇н': 'честн',
    '^чⷭ҇тн': 'честн',
    '^чтⷭ҇': 'чи\u0301ст',
    '^є҆пⷭ҇кп': 'епи\u0301скоп',
    '^є҆ѵⷢ҇лі́с': 'евангели\u0301с',
    '^є҆ѵⷢ҇ло': 'евангело',
    '^є҆ѵⷢ҇л': 'ева\u0301нгел',
    '^є҆леосщ҃е́нїе$': 'улееосвяще\u0301ние',
    '^і҆ерⷭ҇л': 'иерусал',
    '^і҆и҃льтѧ́н': 'израильтя\u0301н',
    '^і҆и҃лі́т': 'израити\u0301т',
    '^і҆и҃л': 'изра\u0301ил',
    '^і҆и҃сꙋ́с': 'иису\u0301с',
    '^і҆и҃с': 'иису\u0301с',
    '^ѡ҆бг҃отвор': 'обоготвор',
    '^ѡ҆дх҃новле́нна$': 'одухновле\u0301нна',
    '^ѡ҆бж҃е́н': 'обоже\u0301н',
    '^ѡ҆сщ҃': 'освящ',
    '^ѡ҆бл҃го': 'облаго',
    '^ѡ҆н҃беси́л': 'онебеси\u0301л',
    '^ѡ҆нб҃с': 'онебес',
    '^ѡ҆ст҃': 'освят',
    '^ѻ҆гнедх҃нове́н': 'огнедухнове\u0301н',
    '^ѻ҆тч҃скимъ$': 'оте\u0301ческим',
    '^ѻ҆т҃ческимъ$': 'оте\u0301ческим',
    '^ѻ҆ч҃с': 'от\u0301чес',
    '^ѻ҆ч҃ь$': 'оте\u0301чь',
    '^ѻ҆́ч҃': 'о\u0301тч',
    '^ѻ҆ц҃ъ$': 'оте\u0301ц',
    '^ѻ҆ч҃еисх': 'отчеисх',
    '^ѻ҆ч҃ерож': 'отчерож',
    '^ѻ҆ч҃еси́л': 'отечеси\u0301л',
    '^ѻ҆ц҃': 'отц',
    '^ѻ҆́ч҃ес': 'оте\u0301чес',
    '^ѻ҆ч҃естволю́б': 'отечестволю\u0301б',
    '^ѻ҆ч҃е': 'оте\u0301че',
    '^ѻ҆ч҃є': 'оте\u0301че',
    '^ѿнн҃ѣ': 'отны\u0301не',
}


def untitlo(word):
    for regexp, subst in TITLO_REX.items():
        expansion = re.sub(regexp, subst, word)
        if word != expansion:
            return expansion
    return word


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Expands titlo')
    parser.add_argument('-i', '--input', default='cu-words.txt')
    parser.add_argument('-o', '--output', default='cu-words-untitlo.txt')

    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        dataset = [l.strip().split() for l in f]

    print(f'Loaded {len(dataset)} words')

    with open(args.output, 'w', encoding='utf-8') as f:
        counter = 0
        for word, count in dataset:
            counter += 1
            if counter % 1000 == 0:
                print(counter)
            expansion = untitlo(word)
            f.write(f'{word}\t{expansion}\t{count}\n')
