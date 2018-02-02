from conjugator import regex_rule
from conjugator import rule
from nltk.stem import WordNetLemmatizer

PAST_TENSE_RULE = "pastTense"
PRESENT_TENSERULE = "presentTense"
PAST_PARTICIPLE_RULE = "pastParticiple"
PRESENT_PARTICIPLE_RULE = "presentParticiple"
CONS = "[bcdfghjklmnpqrstvwxyz]"
ANY_STEM = "^((\\w+)(-\\w+)*)(\\s((\\w+)(-\\w+)*))*$"
VERBAL_PREFIX = "((be|with|pre|un|over|re|mis|under|out|up|fore|for|counter|co|sub)(-?))"

PERSON = "person"
FIRST_PERSON = 1
SECOND_PERSON = 2
THIRD_PERSON = 3
TENSE = "tense"
PAST_TENSE = 4
PRESENT_TENSE = 5
FUTURE_TENSE = 6
NUMBER = "number"
SINGULAR = 7
PLURAL = 8
NORMAL = 9
INFINITIVE = 10
GERUND = 11
IMPERATIVE = 12
BARE_INFINITIVE = 13
SUBJUNCTIVE = 14

DEFAULT_PAST_RULE = regex_rule.RegexRule(ANY_STEM, 0, "ed", 2)
DEFAULT_ING_RULE = regex_rule.RegexRule(ANY_STEM, 0, "ing", 2)
DEFAULT_PP_RULE = regex_rule.RegexRule(ANY_STEM, 0, "ed", 2)
DEFAULT_PRESENT_TENSE = regex_rule.RegexRule(ANY_STEM, 0, "s", 2)

