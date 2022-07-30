from django.core.management.base import BaseCommand
from defaultPicker.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        default_pickers = {
            "ages": ["18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
                     "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                     "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
            "ethnicity": ["American Indian", "Black/ African Descent", "East Asian", "Hispanic / Latino",
                          "Middle Eastern", "Pacific Islander", "South Asian", "White / Caucasian", "Other",
                          "Prefer Not to Say"],
            "ethnicity_fr": ["Amérindien", "Noir / Afro Descendant", "Asie de L'Est",
                             "Hispanique / latino", "Moyen-Orient", "Insulaire du Pacifique", "Sud-Asiatique",
                             "Blanc / Caucasien", "Autre", "Je préfère ne rien dire"],
            "family": ["Don’t want kids", "Want kids ", "Open to kids", "Have kids", "Prefer not to say"],
            "family_fr": ["Je ne veux pas d'enfants", "Je veux des enfants", "Ouvert aux enfants", "J'ai des enfants",
                          "Je préfère ne rien dire", ],
            "heights": ["140", "143", "146", "148", "151", "153", "156", "158", "161", "163", "166", "168", "171",
                        "173", "176", "179", "181", "184", "186", "189", "191", "194", "196", "199", "201", "204",
                        "207", "209", "212", "214", "217", "219", "222", "224", "227", "229", "232", "234", "237",
                        "240", "242", "245", "247"],
            "politics": ["Liberal", "Moderate", "Conservative", "Other", "Prefer Not to Say"],
            "politics_fr": ["Libéral", "Modéré", "Conservateur", "Autre", "Je préfère ne rien dire"],
            "religious": ["Agnostic", "Atheist", "Buddhist", "Catholic", "Christian", "Hindu", "Jewish", "Muslim",
                          "Spiritual", "Other", "Prefer Not to Say"],
            "religious_fr": ["Agnostique", "Athée", "Bouddhiste", "Catholique",
                             "Chrétien", "Hindou", "Juif", "Musulman", "Spirituel", "Autre", "Je préfère ne rien dire"],
            "searchGenders": ["Only Men", "Only Women", "Both"],
            "tags": ["nature lover", "pet friendly", "sports fanatic", "haute culture", "video gamer", "gambler",
                     "otaku", "foodie", "early bird", "night owl", "musician", "nerd", "book worm", "architect",
                     "logician", "commander", "debater", "advocate", "mediator", "protagonist", "campaigner",
                     "responsible", "defender", "executive", "social butterfly", "virtuoso", "adventurer",
                     "entrepreneur", "entertainer", "mechanic", "nurturer", "artist", "idealist", "scientist",
                     "thinker", "caregiver", "visionary", "creative", "philosopher", "sensitive", "compassionate",
                     "ambitious", "traditional", "comedian", "leader", "traveler", "obnoxious", "arrogant", "impatient",
                     "sarcastic", "nihilist", "hustler", "gangster", "Vilain", "Têtu", "Sensible", "Intelligent",
                     "Agréable", "Émotif", "Fou", "Effronté", "De bonne humeur", "Énergique", "Optimiste", "Bavard",
                     "Calme", "Sincère", "Paresseux", "Timide", "Amical", "Honnête", "Chaleureux", "Égoïste", "Utile",
                     "Enthousiaste", "Travailleur", "Fidèle", "Poli", "HEUREUX", "Romantique", "Diplomatique",
                     "Amoureux de la nature", "Animaux acceptés", "Fanatique de sport", "Joueur de jeu vidéo",
                     "Fin gourmet", "Lève tô", "Noctambule", "Musicien", "Nerd", "BIBLIOPHILE", "Architecte",
                     "Logicien", "Le commandant", "Debater", "Militant", "Responsable", "Défenseur", "Exécutif",
                     "Aventurier", "Entrepreneur", "Artiste", "Nourricier", "Artiste", "Idéaliste"],
            "zodiacSigns": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius",
                            "Capricorn", "Aquarius", "Pisces"],
            "zodiacSigns_fr": ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion",
                               "Vierge", "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"]
        }
        for ethnicity_, ethnicity_fr_ in zip(default_pickers['ethnicity'], default_pickers['ethnicity_fr']):
            ethnicity.objects.get_or_create(
                ethnicity=ethnicity_,
                ethnicity_fr=ethnicity_fr_,
                defaults={
                    "ethnicity": ethnicity_,
                    "ethnicity_fr": ethnicity_fr_
                }
            )

        for family_, family_fr_ in zip(default_pickers['family'], default_pickers['family_fr']):
            family.objects.get_or_create(
                familyPlans=family_,
                familyPlans_fr=family_fr_,
                defaults={
                    "familyPlans": family_,
                    "familyPlans_fr": family_fr_
                }
            )

        for height_ in default_pickers['heights']:
            height.objects.get_or_create(
                height=height_,
                defaults={
                    "height": height_
                }
            )

        for politics_, politics_fr_ in zip(default_pickers['politics'], default_pickers['politics_fr']):
            politics.objects.get_or_create(
                politics=politics_,
                politics_fr=politics_fr_,
                defaults={
                    "politics": politics_,
                    "politics_fr": politics_fr_
                }
            )

        for religious_, religious_fr_ in zip(default_pickers['religious'], default_pickers['religious_fr']):
            religious.objects.get_or_create(
                religious=religious_,
                religious_fr=religious_fr_,
                defaults={
                    "religious": religious_,
                    "religious_fr": religious_fr_
                }
            )

        for tag_ in default_pickers['tags']:
            tag_obj = tags.objects.filter(tag=tag_).first()
            if not tag_obj:
                tag_obj = tags(tag=tag_)
                tag_obj.save()

        for zodiacSign_, zodiacSign_fr_ in zip(default_pickers['zodiacSigns'], default_pickers['zodiacSigns_fr']):
            zodiacSign.objects.get_or_create(
                zodiacSign=zodiacSign_,
                zodiacSign_fr=zodiacSign_fr_,
                defaults={
                    "zodiacSign": zodiacSign_,
                    "zodiacSign_fr": zodiacSign_fr_
                }
            )