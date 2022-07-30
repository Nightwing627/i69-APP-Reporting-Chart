from typing import Optional

GENDER_CHOICE__MAP = {
    0: 'Male', 1: 'Female'
}

def get_gender_from_code(id: int) -> Optional[str]:
    try:
        return GENDER_CHOICE__MAP[id]
    except Exception:
        return None


AGE_RANGE = (
    (0,"18"),
    (1,"19"),
    (2,"20"),
    (3,"21"),
    (4,"22"),
    (5,"23"),
    (6,"24"),
    (7,"25"),
    (8,"26"),
    (9,"27"),
    (10,"28"),
    (11,"29"),
    (12,"30"),
    (13,"31"),
    (14,"32"),
    (15,"33"),
    (16,"34"),
    (17,"35"),
    (18,"36"),
    (19,"37"),
    (20,"38"),
    (21,"39"),
    (22,"40"),
    (23,"41"),
    (24,"42"),
    (25,"43"),
    (26,"44"),
    (27,"45"),
    (28,"46"),
    (29,"47"),
    (30,"48"),
    (31,"49"),
    (32,"50"),
    (33,"51"),
    (34,"52"),
    (35,"53"),
    (36,"54"),
    (37,"55"),
    (38,"56"),
    (39,"57"),
    (40,"58"),
    (41,"59"),
)

ETHINICITY_TYPE = (
    (0,"American Indian"),
    (1,"Black/ African Descent"),
    (2,"East Asian"),
    (3,"Hispanic / Latino"),
    (4,"Middle Eastern"),
    (5,"Pacific Islander"),
    (6,"South Asian"),
    (7,"White / Caucasian"),
    (8,"Other"),
    (9,"Prefer Not to Say"),
    (10,"Amérindien"),
    (11,"Noir / Afro Descendant"),
    (12,"Asie de L'Est"),
    (13,"Hispanique / latino"),
    (14,"Moyen-Orient"),
    (15,"Insulaire du Pacifique"),
    (16,"Sud-Asiatique"),
    (17,"Blanc / Caucasien"),
    (18,"Autre"),
    (19,"Je préfère ne rien dire"),
)

FAMILY_CHOICE = (
    (0,"Don’t want kids"),
    (1,"Want kids"),
    (2,"Open to kids"),
    (3,"Have kids"),
    (4,"Prefer not to say"),
    (5,"Je ne veux pas d'enfants"),
    (6,"Je veux des enfants"),
    (7,"Ouvert aux enfants"),
    (8,"J'ai des enfants"),
    (9,"Je préfère ne rien dire"),
)

POLITICS_CHOICE = (
    (0,"Liberal"),
    (1,"Liberal"),
    (2,"Conservative"),
    (3,"Other"),
    (4,"Prefer Not to Say"),
    (5,"Libéral"),
    (6,"Modéré"),
    (7,"Conservateur"),
    (8,"Autre"),
    (9,"Je préfère ne rien dire"),
)

RELIGIOUS_CHOICE = (
    (0,"Agnostic"),
    (1,"Atheist"),
    (2,"Buddhist"),
    (3,"Catholic"),
    (4,"Christian"),
    (5,"Hindu"),
    (6,"Jewish"),
    (7,"Muslim"),
    (8,"Spiritual"),
    (9,"Other"),
    (10,"Prefer Not to Say"),
    (10,"Agnostique"),
    (11,"Athée"),
    (12,"Bouddhiste"),
    (13,"Catholique"),
    (14,"Chrétien"),
    (15,"Hindou"),
    (16,"Juif"),
    (17,"Musulman"),
    (18,"Spirituel"),
    (19,"Autre"),
    (20,"Je préfère ne rien dire"),
)