PAST_TENSE_RULES = [
    regex_rule.RegexRule("^(reduce)$", 0, "d", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?[pls]ay$", 1, "id", 1),
    regex_rule.RegexRule(CONS + "y$", 1, "ied", 1),
    regex_rule.RegexRule("^(fling|cling|hang)$", 3, "ung", 0),
    regex_rule.RegexRule("(([sfc][twlp]?r?|w?r)ing)$", 3, "ang", 1),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(bend|spend|send|lend|spend)$", 1,
                         "t", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?lie$", 2, "ay", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(weep|sleep|sweep|creep|keep)$", 2,
                         "pt", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(sell|tell)$", 3, "old", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?do$", 1, "id", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?dig$", 2, "ug", 0),
    regex_rule.RegexRule("^behave$", 0, "d", 0),
    regex_rule.RegexRule("^(have)$", 2, "d", 0),
    regex_rule.RegexRule("(sink|drink)$", 3, "ank", 0),
    regex_rule.RegexRule("^swing$", 3, "ung", 0),
    regex_rule.RegexRule("^be$", 2, "was", 0),
    regex_rule.RegexRule("^outfight$", 4, "ought", 0),
    regex_rule.RegexRule("^tarmac", 0, "ked", 0),
    regex_rule.RegexRule("^abide$", 3, "ode", 0),
    regex_rule.RegexRule("^aby$", 1, "ought", 0),
    regex_rule.RegexRule("^become$", 3, "ame", 0),
    regex_rule.RegexRule("^begird$", 3, "irt", 0),
    regex_rule.RegexRule("^outlie$", 2, "ay", 0),
    regex_rule.RegexRule("^rebind$", 3, "ound", 0),
    regex_rule.RegexRule("^shit$", 3, "hat", 0),
    regex_rule.RegexRule("^bereave$", 4, "eft", 0),
    regex_rule.RegexRule("^foreswear$", 3, "ore", 0),
    regex_rule.RegexRule("^bename$", 3, "empt", 0),
    regex_rule.RegexRule("^beseech$", 4, "ought", 0),
    regex_rule.RegexRule("^bethink$", 3, "ought", 0),
    regex_rule.RegexRule("^bleed$", 4, "led", 0),
    regex_rule.RegexRule("^bog-down$", 5, "ged-down", 0),
    regex_rule.RegexRule("^buy$", 2, "ought", 0),
    regex_rule.RegexRule("^bind$", 3, "ound", 0),
    regex_rule.RegexRule("^(.*)feed$", 4, "fed", 0),
    regex_rule.RegexRule("^breed$", 4, "red", 0),
    regex_rule.RegexRule("^brei$", 2, "eid", 0),
    regex_rule.RegexRule("^bring$", 3, "ought", 0),
    regex_rule.RegexRule("^build$", 3, "ilt", 0),
    regex_rule.RegexRule("^come$", 3, "ame", 0),
    regex_rule.RegexRule("^catch$", 3, "ught", 0),
    regex_rule.RegexRule("^clothe$", 5, "lad", 0),
    regex_rule.RegexRule("^crossbreed$", 4, "red", 0),
    regex_rule.RegexRule("^deal$", 2, "alt", 0),
    regex_rule.RegexRule("^dow$", 1, "ught", 0),
    regex_rule.RegexRule("^dream$", 2, "amt", 0),
    regex_rule.RegexRule("^dwell$", 3, "elt", 0),
    regex_rule.RegexRule("^enwind$", 3, "ound", 0),
    # new Patternrule.Rule("^feed$", 4, "fed", 0),
    regex_rule.RegexRule("^feel$", 3, "elt", 0),
    regex_rule.RegexRule("^flee$", 3, "led", 0),
    regex_rule.RegexRule("^floodlight$", 5, "lit", 0),
    regex_rule.RegexRule("^arise$", 3, "ose", 0),
    regex_rule.RegexRule("^eat$", 3, "ate", 0),
    regex_rule.RegexRule("^awake$", 3, "oke", 0),
    regex_rule.RegexRule("^backbite$", 4, "bit", 0),
    regex_rule.RegexRule("^backslide$", 4, "lid", 0),
    regex_rule.RegexRule("^befall$", 3, "ell", 0),
    regex_rule.RegexRule("^begin$", 3, "gan", 0),
    regex_rule.RegexRule("^beget$", 3, "got", 0),
    regex_rule.RegexRule("^behold$", 3, "eld", 0),
    regex_rule.RegexRule("^bespeak$", 3, "oke", 0),
    regex_rule.RegexRule("^bestride$", 3, "ode", 0),
    regex_rule.RegexRule("^betake$", 3, "ook", 0),
    regex_rule.RegexRule("^bite$", 4, "bit", 0),
    regex_rule.RegexRule("^blow$", 3, "lew", 0),
    regex_rule.RegexRule("^bear$", 3, "ore", 0),
    regex_rule.RegexRule("^break$", 3, "oke", 0),
    regex_rule.RegexRule("^choose$", 4, "ose", 0),
    regex_rule.RegexRule("^cleave$", 4, "ove", 0),
    regex_rule.RegexRule("^countersink$", 3, "ank", 0),
    regex_rule.RegexRule("^drink$", 3, "ank", 0),
    regex_rule.RegexRule("^draw$", 3, "rew", 0),
    regex_rule.RegexRule("^drive$", 3, "ove", 0),
    regex_rule.RegexRule("^fall$", 3, "ell", 0),
    regex_rule.RegexRule("^fly$", 2, "lew", 0),
    regex_rule.RegexRule("^flyblow$", 3, "lew", 0),
    regex_rule.RegexRule("^forbid$", 2, "ade", 0),
    regex_rule.RegexRule("^forbear$", 3, "ore", 0),
    regex_rule.RegexRule("^foreknow$", 3, "new", 0),
    regex_rule.RegexRule("^foresee$", 3, "saw", 0),
    regex_rule.RegexRule("^forespeak$", 3, "oke", 0),
    regex_rule.RegexRule("^forego$", 2, "went", 0),
    regex_rule.RegexRule("^forgive$", 3, "ave", 0),
    regex_rule.RegexRule("^forget$", 3, "got", 0),
    regex_rule.RegexRule("^forsake$", 3, "ook", 0),
    regex_rule.RegexRule("^forspeak$", 3, "oke", 0),
    regex_rule.RegexRule("^forswear$", 3, "ore", 0),
    regex_rule.RegexRule("^forgo$", 2, "went", 0),
    regex_rule.RegexRule("^fight$", 4, "ought", 0),
    regex_rule.RegexRule("^find$", 3, "ound", 0),
    regex_rule.RegexRule("^freeze$", 4, "oze", 0),
    regex_rule.RegexRule("^give$", 3, "ave", 0),
    regex_rule.RegexRule("^geld$", 3, "elt", 0),
    regex_rule.RegexRule("^gen-up$", 3, "ned-up", 0),
    regex_rule.RegexRule("^ghostwrite$", 3, "ote", 0),
    regex_rule.RegexRule("^get$", 3, "got", 0),
    regex_rule.RegexRule("^grow$", 3, "rew", 0),
    regex_rule.RegexRule("^grind$", 3, "ound", 0),
    # new Patternrule.Rule("^handfeed$", 4, "fed", 0),
    regex_rule.RegexRule("^hear$", 2, "ard", 0),
    regex_rule.RegexRule("^hold$", 3, "eld", 0),
    regex_rule.RegexRule("^hide$", 4, "hid", 0),
    regex_rule.RegexRule("^honey$", 2, "ied", 0),
    regex_rule.RegexRule("^inbreed$", 4, "red", 0),
    regex_rule.RegexRule("^indwell$", 3, "elt", 0),
    regex_rule.RegexRule("^interbreed$", 4, "red", 0),
    regex_rule.RegexRule("^interweave$", 4, "ove", 0),
    regex_rule.RegexRule("^inweave$", 4, "ove", 0),
    regex_rule.RegexRule("^ken$", 2, "ent", 0),
    regex_rule.RegexRule("^kneel$", 3, "elt", 0),
    regex_rule.RegexRule("^^know$$", 3, "new", 0),
    regex_rule.RegexRule("^leap$", 2, "apt", 0),
    regex_rule.RegexRule("^learn$", 2, "rnt", 0),
    regex_rule.RegexRule("^lead$", 4, "led", 0),
    regex_rule.RegexRule("^leave$", 4, "eft", 0),
    regex_rule.RegexRule("^light$", 5, "lit", 0),
    regex_rule.RegexRule("^lose$", 3, "ost", 0),
    regex_rule.RegexRule("^make$", 3, "ade", 0),
    regex_rule.RegexRule("^mean$", 2, "ant", 0),
    regex_rule.RegexRule("^meet$", 4, "met", 0),
    regex_rule.RegexRule("^misbecome$", 3, "ame", 0),
    regex_rule.RegexRule("^misdeal$", 2, "alt", 0),
    regex_rule.RegexRule("^misgive$", 3, "ave", 0),
    regex_rule.RegexRule("^mishear$", 2, "ard", 0),
    regex_rule.RegexRule("^mislead$", 4, "led", 0),
    regex_rule.RegexRule("^mistake$", 3, "ook", 0),
    regex_rule.RegexRule("^misunderstand$", 3, "ood", 0),
    regex_rule.RegexRule("^outbreed$", 4, "red", 0),
    regex_rule.RegexRule("^outgrow$", 3, "rew", 0),
    regex_rule.RegexRule("^outride$", 3, "ode", 0),
    regex_rule.RegexRule("^outshine$", 3, "one", 0),
    regex_rule.RegexRule("^outshoot$", 4, "hot", 0),
    regex_rule.RegexRule("^outstand$", 3, "ood", 0),
    regex_rule.RegexRule("^outthink$", 3, "ought", 0),
    regex_rule.RegexRule("^outgo$", 2, "went", 0),
    regex_rule.RegexRule("^outwear$", 3, "ore", 0),
    regex_rule.RegexRule("^overblow$", 3, "lew", 0),
    regex_rule.RegexRule("^overbear$", 3, "ore", 0),
    regex_rule.RegexRule("^overbuild$", 3, "ilt", 0),
    regex_rule.RegexRule("^overcome$", 3, "ame", 0),
    regex_rule.RegexRule("^overdraw$", 3, "rew", 0),
    regex_rule.RegexRule("^overdrive$", 3, "ove", 0),
    regex_rule.RegexRule("^overfly$", 2, "lew", 0),
    regex_rule.RegexRule("^overgrow$", 3, "rew", 0),
    regex_rule.RegexRule("^overhear$", 2, "ard", 0),
    regex_rule.RegexRule("^overpass$", 3, "ast", 0),
    regex_rule.RegexRule("^override$", 3, "ode", 0),
    regex_rule.RegexRule("^oversee$", 3, "saw", 0),
    regex_rule.RegexRule("^overshoot$", 4, "hot", 0),
    regex_rule.RegexRule("^overthrow$", 3, "rew", 0),
    regex_rule.RegexRule("^overtake$", 3, "ook", 0),
    regex_rule.RegexRule("^overwind$", 3, "ound", 0),
    regex_rule.RegexRule("^overwrite$", 3, "ote", 0),
    regex_rule.RegexRule("^partake$", 3, "ook", 0),
    regex_rule.RegexRule("^" + VERBAL_PREFIX + "?run$", 2, "an", 0),
    regex_rule.RegexRule("^ring$", 3, "ang", 0),
    regex_rule.RegexRule("^rebuild$", 3, "ilt", 0),
    regex_rule.RegexRule("^red", 0, "", 0),
    regex_rule.RegexRule("^reave$", 4, "eft", 0),
    regex_rule.RegexRule("^remake$", 3, "ade", 0),
    regex_rule.RegexRule("^resit$", 3, "sat", 0),
    regex_rule.RegexRule("^rethink$", 3, "ought", 0),
    regex_rule.RegexRule("^retake$", 3, "ook", 0),
    regex_rule.RegexRule("^rewind$", 3, "ound", 0),
    regex_rule.RegexRule("^rewrite$", 3, "ote", 0),
    regex_rule.RegexRule("^ride$", 3, "ode", 0),
    regex_rule.RegexRule("^rise$", 3, "ose", 0),
    regex_rule.RegexRule("^reeve$", 4, "ove", 0),
    regex_rule.RegexRule("^sing$", 3, "ang", 0),
    regex_rule.RegexRule("^sink$", 3, "ank", 0),
    regex_rule.RegexRule("^sit$", 3, "sat", 0),
    regex_rule.RegexRule("^see$", 3, "saw", 0),
    regex_rule.RegexRule("^shoe$", 3, "hod", 0),
    regex_rule.RegexRule("^shine$", 3, "one", 0),
    regex_rule.RegexRule("^shake$", 3, "ook", 0),
    regex_rule.RegexRule("^shoot$", 4, "hot", 0),
    regex_rule.RegexRule("^shrink$", 3, "ank", 0),
    regex_rule.RegexRule("^shrive$", 3, "ove", 0),
    regex_rule.RegexRule("^sightsee$", 3, "saw", 0),
    regex_rule.RegexRule("^ski$", 1, "i'd", 0),
    regex_rule.RegexRule("^skydive$", 3, "ove", 0),
    regex_rule.RegexRule("^slay$", 3, "lew", 0),
    regex_rule.RegexRule("^slide$", 4, "lid", 0),
    regex_rule.RegexRule("^slink$", 3, "unk", 0),
    regex_rule.RegexRule("^smite$", 4, "mit", 0),
    regex_rule.RegexRule("^seek$", 3, "ought", 0),
    regex_rule.RegexRule("^spit$", 3, "pat", 0),
    regex_rule.RegexRule("^speed$", 4, "ped", 0),
    regex_rule.RegexRule("^spellbind$", 3, "ound", 0),
    regex_rule.RegexRule("^spoil$", 2, "ilt", 0),
    regex_rule.RegexRule("^speak$", 3, "oke", 0),
    regex_rule.RegexRule("^spotlight$", 5, "lit", 0),
    regex_rule.RegexRule("^spring$", 3, "ang", 0),
    regex_rule.RegexRule("^spin$", 3, "pun", 0),
    regex_rule.RegexRule("^stink$", 3, "ank", 0),
    regex_rule.RegexRule("^steal$", 3, "ole", 0),
    regex_rule.RegexRule("^stand$", 3, "ood", 0),
    regex_rule.RegexRule("^stave$", 3, "ove", 0),
    regex_rule.RegexRule("^stride$", 3, "ode", 0),
    regex_rule.RegexRule("^strive$", 3, "ove", 0),
    regex_rule.RegexRule("^strike$", 3, "uck", 0),
    regex_rule.RegexRule("^stick$", 3, "uck", 0),
    regex_rule.RegexRule("^swim$", 3, "wam", 0),
    regex_rule.RegexRule("^swear$", 3, "ore", 0),
    regex_rule.RegexRule("^teach$", 4, "aught", 0),
    regex_rule.RegexRule("^think$", 3, "ought", 0),
    regex_rule.RegexRule("^throw$", 3, "rew", 0),
    regex_rule.RegexRule("^take$", 3, "ook", 0),
    regex_rule.RegexRule("^tear$", 3, "ore", 0),
    regex_rule.RegexRule("^transship$", 4, "hip", 0),
    regex_rule.RegexRule("^tread$", 4, "rod", 0),
    regex_rule.RegexRule("^typewrite$", 3, "ote", 0),
    regex_rule.RegexRule("^unbind$", 3, "ound", 0),
    regex_rule.RegexRule("^unclothe$", 5, "lad", 0),
    regex_rule.RegexRule("^underbuy$", 2, "ought", 0),
    # new Patternrule.Rule("^underfeed$", 4, "fed", 0),
    regex_rule.RegexRule("^undergird$", 3, "irt", 0),
    regex_rule.RegexRule("^undershoot$", 4, "hot", 0),
    regex_rule.RegexRule("^understand$", 3, "ood", 0),
    regex_rule.RegexRule("^undertake$", 3, "ook", 0),
    regex_rule.RegexRule("^undergo$", 2, "went", 0),
    regex_rule.RegexRule("^underwrite$", 3, "ote", 0),
    regex_rule.RegexRule("^unfreeze$", 4, "oze", 0),
    regex_rule.RegexRule("^unlearn$", 2, "rnt", 0),
    regex_rule.RegexRule("^unmake$", 3, "ade", 0),
    regex_rule.RegexRule("^unreeve$", 4, "ove", 0),
    regex_rule.RegexRule("^unspeak$", 3, "oke", 0),
    regex_rule.RegexRule("^unstick$", 3, "uck", 0),
    regex_rule.RegexRule("^unswear$", 3, "ore", 0),
    regex_rule.RegexRule("^unteach$", 4, "aught", 0),
    regex_rule.RegexRule("^unthink$", 3, "ought", 0),
    regex_rule.RegexRule("^untread$", 4, "rod", 0),
    regex_rule.RegexRule("^unwind$", 3, "ound", 0),
    regex_rule.RegexRule("^upbuild$", 3, "ilt", 0),
    regex_rule.RegexRule("^uphold$", 3, "eld", 0),
    regex_rule.RegexRule("^upheave$", 4, "ove", 0),
    regex_rule.RegexRule("^uprise$", 3, "ose", 0),
    regex_rule.RegexRule("^upspring$", 3, "ang", 0),
    regex_rule.RegexRule("^go$", 2, "went", 0),
    # new Patternrule.Rule("^winterfeed$", 4, "fed", 0),
    regex_rule.RegexRule("^wiredraw$", 3, "rew", 0),
    regex_rule.RegexRule("^withdraw$", 3, "rew", 0),
    regex_rule.RegexRule("^withhold$", 3, "eld", 0),
    regex_rule.RegexRule("^withstand$", 3, "ood", 0),
    regex_rule.RegexRule("^wake$", 3, "oke", 0),
    regex_rule.RegexRule("^win$", 3, "won", 0),
    regex_rule.RegexRule("^wear$", 3, "ore", 0),
    regex_rule.RegexRule("^wind$", 3, "ound", 0),
    regex_rule.RegexRule("^weave$", 4, "ove", 0),
    regex_rule.RegexRule("^write$", 3, "ote", 0),
    regex_rule.RegexRule("^trek$", 1, "cked", 0),
    regex_rule.RegexRule("^ko$", 1, "o'd", 0), regex_rule.RegexRule("^bid", 2, "ade", 0),
    regex_rule.RegexRule("^win$", 2, "on", 0),
    regex_rule.RegexRule("^swim", 2, "am", 0),
    regex_rule.RegexRule("e$", 0, "d", 1),
    regex_rule.RegexRule(
        "^"
        + VERBAL_PREFIX
        + "?(cast|thrust|typeset|cut|bid|upset|wet|bet|cut|"
        + "hit|hurt|inset|let|cost|burst|beat|beset|set|upset|hit|"
        + "offset|put|quit|wed|typeset|wed|spread|split|slit|read|run|shut|shed|lay)$",
        0, "", 0)
]

PRESENT_TENSE_RULES = [
    regex_rule.RegexRule("^aby$", 0, "es", 0),
    regex_rule.RegexRule("^bog-down$", 5, "s-down", 0),
    regex_rule.RegexRule("^chivy$", 1, "vies", 0),
    regex_rule.RegexRule("^gen-up$", 3, "s-up", 0),
    regex_rule.RegexRule("^prologue$", 3, "gs", 0),
    regex_rule.RegexRule("^picknic$", 0, "ks", 0),
    regex_rule.RegexRule("^ko$", 0, "'s", 0),
    regex_rule.RegexRule("[osz]$", 0, "es", 1),
    regex_rule.RegexRule("^have$", 2, "s", 0),
    regex_rule.RegexRule(CONS + "y$", 1, "ies", 1),
    regex_rule.RegexRule("^be$", 2, "is"),
    regex_rule.RegexRule("([zsx]|ch|sh)$", 0, "es", 1)]

PAST_PARTICIPLE_RULES = [regex_rule.RegexRule(CONS + "y$", 1, "ied", 1),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(bring)$", 3, "ought", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX
                                             + "?(take|rise|strew|blow|draw|drive|know|give|sake|"
                                             + "arise|gnaw|grave|grow|hew|know|mow|see|sew|throw|"
                                             + "partake|prove|saw|quartersaw|shake|shew|show|shrive|"
                                             + "sightsee|strew|strive)$", 0, "n", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?[gd]o$", 0, "ne", 1),
                         regex_rule.RegexRule("^(beat|eat|be|fall)$", 0, "en", 0),
                         regex_rule.RegexRule("^(have)$", 2, "d", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?bid$", 0, "den", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?[lps]ay$", 1, "id", 1),
                         regex_rule.RegexRule("^behave$", 0, "d", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?have$", 2, "d", 1),
                         regex_rule.RegexRule("(sink|slink|drink|shrink|stink)$", 3, "unk", 0),
                         regex_rule.RegexRule("(([sfc][twlp]?r?|w?r)ing|hang)$", 3, "ung", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(shear|swear|bear|wear|tear)$", 3,
                                             "orn", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(bend|spend|send|lend)$", 1, "t", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(weep|sleep|sweep|creep|keep$)$",
                                             2, "pt", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(sell|tell)$", 3, "old", 0),
                         regex_rule.RegexRule("^(outfight|beseech)$", 4, "ought", 0),
                         regex_rule.RegexRule("^bethink$", 3, "ought", 0),
                         regex_rule.RegexRule("^buy$", 2, "ought", 0),
                         regex_rule.RegexRule("^aby$", 1, "ought", 0),
                         regex_rule.RegexRule("^tarmac", 0, "ked", 0),
                         regex_rule.RegexRule("^abide$", 3, "ode", 0),
                         regex_rule.RegexRule("^" + VERBAL_PREFIX + "?(speak|(a?)wake|break)$", 3, "oken", 0),
                         regex_rule.RegexRule("^backbite$", 1, "ten", 0),
                         regex_rule.RegexRule("^backslide$", 1, "den", 0),
                         regex_rule.RegexRule("^become$", 3, "ame", 0),
                         regex_rule.RegexRule("^begird$", 3, "irt", 0),
                         regex_rule.RegexRule("^outlie$", 2, "ay", 0),
                         regex_rule.RegexRule("^rebind$", 3, "ound", 0),
                         regex_rule.RegexRule("^relay$", 2, "aid", 0),
                         regex_rule.RegexRule("^shit$", 3, "hat", 0),
                         regex_rule.RegexRule("^bereave$", 4, "eft", 0),
                         regex_rule.RegexRule("^foreswear$", 3, "ore", 0),
                         regex_rule.RegexRule("^overfly$", 1, "own", 0),
                         regex_rule.RegexRule("^beget$", 2, "otten", 0),
                         regex_rule.RegexRule("^begin$", 3, "gun", 0),
                         regex_rule.RegexRule("^bestride$", 1, "den", 0),
                         regex_rule.RegexRule("^bite$", 1, "ten", 0),
                         regex_rule.RegexRule("^bleed$", 4, "led", 0),
                         regex_rule.RegexRule("^bog-down$", 5, "ged-down", 0),
                         regex_rule.RegexRule("^bind$", 3, "ound", 0),
                         regex_rule.RegexRule("^(.*)feed$", 4, "fed", 0),
                         regex_rule.RegexRule("^breed$", 4, "red", 0),
                         regex_rule.RegexRule("^brei", 0, "d", 0),
                         regex_rule.RegexRule("^bring$", 3, "ought", 0),
                         regex_rule.RegexRule("^build$", 1, "t", 0),
                         regex_rule.RegexRule("^come", 0, "", 0),
                         regex_rule.RegexRule("^catch$", 3, "ught", 0),
                         regex_rule.RegexRule("^chivy$", 1, "vied", 0),
                         regex_rule.RegexRule("^choose$", 3, "sen", 0),
                         regex_rule.RegexRule("^cleave$", 4, "oven", 0),
                         regex_rule.RegexRule("^crossbreed$", 4, "red", 0),
                         regex_rule.RegexRule("^deal", 0, "t", 0),
                         regex_rule.RegexRule("^dow$", 1, "ught", 0),
                         regex_rule.RegexRule("^dream", 0, "t", 0),
                         regex_rule.RegexRule("^dig$", 3, "dug", 0),
                         regex_rule.RegexRule("^dwell$", 2, "lt", 0),
                         regex_rule.RegexRule("^enwind$", 3, "ound", 0),
                         # new Patternrule.Rule("^feed$", 4, "fed", 0),
                        regex_rule.RegexRule("^feel$", 3, "elt", 0),
                         regex_rule.RegexRule("^flee$", 2, "ed", 0),
                         regex_rule.RegexRule("^floodlight$", 5, "lit", 0),
                         regex_rule.RegexRule("^fly$", 1, "own", 0),
                         regex_rule.RegexRule("^forbear$", 3, "orne", 0),
                         regex_rule.RegexRule("^forerun$", 3, "ran", 0),
                         regex_rule.RegexRule("^forget$", 2, "otten", 0),
                         regex_rule.RegexRule("^fight$", 4, "ought", 0),
                         regex_rule.RegexRule("^find$", 3, "ound", 0),
                         regex_rule.RegexRule("^freeze$", 4, "ozen", 0),
                         regex_rule.RegexRule("^gainsay$", 2, "aid", 0),
                         regex_rule.RegexRule("^gin$", 3, "gan", 0),
                         regex_rule.RegexRule("^gen-up$", 3, "ned-up", 0),
                         regex_rule.RegexRule("^ghostwrite$", 1, "ten", 0),
                         regex_rule.RegexRule("^get$", 2, "otten", 0),
                         regex_rule.RegexRule("^go$", 0, "ne", 0),
                         regex_rule.RegexRule("^grind$", 3, "ound", 0),
                         regex_rule.RegexRule("^hacksaw", 0, "n", 0),
                         # new Patternrule.Rule("^handfeed$", 4, "fed", 0),
                        regex_rule.RegexRule("^hear", 0, "d", 0),
                         regex_rule.RegexRule("^hold$", 3, "eld", 0),
                         regex_rule.RegexRule("^hide$", 1, "den", 0),
                         regex_rule.RegexRule("^honey$", 2, "ied", 0),
                         regex_rule.RegexRule("^inbreed$", 4, "red", 0),
                         regex_rule.RegexRule("^indwell$", 3, "elt", 0),
                         regex_rule.RegexRule("^interbreed$", 4, "red", 0),
                         regex_rule.RegexRule("^interweave$", 4, "oven", 0),
                         regex_rule.RegexRule("^inweave$", 4, "oven", 0),
                         regex_rule.RegexRule("^ken$", 2, "ent", 0),
                         regex_rule.RegexRule("^kneel$", 3, "elt", 0),
                         regex_rule.RegexRule("^lie$", 2, "ain", 0),
                         regex_rule.RegexRule("^leap$", 0, "t", 0),
                         regex_rule.RegexRule("^learn$", 0, "t", 0),
                         regex_rule.RegexRule("^lead$", 4, "led", 0),
                         regex_rule.RegexRule("^leave$", 4, "eft", 0),
                         regex_rule.RegexRule("^light$", 5, "lit", 0),
                         regex_rule.RegexRule("^lose$", 3, "ost", 0),
                         regex_rule.RegexRule("^make$", 3, "ade", 0),
                         regex_rule.RegexRule("^mean", 0, "t", 0),
                         regex_rule.RegexRule("^meet$", 4, "met", 0),
                         regex_rule.RegexRule("^misbecome$", 3, "ame", 0),
                         regex_rule.RegexRule("^misdeal$", 2, "alt", 0),
                         regex_rule.RegexRule("^mishear$", 1, "d", 0),
                         regex_rule.RegexRule("^mislead$", 4, "led", 0),
                         regex_rule.RegexRule("^misunderstand$", 3, "ood", 0),
                         regex_rule.RegexRule("^outbreed$", 4, "red", 0),
                         regex_rule.RegexRule("^outrun$", 3, "ran", 0),
                         regex_rule.RegexRule("^outride$", 1, "den", 0),
                         regex_rule.RegexRule("^outshine$", 3, "one", 0),
                         regex_rule.RegexRule("^outshoot$", 4, "hot", 0),
                         regex_rule.RegexRule("^outstand$", 3, "ood", 0),
                         regex_rule.RegexRule("^outthink$", 3, "ought", 0),
                         regex_rule.RegexRule("^outgo$", 2, "went", 0),
                         regex_rule.RegexRule("^overbear$", 3, "orne", 0),
                         regex_rule.RegexRule("^overbuild$", 3, "ilt", 0),
                         regex_rule.RegexRule("^overcome$", 3, "ame", 0),
                         regex_rule.RegexRule("^overfly$", 2, "lew", 0),
                         regex_rule.RegexRule("^overhear$", 2, "ard", 0),
                         regex_rule.RegexRule("^overlie$", 2, "ain", 0),
                         regex_rule.RegexRule("^overrun$", 3, "ran", 0),
                         regex_rule.RegexRule("^override$", 1, "den", 0),
                         regex_rule.RegexRule("^overshoot$", 4, "hot", 0),
                         regex_rule.RegexRule("^overwind$", 3, "ound", 0),
                         regex_rule.RegexRule("^overwrite$", 1, "ten", 0),
                         regex_rule.RegexRule("^rebuild$", 3, "ilt", 0),
                         regex_rule.RegexRule("^red$", 3, "red", 0),
                         regex_rule.RegexRule("^redo$", 1, "one", 0),
                         regex_rule.RegexRule("^remake$", 3, "ade", 0),
                         regex_rule.RegexRule("^run$", 3, "run", 0),
                         regex_rule.RegexRule("^rerun$", 3, "ran", 0),
                         regex_rule.RegexRule("^resit$", 3, "sat", 0),
                         regex_rule.RegexRule("^rethink$", 3, "ought", 0),
                         regex_rule.RegexRule("^rewind$", 3, "ound", 0),
                         regex_rule.RegexRule("^rewrite$", 1, "ten", 0),
                         regex_rule.RegexRule("^ride$", 1, "den", 0),
                         regex_rule.RegexRule("^reeve$", 4, "ove", 0),
                         regex_rule.RegexRule("^sit$", 3, "sat", 0),
                         regex_rule.RegexRule("^shoe$", 3, "hod", 0),
                         regex_rule.RegexRule("^shine$", 3, "one", 0),
                         regex_rule.RegexRule("^shoot$", 4, "hot", 0),
                         regex_rule.RegexRule("^ski$", 1, "i'd", 0),
                         regex_rule.RegexRule("^slide$", 1, "den", 0),
                         regex_rule.RegexRule("^smite$", 1, "ten", 0),
                         regex_rule.RegexRule("^seek$", 3, "ought", 0),
                         regex_rule.RegexRule("^spit$", 3, "pat", 0),
                         regex_rule.RegexRule("^speed$", 4, "ped", 0),
                         regex_rule.RegexRule("^spellbind$", 3, "ound", 0),
                         regex_rule.RegexRule("^spoil$", 2, "ilt", 0),
                         regex_rule.RegexRule("^spotlight$", 5, "lit", 0),
                         regex_rule.RegexRule("^spin$", 3, "pun", 0),
                         regex_rule.RegexRule("^steal$", 3, "olen", 0),
                         regex_rule.RegexRule("^stand$", 3, "ood", 0),
                         regex_rule.RegexRule("^stave$", 3, "ove", 0),
                         regex_rule.RegexRule("^stride$", 1, "den", 0),
                         regex_rule.RegexRule("^strike$", 3, "uck", 0),
                         regex_rule.RegexRule("^stick$", 3, "uck", 0),
                         regex_rule.RegexRule("^swell$", 3, "ollen", 0),
                         regex_rule.RegexRule("^swim$", 3, "wum", 0),
                         regex_rule.RegexRule("^teach$", 4, "aught", 0),
                         regex_rule.RegexRule("^think$", 3, "ought", 0),
                         regex_rule.RegexRule("^tread$", 3, "odden", 0),
                         regex_rule.RegexRule("^typewrite$", 1, "ten", 0),
                         regex_rule.RegexRule("^unbind$", 3, "ound", 0),
                         regex_rule.RegexRule("^underbuy$", 2, "ought", 0),
                         # new Patternrule.Rule("^underfeed$", 4, "fed", 0),
                        regex_rule.RegexRule("^undergird$", 3, "irt", 0),
                         regex_rule.RegexRule("^undergo$", 1, "one", 0),
                         regex_rule.RegexRule("^underlie$", 2, "ain", 0),
                         regex_rule.RegexRule("^undershoot$", 4, "hot", 0),
                         regex_rule.RegexRule("^understand$", 3, "ood", 0),
                         regex_rule.RegexRule("^unfreeze$", 4, "ozen", 0),
                         regex_rule.RegexRule("^unlearn", 0, "t", 0),
                         regex_rule.RegexRule("^unmake$", 3, "ade", 0),
                         regex_rule.RegexRule("^unreeve$", 4, "ove", 0),
                         regex_rule.RegexRule("^unstick$", 3, "uck", 0),
                         regex_rule.RegexRule("^unteach$", 4, "aught", 0),
                         regex_rule.RegexRule("^unthink$", 3, "ought", 0),
                         regex_rule.RegexRule("^untread$", 3, "odden", 0),
                         regex_rule.RegexRule("^unwind$", 3, "ound", 0),
                         regex_rule.RegexRule("^upbuild$", 1, "t", 0),
                         regex_rule.RegexRule("^uphold$", 3, "eld", 0),
                         regex_rule.RegexRule("^upheave$", 4, "ove", 0),
                         regex_rule.RegexRule("^waylay$", 2, "ain", 0),
                         regex_rule.RegexRule("^whipsaw$", 2, "awn", 0),
                         # new Patternrule.Rule("^winterfeed$", 4, "fed", 0),
                        regex_rule.RegexRule("^withhold$", 3, "eld", 0),
                         regex_rule.RegexRule("^withstand$", 3, "ood", 0),
                         regex_rule.RegexRule("^win$", 3, "won", 0),
                         regex_rule.RegexRule("^wind$", 3, "ound", 0),
                         regex_rule.RegexRule("^weave$", 4, "oven", 0),
                         regex_rule.RegexRule("^write$", 1, "ten", 0),
                         regex_rule.RegexRule("^trek$", 1, "cked", 0),
                         regex_rule.RegexRule("^ko$", 1, "o'd", 0),
                         regex_rule.RegexRule("^win$", 2, "on", 0),
                         regex_rule.RegexRule("e$", 0, "d", 1),  # DH
                        regex_rule.RegexRule(
                            "^"
                            + VERBAL_PREFIX
                            + "?(cast|thrust|typeset|cut|bid|upset|wet|bet|cut|"
                            + "hit|hurt|inset|let|cost|burst|beat|beset|set|upset|hit|"
                            + "offset|put|quit|wed|typeset|wed|spread|split|slit|read|run|shut|shed)$",
                            0, "", 0)
                         ]

ING_FORM_RULES = [
    regex_rule.RegexRule(CONS + "ie$", 2, "ying", 1),
    regex_rule.RegexRule("[^ie]e$", 1, "ing", 1),
    regex_rule.RegexRule("^bog-down$", 5, "ging-down", 0),
    regex_rule.RegexRule("^chivy$", 1, "vying", 0),
    regex_rule.RegexRule("^gen-up$", 3, "ning-up", 0),
    regex_rule.RegexRule("^trek$", 1, "cking", 0),
    regex_rule.RegexRule("^ko$", 0, "'ing", 0),
    regex_rule.RegexRule("^(age|be)$", 0, "ing", 0),
    regex_rule.RegexRule("(ibe)$", 1, "ing", 0)
]

RULE_MAP = {
    PAST_TENSE_RULE: rule.Rule("PAST_TENSE", DEFAULT_PAST_RULE, PAST_TENSE_RULES),
    PRESENT_TENSERULE: rule.Rule("PRESENT_TENSE", DEFAULT_PRESENT_TENSE, PRESENT_TENSE_RULES),
    PAST_PARTICIPLE_RULE: rule.Rule("PAST_PARTICIPLE", DEFAULT_PP_RULE, PAST_PARTICIPLE_RULES),
    PRESENT_PARTICIPLE_RULE: rule.Rule("ING_FORM", DEFAULT_ING_RULE, ING_FORM_RULES)
}

AUXILIARIES = ["do", "have", "be"]

VERB_CONS_DOUBLING = ["abat", "abet",
                      "abhor", "abut", "accur", "acquit", "adlib", "admit", "aerobat",
                      "aerosol", "agendaset", "allot", "alot", "anagram", "annul", "appal",
                      "apparel", "armbar", "aver", "babysit", "airdrop", "appal", "blackleg",
                      "bobsled", "bur", "chum", "confab", "counterplot", "curet", "dib",
                      "backdrop", "backfil", "backflip", "backlog", "backpedal", "backslap",
                      "backstab", "bag", "balfun", "ballot", "ban", "bar", "barbel", "bareleg",
                      "barrel", "bat", "bayonet", "becom", "bed", "bedevil", "bedwet",
                      "beenhop", "befit", "befog", "beg", "beget", "begin", "bejewel",
                      "bemedal", "benefit", "benum", "beset", "besot", "bestir", "bet",
                      "betassel", "bevel", "bewig", "bib", "bid", "billet", "bin", "bip",
                      "bit", "bitmap", "blab", "blag", "blam", "blan", "blat", "bles", "blim",
                      "blip", "blob", "bloodlet", "blot", "blub", "blur", "bob", "bodypop",
                      "bog", "booby-trap", "boobytrap", "booksel", "bootleg", "bop", "bot",
                      "bowel", "bracket", "brag", "brig", "brim", "bud", "buffet", "bug",
                      "bullshit", "bum", "bun", "bus", "but", "cab", "cabal", "cam", "can",
                      "cancel", "cap", "caracol", "caravan", "carburet", "carnap", "carol",
                      "carpetbag", "castanet", "cat", "catcal", "catnap", "cavil", "chan",
                      "chanel", "channel", "chap", "char", "chargecap", "chat", "chin", "chip",
                      "chir", "chirrup", "chisel", "chop", "chug", "chur", "clam", "clap",
                      "clearcut", "clip", "clodhop", "clog", "clop", "closet", "clot", "club",
                      "co-occur", "co-program", "co-refer", "co-run", "co-star", "cob",
                      "cobweb", "cod", "coif", "com", "combat", "comit", "commit", "compel",
                      "con", "concur", "confer", "confiscat", "control", "cop", "coquet",
                      "coral", "corbel", "corral", "cosset", "cotransmit", "councel",
                      "council", "counsel", "court-martial", "crab", "cram", "crap", "crib",
                      "crop", "crossleg", "cub", "cudgel", "cum", "cun", "cup", "cut", "dab",
                      "dag", "dam", "dan", "dap", "daysit", "de-control", "de-gazet", "de-hul",
                      "de-instal", "de-mob", "de-program", "de-rig", "de-skil", "deadpan",
                      "debag", "debar", "debug", "decommit", "decontrol", "defer", "defog",
                      "deg", "degas", "deinstal", "demit", "demob", "demur", "den", "denet",
                      "depig", "depip", "depit", "der", "deskil", "deter", "devil", "diagram",
                      "dial", "dig", "dim", "din", "dip", "disbar", "disbud", "discomfit",
                      "disembed", "disembowel", "dishevel", "disinter", "dispel", "disprefer",
                      "distil", "dog", "dognap", "don", "doorstep", "dot", "dowel", "drag",
                      "drat", "driftnet", "distil", "egotrip", "enrol", "enthral", "extol",
                      "fulfil", "gaffe", "golliwog", "idyl", "inspan", "drip", "drivel",
                      "drop", "drub", "drug", "drum", "dub", "duel", "dun", "dybbuk", "earwig",
                      "eavesdrop", "ecolabel", "eitherspigot", "electroblot", "embed", "emit",
                      "empanel", "enamel", "endlabel", "endtrim", "enrol", "enthral",
                      "entrammel", "entrap", "enwrap", "equal", "equip", "estop", "exaggerat",
                      "excel", "expel", "extol", "fag", "fan", "farewel", "fat", "featherbed",
                      "feget", "fet", "fib", "fig", "fin", "fingerspel", "fingertip", "fit",
                      "flab", "flag", "flap", "flip", "flit", "flog", "flop", "fob", "focus",
                      "fog", "footbal", "footslog", "fop", "forbid", "forget", "format",
                      "fortunetel", "fot", "foxtrot", "frag", "freefal", "fret", "frig",
                      "frip", "frog", "frug", "fuel", "fufil", "fulfil", "fullyfit", "fun",
                      "funnel", "fur", "furpul", "gab", "gad", "gag", "gam", "gambol", "gap",
                      "garot", "garrot", "gas", "gat", "gel", "gen", "get", "giftwrap", "gig",
                      "gimbal", "gin", "glam", "glenden", "glendin", "globetrot", "glug",
                      "glut", "gob", "goldpan", "goostep", "gossip", "grab", "gravel", "grid",
                      "grin", "grip", "grit", "groundhop", "grovel", "grub", "gum", "gun",
                      "gunrun", "gut", "gyp", "haircut", "ham", "han", "handbag", "handicap",
                      "handknit", "handset", "hap", "hareleg", "hat", "headbut", "hedgehop",
                      "hem", "hen", "hiccup", "highwal", "hip", "hit", "hobnob", "hog", "hop",
                      "horsewhip", "hostel", "hot", "hotdog", "hovel", "hug", "hum", "humbug",
                      "hup", "hushkit", "hut", "illfit", "imbed", "immunblot", "immunoblot",
                      "impannel", "impel", "imperil", "incur", "infer", "infil", "inflam",
                      "initial", "input", "inset", "instil", "inter", "interbed", "intercrop",
                      "intercut", "interfer", "instal", "instil", "intermit", "japan", "jug",
                      "kris", "manumit", "mishit", "mousse", "mud", "interwar", "jab", "jag",
                      "jam", "jar", "jawdrop", "jet", "jetlag", "jewel", "jib", "jig",
                      "jitterbug", "job", "jog", "jog-trot", "jot", "jut", "ken", "kennel",
                      "kid", "kidnap", "kip", "kissogram", "kit", "knap", "kneecap", "knit",
                      "knob", "knot", "kor", "label", "lag", "lam", "lap", "lavel", "leafcut",
                      "leapfrog", "leg", "lem", "lep", "let", "level", "libel", "lid", "lig",
                      "lip", "lob", "log", "lok", "lollop", "longleg", "lop", "lowbal", "lug",
                      "mackerel", "mahom", "man", "map", "mar", "marshal", "marvel", "mat",
                      "matchwin", "metal", "micro-program", "microplan", "microprogram",
                      "milksop", "mis-cal", "mis-club", "mis-spel", "miscal", "mishit",
                      "mislabel", "mit", "mob", "mod", "model", "mohmam", "monogram", "mop",
                      "mothbal", "mug", "multilevel", "mum", "nab", "nag", "nan", "nap", "net",
                      "nightclub", "nightsit", "nip", "nod", "nonplus", "norkop", "nostril",
                      "not", "nut", "nutmeg", "occur", "ocur", "offput", "offset", "omit",
                      "ommit", "onlap", "out-general", "out-gun", "out-jab", "out-plan",
                      "out-pol", "out-pul", "out-put", "out-run", "out-sel", "outbid",
                      "outcrop", "outfit", "outgas", "outgun", "outhit", "outjab", "outpol",
                      "output", "outrun", "outship", "outshop", "outsin", "outstrip",
                      "outswel", "outspan", "overcrop", "pettifog", "photostat", "pouf",
                      "preset", "prim", "pug", "ret", "rosin", "outwit", "over-commit",
                      "over-control", "over-fil", "over-fit", "over-lap", "over-model",
                      "over-pedal", "over-pet", "over-run", "over-sel", "over-step",
                      "over-tip", "over-top", "overbid", "overcal", "overcommit",
                      "overcontrol", "overcrap", "overdub", "overfil", "overhat", "overhit",
                      "overlap", "overman", "overplot", "overrun", "overshop", "overstep",
                      "overtip", "overtop", "overwet", "overwil", "pad", "paintbal", "pan",
                      "panel", "paperclip", "par", "parallel", "parcel", "partiescal", "pat",
                      "patrol", "pedal", "peewit", "peg", "pen", "pencil", "pep", "permit",
                      "pet", "petal", "photoset", "phototypeset", "phut", "picket", "pig",
                      "pilot", "pin", "pinbal", "pip", "pipefit", "pipet", "pit", "plan",
                      "plit", "plod", "plop", "plot", "plug", "plumet", "plummet", "pod",
                      "policyset", "polyfil", "ponytrek", "pop", "pot", "pram", "prebag",
                      "predistil", "predril", "prefer", "prefil", "preinstal", "prep",
                      "preplan", "preprogram", "prizewin", "prod", "profer", "prog", "program",
                      "prop", "propel", "pub", "pummel", "pun", "pup", "pushfit", "put",
                      "quarel", "quarrel", "quickskim", "quickstep", "quickwit", "quip",
                      "quit", "quivertip", "quiz", "rabbit", "rabit", "radiolabel", "rag",
                      "ram", "ramrod", "rap", "rat", "ratecap", "ravel", "re-admit", "re-cal",
                      "re-cap", "re-channel", "re-dig", "re-dril", "re-emit", "re-fil",
                      "re-fit", "re-flag", "re-format", "re-fret", "re-hab", "re-instal",
                      "re-inter", "re-lap", "re-let", "re-map", "re-metal", "re-model",
                      "re-pastel", "re-plan", "re-plot", "re-plug", "re-pot", "re-program",
                      "re-refer", "re-rig", "re-rol", "re-run", "re-sel", "re-set", "re-skin",
                      "re-stal", "re-submit", "re-tel", "re-top", "re-transmit", "re-trim",
                      "re-wrap", "readmit", "reallot", "rebel", "rebid", "rebin", "rebut",
                      "recap", "rechannel", "recommit", "recrop", "recur", "recut", "red",
                      "redril", "refer", "refit", "reformat", "refret", "refuel", "reget",
                      "regret", "reinter", "rejig", "rekit", "reknot", "relabel", "relet",
                      "rem", "remap", "remetal", "remit", "remodel", "reoccur", "rep", "repel",
                      "repin", "replan", "replot", "repol", "repot", "reprogram", "rerun",
                      "reset", "resignal", "resit", "reskil", "resubmit", "retransfer",
                      "retransmit", "retro-fit", "retrofit", "rev", "revel", "revet", "rewrap",
                      "rib", "richochet", "ricochet", "rid", "rig", "rim", "ringlet", "rip",
                      "rit", "rival", "rivet", "roadrun", "rob", "rocket", "rod", "roset",
                      "rot", "rowel", "rub", "run", "runnel", "rut", "sab", "sad", "sag",
                      "sandbag", "sap", "scab", "scalpel", "scam", "scan", "scar", "scat",
                      "schlep", "scrag", "scram", "shall", "sled", "smut", "stet", "sulfuret",
                      "trepan", "unrip", "unstop", "whir", "whop", "wig", "scrap", "scrat",
                      "scrub", "scrum", "scud", "scum", "scur", "semi-control", "semi-skil",
                      "semi-skim", "semiskil", "sentinel", "set", "shag", "sham", "shed",
                      "shim", "shin", "ship", "shir", "shit", "shlap", "shop", "shopfit",
                      "shortfal", "shot", "shovel", "shred", "shrinkwrap", "shrivel", "shrug",
                      "shun", "shut", "side-step", "sideslip", "sidestep", "signal", "sin",
                      "sinbin", "sip", "sit", "skid", "skim", "skin", "skip", "skir", "skrag",
                      "slab", "slag", "slam", "slap", "slim", "slip", "slit", "slob", "slog",
                      "slop", "slot", "slowclap", "slug", "slum", "slur", "smit", "snag",
                      "snap", "snip", "snivel", "snog", "snorkel", "snowcem", "snub", "snug",
                      "sob", "sod", "softpedal", "son", "sop", "spam", "span", "spar", "spat",
                      "spiderweb", "spin", "spiral", "spit", "splat", "split", "spot", "sprag",
                      "spraygun", "sprig", "springtip", "spud", "spur", "squat", "squirrel",
                      "stab", "stag", "star", "stem", "sten", "stencil", "step", "stir",
                      "stop", "storytel", "strap", "strim", "strip", "strop", "strug", "strum",
                      "strut", "stub", "stud", "stun", "sub", "subcrop", "sublet", "submit",
                      "subset", "suedetrim", "sum", "summit", "sun", "suntan", "sup",
                      "super-chil", "superad", "swab", "swag", "swan", "swap", "swat", "swig",
                      "swim", "swivel", "swot", "tab", "tag", "tan", "tansfer", "tap", "tar",
                      "tassel", "tat", "tefer", "teleshop", "tendril", "terschel", "th'strip",
                      "thermal", "thermostat", "thin", "throb", "thrum", "thud", "thug",
                      "tightlip", "tin", "tinsel", "tip", "tittup", "toecap", "tog", "tom",
                      "tomorrow", "top", "tot", "total", "towel", "traget", "trainspot",
                      "tram", "trammel", "transfer", "tranship", "transit", "transmit",
                      "transship", "trap", "travel", "trek", "trendset", "trim", "trip",
                      "tripod", "trod", "trog", "trot", "trousseaushop", "trowel", "trup",
                      "tub", "tug", "tunnel", "tup", "tut", "twat", "twig", "twin", "twit",
                      "typeset", "tyset", "un-man", "unban", "unbar", "unbob", "uncap",
                      "unclip", "uncompel", "undam", "under-bil", "under-cut", "under-fit",
                      "under-pin", "under-skil", "underbid", "undercut", "underlet",
                      "underman", "underpin", "unfit", "unfulfil", "unknot", "unlip",
                      "unlywil", "unman", "unpad", "unpeg", "unpin", "unplug", "unravel",
                      "unrol", "unscrol", "unsnap", "unstal", "unstep", "unstir", "untap",
                      "unwrap", "unzip", "up", "upset", "upskil", "upwel", "ven", "verbal",
                      "vet", "victual", "vignet", "wad", "wag", "wainscot", "wan", "war",
                      "water-log", "waterfal", "waterfil", "waterlog", "weasel", "web", "wed",
                      "wet", "wham", "whet", "whip", "whir", "whiteskin", "whiz", "whup",
                      "wildcat", "win", "windmil", "wit", "woodchop", "woodcut", "wor",
                      "worship", "wrap", "wiretap", "yen", "yak", "yap", "yarnspin", "yip",
                      "yodel", "zag", "zap", "zig", "zig-zag", "zigzag", "zip", "ztrip",
                      "hand-bag", "hocus", "hocus-pocus"]

MODALS = ["shall", "would", "may",
          "might", "ought", "should"]

SYMBOLS = ["!", "?", "$", "%", "*",
           "+", "-", "="]


def check_verb(verb):
    verb2 = verb.lower()
    if verb2 is "am" or verb2 is "are" or verb2 is "is" or verb2 is "was" or verb2 is "were":
        verb2 = "be"
    return verb2


def get_base_form(verb, particle=None):
    if particle is None:
        return verb
    else:
        return verb + " " + particle


def get_present(verb, person, number):
    if person is THIRD_PERSON and number is SINGULAR:
        return apply(RULE_MAP[PRESENT_TENSERULE], verb)
    elif verb.lower() == "be":
        if number is SINGULAR:
            if person is FIRST_PERSON:
                return get_base_form("am")
            elif person is SECOND_PERSON:
                return get_base_form("are")
            elif person is THIRD_PERSON:
                return get_base_form("is")
            else:
                return ""
        else:
            return get_base_form("are")
    else:
        return get_base_form(verb)


def get_past(verb, person, number):
    if verb.lower() == "be":
        if number is SINGULAR:
            if person is THIRD_PERSON:
                return get_base_form("was")
            elif person is SECOND_PERSON:
                return get_base_form("were")
        elif number is PLURAL:
            return get_base_form("were")

    return apply(RULE_MAP[PAST_TENSE_RULE], verb)


def get_present_participle(verb):
    return apply(RULE_MAP[PRESENT_PARTICIPLE_RULE], verb)


def get_past_participle(verb):
    return apply(RULE_MAP[PAST_PARTICIPLE_RULE], verb)


def get_verb_form(verb, tense, person, number):
    if tense is PRESENT_TENSE:
        return get_present(verb, person, number)
    elif tense is PAST_TENSE:
        return get_past(verb, person, number)
    else:
        get_base_form(verb)


def double_final_consonant(word):
    return word + word[len(word) - 1]


def apply(rule, verb):
    base_form = get_base_form(verb)
    result = None

    if base_form in MODALS:
        return base_form

    for x in rule.rules:
        if x.applies(base_form):
            result = x.fire(base_form)
            break

    if result is None and rule.default_rule is not None:
        if rule.doubling and verb in VERB_CONS_DOUBLING:
            base_form = double_final_consonant(base_form)

        result = rule.default_rule.fire(base_form)

    return result


def conjugate(verb, number=SINGULAR, person=THIRD_PERSON, tense=PRESENT_TENSE, modal=None,
              form=NORMAL, passive=False, progressive=False, perfect=False, interrogative=False):
    conjugate_stack = []
    modal_past = False
    actual_modal = None

    if form is INFINITIVE:
        actual_modal = "to"
    elif tense is FUTURE_TENSE and modal is None:
        actual_modal = "will"
    elif modal is not None:
        actual_modal = modal
        if tense is PAST_TENSE:
            modal_past = True

    front_VG = check_verb(verb)

    if passive:
        conjugate_stack.insert(0, get_past_participle(front_VG))
        front_VG = "be"

    if progressive:
        conjugate_stack.insert(0, get_present_participle(front_VG))
        front_VG = "be"

    if perfect or modal_past:
        if tense is PRESENT_TENSE:
            conjugate_stack.insert(0, get_present_participle(front_VG))
        else:
            conjugate_stack.insert(0, get_past_participle(front_VG))
        front_VG = "have"

    if actual_modal is not None:
        conjugate_stack.insert(0, get_base_form(front_VG))
        front_VG = None

    if front_VG is not None:
        if form is GERUND:
            conjugate_stack.insert(0, get_present_participle(front_VG))
        elif interrogative and front_VG is not "be" and len(conjugate_stack) == 0:
            conjugate_stack.insert(0, get_base_form(front_VG))
        else:
            conjugate_stack.insert(0, get_verb_form(get_base_form(front_VG), tense, person, number))

    if actual_modal is not None:
        conjugate_stack.insert(0, actual_modal)

    return " ".join(conjugate_stack).strip()

def is_plural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural