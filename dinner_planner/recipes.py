from dataclasses import dataclass, field

CATEGORIES = {
    "verdure": "Verdure e Ortaggi",
    "latticini": "Latticini e Uova",
    "legumi": "Legumi",
    "pasta_riso": "Pasta, Riso e Cereali",
    "carne_pesce": "Carne e Pesce",
    "dispensa": "Dispensa",
    "pane": "Pane e Prodotti da Forno",
}


@dataclass
class Ingredient:
    name: str
    quantity: str
    category: str


@dataclass
class Recipe:
    id: str
    name: str
    ingredients: list
    prep_time_min: int
    is_vegetarian: bool
    instructions: list
    servings: int = 2

    @property
    def is_quick(self) -> bool:
        return self.prep_time_min <= 15


def _i(name, qty, cat):
    return Ingredient(name=name, quantity=qty, category=cat)


RECIPES = [
    # ── Quick vegetariane (≤ 15 min) ────────────────────────────────────────
    Recipe(
        id="pasta_pomodoro",
        name="Pasta al pomodoro e basilico",
        prep_time_min=12,
        is_vegetarian=True,
        ingredients=[
            _i("pasta (spaghetti o rigatoni)", "320 g", "pasta_riso"),
            _i("passata di pomodoro", "400 g", "dispensa"),
            _i("aglio", "2 spicchi", "verdure"),
            _i("basilico fresco", "1 mazzetto", "verdure"),
            _i("olio extravergine d'oliva", "4 cucchiai", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
            _i("parmigiano grattugiato", "40 g", "latticini"),
        ],
        instructions=[
            "Porta a bollore abbondante acqua salata e cuoci la pasta al dente.",
            "Nel frattempo, scalda l'olio in padella a fuoco medio e fai dorare l'aglio schiacciato.",
            "Versa la passata, aggiusta di sale e pepe e cuoci 8 minuti.",
            "Scola la pasta, mantecala in padella con il sugo.",
            "Servi con basilico fresco e parmigiano.",
        ],
    ),
    Recipe(
        id="frittata_verdure",
        name="Frittata di verdure miste",
        prep_time_min=12,
        is_vegetarian=True,
        ingredients=[
            _i("uova", "4 pezzi", "latticini"),
            _i("zucchine", "1 piccola", "verdure"),
            _i("peperone rosso", "½", "verdure"),
            _i("cipolla", "½", "verdure"),
            _i("parmigiano grattugiato", "30 g", "latticini"),
            _i("olio extravergine d'oliva", "2 cucchiai", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Taglia le verdure a julienne sottile.",
            "Scalda l'olio in padella antiaderente e salta le verdure 4 minuti.",
            "Sbatti le uova con parmigiano, sale e pepe.",
            "Versa il composto sulle verdure e cuoci 3 minuti per lato a fuoco medio.",
            "Servi tagliata a spicchi.",
        ],
    ),
    Recipe(
        id="insalata_ceci",
        name="Insalata di ceci, pomodori e cetrioli",
        prep_time_min=5,
        is_vegetarian=True,
        ingredients=[
            _i("ceci in scatola", "400 g", "legumi"),
            _i("pomodori ciliegino", "200 g", "verdure"),
            _i("cetriolo", "1", "verdure"),
            _i("cipolla rossa", "½", "verdure"),
            _i("prezzemolo fresco", "1 mazzetto", "verdure"),
            _i("olio extravergine d'oliva", "3 cucchiai", "dispensa"),
            _i("succo di limone", "1 limone", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Scola e sciacqua i ceci.",
            "Taglia pomodori a metà, cetriolo a cubetti, cipolla a rondelle sottili.",
            "Mescola tutto in una ciotola grande.",
            "Condisci con olio, succo di limone, sale, pepe e prezzemolo.",
        ],
    ),
    Recipe(
        id="bruschette_ricotta",
        name="Bruschette con ricotta, pomodori e basilico",
        prep_time_min=10,
        is_vegetarian=True,
        ingredients=[
            _i("pane casereccio", "4 fette spesse", "pane"),
            _i("ricotta fresca", "200 g", "latticini"),
            _i("pomodori", "2", "verdure"),
            _i("basilico fresco", "1 mazzetto", "verdure"),
            _i("olio extravergine d'oliva", "3 cucchiai", "dispensa"),
            _i("aglio", "1 spicchio", "verdure"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Tosta le fette di pane in padella o tostapane.",
            "Strofina ogni fetta con l'aglio tagliato a metà.",
            "Spalma abbondante ricotta su ogni bruschetta.",
            "Taglia i pomodori a cubetti e distribuiscili sopra.",
            "Irrora con olio, aggiungi basilico, sale e pepe.",
        ],
    ),
    Recipe(
        id="pasta_aglio_olio",
        name="Pasta aglio, olio e peperoncino",
        prep_time_min=12,
        is_vegetarian=True,
        ingredients=[
            _i("spaghetti", "320 g", "pasta_riso"),
            _i("aglio", "4 spicchi", "verdure"),
            _i("peperoncino rosso", "1-2", "verdure"),
            _i("prezzemolo fresco", "1 mazzetto", "verdure"),
            _i("olio extravergine d'oliva", "6 cucchiai", "dispensa"),
            _i("sale", "q.b.", "dispensa"),
            _i("parmigiano grattugiato (facoltativo)", "40 g", "latticini"),
        ],
        instructions=[
            "Cuoci gli spaghetti in acqua bollente salata.",
            "Affetta l'aglio e il peperoncino. Falli soffriggere dolcemente nell'olio senza bruciare l'aglio.",
            "Scola la pasta tenendo da parte ½ bicchiere di acqua di cottura.",
            "Manteca la pasta in padella con il soffritto e l'acqua di cottura.",
            "Completa con prezzemolo tritato e, a piacere, parmigiano.",
        ],
    ),
    Recipe(
        id="uova_spinaci",
        name="Uova strapazzate con spinaci e feta",
        prep_time_min=8,
        is_vegetarian=True,
        ingredients=[
            _i("uova", "4 pezzi", "latticini"),
            _i("spinaci freschi", "150 g", "verdure"),
            _i("feta", "80 g", "latticini"),
            _i("burro", "20 g", "latticini"),
            _i("aglio", "1 spicchio", "verdure"),
            _i("sale e pepe", "q.b.", "dispensa"),
            _i("pane tostato", "4 fette", "pane"),
        ],
        instructions=[
            "Scalda il burro in padella, aggiungi l'aglio tritato e cuoci 1 minuto.",
            "Unisci gli spinaci e falli appassire 2 minuti.",
            "Sbatti le uova, versale sugli spinaci e mescola delicatamente a fuoco basso.",
            "Aggiungi la feta sbriciolata, aggiusta di sale e pepe.",
            "Servi sulle fette di pane tostato.",
        ],
    ),
    Recipe(
        id="caprese_pesto",
        name="Caprese con mozzarella e pesto",
        prep_time_min=5,
        is_vegetarian=True,
        ingredients=[
            _i("mozzarella di bufala", "250 g", "latticini"),
            _i("pomodori cuore di bue", "3 grandi", "verdure"),
            _i("pesto al basilico", "3 cucchiai", "dispensa"),
            _i("olio extravergine d'oliva", "2 cucchiai", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
            _i("pane ciabatta", "4 fette", "pane"),
        ],
        instructions=[
            "Taglia mozzarella e pomodori a fette di circa 1 cm.",
            "Disponile alternandole su un piatto da portata.",
            "Aggiungi cucchiaiate di pesto tra le fette.",
            "Irrora con olio, sale e pepe.",
            "Servi con pane ciabatta.",
        ],
    ),
    Recipe(
        id="lenticchie_scatola",
        name="Zuppa rapida di lenticchie al curry",
        prep_time_min=15,
        is_vegetarian=True,
        ingredients=[
            _i("lenticchie in scatola", "400 g", "legumi"),
            _i("pomodori pelati", "200 g", "dispensa"),
            _i("cipolla", "1", "verdure"),
            _i("curry in polvere", "1 cucchiaio", "dispensa"),
            _i("latte di cocco", "200 ml", "dispensa"),
            _i("olio extravergine d'oliva", "2 cucchiai", "dispensa"),
            _i("sale", "q.b.", "dispensa"),
            _i("pane naan o pita", "2 pezzi", "pane"),
        ],
        instructions=[
            "Soffriggi la cipolla tritata nell'olio per 3 minuti.",
            "Aggiungi il curry e cuoci 1 minuto mescolando.",
            "Unisci lenticchie scolate, pomodori pelati e latte di cocco.",
            "Cuoci a fuoco medio per 8 minuti finché si addensa.",
            "Aggiusta di sale e servi con pane naan.",
        ],
    ),
    Recipe(
        id="tacos_fagioli",
        name="Tacos vegetariani con fagioli neri e avocado",
        prep_time_min=15,
        is_vegetarian=True,
        ingredients=[
            _i("tortillas di mais", "4 pezzi", "pane"),
            _i("fagioli neri in scatola", "400 g", "legumi"),
            _i("avocado maturo", "1", "verdure"),
            _i("pomodori ciliegino", "150 g", "verdure"),
            _i("mais in scatola", "80 g", "legumi"),
            _i("lime", "1", "dispensa"),
            _i("coriandolo o prezzemolo", "q.b.", "verdure"),
            _i("paprika affumicata", "1 cucchiaino", "dispensa"),
            _i("sale", "q.b.", "dispensa"),
        ],
        instructions=[
            "Scalda i fagioli con paprika e sale in padella per 5 minuti.",
            "Schiaccia l'avocado con succo di lime e sale.",
            "Taglia i pomodori a metà.",
            "Scalda le tortillas in padella asciutta 30 secondi per lato.",
            "Farcisci ogni tortilla con fagioli, guacamole, mais e pomodori.",
        ],
    ),
    Recipe(
        id="pasta_burro_salvia",
        name="Pasta con burro, salvia e noci",
        prep_time_min=12,
        is_vegetarian=True,
        ingredients=[
            _i("pasta (tagliatelle o pappardelle)", "320 g", "pasta_riso"),
            _i("burro", "60 g", "latticini"),
            _i("salvia fresca", "10 foglie", "verdure"),
            _i("noci tritate", "40 g", "dispensa"),
            _i("parmigiano grattugiato", "50 g", "latticini"),
            _i("sale e pepe nero", "q.b.", "dispensa"),
        ],
        instructions=[
            "Cuoci la pasta in acqua bollente salata.",
            "Fai sciogliere il burro in padella a fuoco medio.",
            "Aggiungi le foglie di salvia e le noci, cuoci 2 minuti.",
            "Scola la pasta e mantecala nel burro aromatizzato.",
            "Servi con abbondante parmigiano e pepe nero.",
        ],
    ),

    # ── Vegetariane elaborate (> 15 min) ────────────────────────────────────
    Recipe(
        id="risotto_funghi",
        name="Risotto ai funghi porcini",
        prep_time_min=30,
        is_vegetarian=True,
        ingredients=[
            _i("riso Carnaroli", "320 g", "pasta_riso"),
            _i("funghi porcini secchi", "30 g", "verdure"),
            _i("funghi champignon freschi", "200 g", "verdure"),
            _i("cipolla", "1", "verdure"),
            _i("vino bianco secco", "100 ml", "dispensa"),
            _i("brodo vegetale", "800 ml", "dispensa"),
            _i("burro", "40 g", "latticini"),
            _i("parmigiano grattugiato", "50 g", "latticini"),
            _i("olio extravergine d'oliva", "2 cucchiai", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
            _i("prezzemolo fresco", "q.b.", "verdure"),
        ],
        instructions=[
            "Ammolla i porcini secchi in acqua tiepida per 20 minuti, poi strizzali.",
            "Scalda il brodo in una pentola separata.",
            "Soffriggi la cipolla nell'olio per 3 minuti, poi aggiunge i funghi e cuoci 5 minuti.",
            "Tosta il riso 2 minuti, sfuma con il vino.",
            "Aggiungi il brodo caldo mestolo per mestolo, mescolando continuamente per 18 minuti.",
            "Spegni il fuoco, manteca con burro e parmigiano. Riposa 2 minuti.",
            "Servi con prezzemolo e pepe nero.",
        ],
    ),
    Recipe(
        id="curry_lenticchie",
        name="Curry di lenticchie rosse con riso basmati",
        prep_time_min=25,
        is_vegetarian=True,
        ingredients=[
            _i("lenticchie rosse decorticate", "200 g", "legumi"),
            _i("riso basmati", "200 g", "pasta_riso"),
            _i("cipolla", "1", "verdure"),
            _i("aglio", "2 spicchi", "verdure"),
            _i("zenzero fresco", "2 cm", "verdure"),
            _i("pomodori pelati", "400 g", "dispensa"),
            _i("latte di cocco", "400 ml", "dispensa"),
            _i("curry in polvere", "2 cucchiai", "dispensa"),
            _i("curcuma", "1 cucchiaino", "dispensa"),
            _i("olio di semi", "2 cucchiai", "dispensa"),
            _i("coriandolo o prezzemolo", "q.b.", "verdure"),
            _i("sale", "q.b.", "dispensa"),
        ],
        instructions=[
            "Cuoci il riso basmati secondo le istruzioni della confezione.",
            "Soffriggi cipolla, aglio e zenzero grattugiato nell'olio per 4 minuti.",
            "Aggiungi curry e curcuma, tosta 1 minuto.",
            "Unisci lenticchie, pomodori pelati e latte di cocco.",
            "Cuoci a fuoco medio-basso per 20 minuti finché le lenticchie sono tenere.",
            "Aggiusta di sale e servi sul riso con coriandolo.",
        ],
    ),
    Recipe(
        id="parmigiana_melanzane",
        name="Parmigiana di melanzane",
        prep_time_min=45,
        is_vegetarian=True,
        ingredients=[
            _i("melanzane", "2 grandi", "verdure"),
            _i("passata di pomodoro", "500 g", "dispensa"),
            _i("mozzarella", "250 g", "latticini"),
            _i("parmigiano grattugiato", "80 g", "latticini"),
            _i("basilico fresco", "1 mazzetto", "verdure"),
            _i("olio extravergine d'oliva", "4 cucchiai", "dispensa"),
            _i("aglio", "2 spicchi", "verdure"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Taglia le melanzane a fette di 5 mm, salale e lascia riposare 15 minuti, poi asciugale.",
            "Griglia o friggi le fette di melanzana finché dorate.",
            "Prepara un sugo veloce: soffriggi aglio, aggiungi passata e cuoci 10 minuti.",
            "In una pirofila, alterna strati di melanzane, sugo, mozzarella e parmigiano.",
            "Cuoci in forno a 200°C per 20 minuti. Lascia intiepidire prima di servire.",
        ],
    ),
    Recipe(
        id="gnocchi_pesto_rucola",
        name="Gnocchi al pesto di rucola e noci",
        prep_time_min=20,
        is_vegetarian=True,
        ingredients=[
            _i("gnocchi freschi", "500 g", "pasta_riso"),
            _i("rucola", "80 g", "verdure"),
            _i("noci", "50 g", "dispensa"),
            _i("parmigiano grattugiato", "40 g", "latticini"),
            _i("olio extravergine d'oliva", "5 cucchiai", "dispensa"),
            _i("aglio", "1 spicchio", "verdure"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Frulla rucola, noci, parmigiano, aglio e olio finché ottieni un pesto cremoso.",
            "Aggiusta di sale.",
            "Cuoci gli gnocchi in acqua bollente salata finché vengono a galla.",
            "Scola tenendo un po' d'acqua di cottura.",
            "Manteca gli gnocchi con il pesto, aggiungendo acqua di cottura se necessario.",
        ],
    ),
    Recipe(
        id="minestrone",
        name="Minestrone di verdure di stagione",
        prep_time_min=35,
        is_vegetarian=True,
        ingredients=[
            _i("patate", "2", "verdure"),
            _i("carote", "2", "verdure"),
            _i("sedano", "2 gambi", "verdure"),
            _i("zucchine", "1", "verdure"),
            _i("fagioli borlotti in scatola", "400 g", "legumi"),
            _i("pomodori pelati", "200 g", "dispensa"),
            _i("cipolla", "1", "verdure"),
            _i("pasta corta o riso", "100 g", "pasta_riso"),
            _i("brodo vegetale", "1 litro", "dispensa"),
            _i("olio extravergine d'oliva", "3 cucchiai", "dispensa"),
            _i("parmigiano grattugiato", "40 g", "latticini"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Taglia tutte le verdure a cubetti regolari.",
            "Soffriggi cipolla e sedano nell'olio per 3 minuti.",
            "Aggiungi carote, patate e zucchine, cuoci altri 3 minuti.",
            "Versa il brodo, i pomodori e i fagioli. Porta a bollore.",
            "Cuoci a fuoco medio per 20 minuti. Aggiungi la pasta e cuoci fino al dente.",
            "Servi con olio a crudo e parmigiano.",
        ],
    ),

    # ── Non vegetariane (max 2/settimana) ────────────────────────────────────
    Recipe(
        id="salmone_limone",
        name="Salmone al limone con verdure grigliate",
        prep_time_min=15,
        is_vegetarian=False,
        ingredients=[
            _i("filetti di salmone", "2 pezzi (ca. 150 g ciascuno)", "carne_pesce"),
            _i("limone", "1", "dispensa"),
            _i("zucchine", "1", "verdure"),
            _i("asparagi", "200 g", "verdure"),
            _i("olio extravergine d'oliva", "3 cucchiai", "dispensa"),
            _i("aglio", "1 spicchio", "verdure"),
            _i("timo fresco", "q.b.", "verdure"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Scalda una padella antiaderente a fuoco alto con 1 cucchiaio d'olio.",
            "Cuoci il salmone 3-4 minuti per lato. Sfuma con succo di limone.",
            "Nella stessa padella, griglia velocemente le verdure tagliate a nastro.",
            "Condisci le verdure con aglio, timo, sale e olio.",
            "Servi il salmone sopra le verdure con zest di limone.",
        ],
    ),
    Recipe(
        id="pollo_limone",
        name="Pollo al limone con rosmarino e patate",
        prep_time_min=30,
        is_vegetarian=False,
        ingredients=[
            _i("petti di pollo", "2 (ca. 150 g ciascuno)", "carne_pesce"),
            _i("patate", "3 medie", "verdure"),
            _i("limone", "1", "dispensa"),
            _i("rosmarino fresco", "2 rametti", "verdure"),
            _i("aglio", "3 spicchi", "verdure"),
            _i("olio extravergine d'oliva", "4 cucchiai", "dispensa"),
            _i("vino bianco secco", "100 ml", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
        ],
        instructions=[
            "Preriscalda il forno a 200°C.",
            "Taglia le patate a spicchi e lessale 5 minuti in acqua bollente.",
            "Disponi il pollo in una pirofila con patate, aglio, rosmarino.",
            "Irrora con olio e vino, aggiungi succo e zest di limone.",
            "Cuoci in forno per 25 minuti finché il pollo è dorato.",
        ],
    ),
    Recipe(
        id="tonno_legumi",
        name="Insalata di tonno, fagioli cannellini e cipolla rossa",
        prep_time_min=8,
        is_vegetarian=False,
        ingredients=[
            _i("tonno al naturale", "2 scatole (80 g ciascuna)", "carne_pesce"),
            _i("fagioli cannellini in scatola", "400 g", "legumi"),
            _i("cipolla rossa", "½", "verdure"),
            _i("sedano", "2 gambi", "verdure"),
            _i("prezzemolo fresco", "q.b.", "verdure"),
            _i("olio extravergine d'oliva", "3 cucchiai", "dispensa"),
            _i("aceto di vino", "1 cucchiaio", "dispensa"),
            _i("sale e pepe", "q.b.", "dispensa"),
            _i("pane casereccio", "4 fette", "pane"),
        ],
        instructions=[
            "Scola e sciacqua i fagioli.",
            "Taglia cipolla rossa a rondelle sottili e sedano a fette.",
            "Sgocciola il tonno e sminuzzalo.",
            "Mescola tutto in una ciotola con olio, aceto, sale e pepe.",
            "Completa con prezzemolo tritato e servi con pane.",
        ],
    ),
]

RECIPE_MAP = {r.id: r for r in RECIPES}
QUICK_VEGETARIAN = [r for r in RECIPES if r.is_vegetarian and r.is_quick]
VEGETARIAN = [r for r in RECIPES if r.is_vegetarian]
NON_VEGETARIAN = [r for r in RECIPES if not r.is_vegetarian]
