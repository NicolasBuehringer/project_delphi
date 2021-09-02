import os
#from dotenv import load_dotenv
#from os.path import join, dirname

bearer_token = os.environ.get("BEARER_TOKEN")


def get_credentials(bearer_token):

    #dotenv_path = join(dirname(__file__),"..", '.env')

    #dotenv_path = "/Users/nicolas/code/NicolasBuehringer/project_delphi/.env"
    #load_dotenv(dotenv_path)
    # load secret bearer token from .env
    #bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


    # create authorization dict for the api
    headers = {"Authorization": f"Bearer {bearer_token}"}

    return headers

# all queries:
query_cdu = """(@cducsubt OR @CDU OR @ArminLaschet  OR #Laschet OR #ArminLaschet  OR #arminlaschet OR #laschet OR #cdu OR #CDU OR CDU/CSU OR Laschet)
lang:de -is:retweet
-#GRUENEN -@Die_Gruenen -Baerbock -@ABaerbock
-#SPD -@spdde -Scholz -@OlafScholz
-#AFD -@AfD -Weidel -@Alice_Weidel -Chrupalla -@Tino_Chrupalla
-#FDP -@fdp -Lindner -@c_lindner
-#DieLinke -@dieLinke -Wissler -@Janine_Wissler -Bartsch -@DietmarBartsch
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""

query_linke = """(@dieLinke OR @Janine_Wissler OR  @DietmarBartsch OR #DieLinke OR #DieLINKE OR #Linke OR #dielinke OR #Bartsch OR #Wissler OR Wissler OR DieLinke)
lang:de -is:retweet
-@cducsubt -@CDU -@ArminLaschet -#Laschet -#ArminLaschet -#laschet -#cdu -#CDU -CDU/CSU -Laschet
-@Die_Gruenen -@ABaerbock -@GrueneBundestag -#Gruene -#Grünen -#Grüne -#GRUENEN -#AnnalenaBaerbock -#Baerbock -#baerbock -Baerbock -Grüne -Gruene
-@spdde -@OlafScholz -@spdbt -#SPD -#spd -#Spd -#Scholz -#OlafScholz -#SCHOLZ -#scholz -Scholz -SPD
-@AfD -@Alice_Weidel -@Tino_Chrupalla -#AFD -#AfD  -#afd  -#Weidel -#weidel -#Chrupalla -AFD -Weidel -Chrupalla
-@fdp -@fdpbt -@c_lindner -#FDP -#fdp -#Fdp -#Lindner -#lindner -#LINDNER -#ChristianLindner -Lindner -FDP
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""

query_afd = """( @AfD OR @Alice_Weidel OR @Tino_Chrupalla OR #AFD OR #AfD OR #afd OR #AlternativefürDeutschland OR #Weidel OR #weidel OR #AliceWeidel OR #WEIDEL OR #Chrupalla OR #chrupalla OR #TinoChruppala OR AFD OR Weidel OR Chrupalla)
lang:de -is:retweet
-@cducsubt -@CDU -@ArminLaschet -#Laschet -#ArminLaschet -#arminlaschet -#laschet -#cdu -#CDU -CDU/CSU -Laschet
-@Die_Gruenen -@ABaerbock -@GrueneBundestag -#Gruene -#Grünen -#Grüne -#GRUENEN -#AnnalenaBaerbock -#Baerbock -#baerbock -Baerbock -Grüne -Gruene
-@spdde -@OlafScholz -@spdbt -#SPD -#spd -#Spd -#Scholz -#OlafScholz -#SCHOLZ -#scholz -Scholz -SPD -Sozialdemokraten
-#FDP -@fdp -Lindner -@c_lindner
-#DieLinke -@dieLinke -Wissler -@Janine_Wissler -Bartsch -@DietmarBartsch
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""

query_fdp = """(@fdp OR @fdpbt OR @c_lindner OR #FDP OR #fdp OR #Fdp OR #Lindner OR #lindner OR #LINDNER OR #ChristianLindner OR Lindner OR FDP)
lang:de -is:retweet
-@cducsubt -@CDU -@ArminLaschet -#Laschet -#ArminLaschet -#laschet -#cdu -#CDU -CDU/CSU -Laschet
-@Die_Gruenen -@ABaerbock -@GrueneBundestag -#Gruene -#Grünen -#Grüne -#GRUENEN -#AnnalenaBaerbock -#Baerbock -#baerbock -Baerbock -Grüne -Gruene
-@spdde -@OlafScholz -@spdbt -#SPD -#spd -#Spd -#Scholz -#OlafScholz -#SCHOLZ -#scholz -Scholz -SPD
-@AfD -@Alice_Weidel -@Tino_Chrupalla -#AFD -#AfD -#afd -#Weidel -#weidel -#Chrupalla -AFD -Weidel -Chrupalla
-#DieLinke -@dieLinke -Wissler -@Janine_Wissler -Bartsch -@DietmarBartsch
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""

query_others = """(#FreieWaehler OR #FreieWähler OR @HubertAiwanger OR #FREIEWÄHLER OR @FREIEWAEHLER_BV #freiewähler2021 OR #diePARTEI OR @DiePARTEI OR @Tierschutzparte OR NPD OR @Piratenpartei OR #Piraten OR #dieBasis OR @diebasispartei OR #Volt OR @VoltDeutschland OR @oedp_de OR @bgepartei OR @TodenhoeferTeam OR #TeamTodenhoefer)
lang:de -is:retweet"""

query_spd = """( @spdde OR @OlafScholz OR @spdbt OR #SPD OR #spd OR #Spd OR #Scholz OR #OlafScholz OR #SCHOLZ OR #scholz OR Scholz OR SPD OR Sozialdemokraten)
lang:de -is:retweet
-@cducsubt -@CDU -@ArminLaschet -#Laschet -#ArminLaschet -#arminlaschet -#laschet -#cdu -#CDU -CDU/CSU -Laschet
-@Die_Gruenen -@ABaerbock -@GrueneBundestag -#Gruene -#Grünen -#Grüne -#GRUENEN -#AnnalenaBaerbock -#Baerbock -#baerbock -Baerbock -Grüne -Gruene
-#AFD -@AfD -Weidel -@Alice_Weidel -Chrupalla -@Tino_Chrupalla
-#FDP -@fdp -Lindner -@c_lindner
-#DieLinke -@dieLinke -Wissler -@Janine_Wissler -Bartsch -@DietmarBartsch
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""


query_gruene = """( @Die_Gruenen OR @ABaerbock OR @GrueneBundestag OR #Gruene OR #Grünen OR #Grüne OR #GRUENEN OR #AnnalenaBaerbock OR #Baerbock OR #baerbock OR Baerbock OR Grüne OR Gruene)
lang:de -is:retweet
-@cducsubt -@CDU -@ArminLaschet -#Laschet -#ArminLaschet -#arminlaschet -#laschet -#cdu -#CDU -CDU/CSU -Laschet
-#SPD -@spdde -Scholz -@OlafScholz
-#AFD -@AfD -Weidel -@Alice_Weidel -Chrupalla -@Tino_Chrupalla
-#FDP -@fdp -Lindner -@c_lindner
-#DieLinke -@dieLinke -Wissler -@Janine_Wissler -Bartsch -@DietmarBartsch
-#FreieWaehler -@FREIEWAEHLER_BV
-#diePARTEI -@DiePARTEI
-@Tierschutzparte -NPD -@Piratenpartei -#Piraten -#dieBasis -@diebasispartei -#Volt -@VoltDeutschland"""

# create a query dict to iterate over with the party name, its search string and the maximum number of tweets
query_dict = {
    "SPD": (query_spd, 80000),
    "AFD": (query_afd, 60000),
    "CDU": (query_cdu, 80000),
    "FDP": (query_fdp, 60000),
    "GRUENE": (query_gruene, 80000),
    "LINKE": (query_linke, 40000),
    "OTHER": (query_others, 40000)
}
