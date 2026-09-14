from PyWSGIRef import *
from cgi import FieldStorage

from strings import *

__version__ = "1.0.0"
APP_NAME = "BIRTHDAY APP TEMPLATE"

BETA.enable()

# Load templates
basePath = "./templates/{}.pyhtml"

for i in ["gameSurvey", "evaluateGameSurvey", "viewGameSurvey", "gameSurveyInit", "main"]:
    addSchablone(i, loadFromFile(privateURL.format(i)))

# base function
# i know this is ugly but it works

def saveGameSurvey(form: FieldStorage):
    name = form.getvalue("name")
    id_ = form.getvalue("id")
    try:
        if name+id_ in ["Paul568", "Leander999"]: # send the users their id
            fav = form.getvalue("fav").replace("<", "SIGN_BANNED_BY_DEV#1")
            fur = form.getvalue("msg").replace("<", "SIGN_BANNED_BY_DEV#2")
            can = form.getvalue("can")
            day = form.getvalue("day")
            with open("./gameSurvey.txt", "r", encoding="utf-8") as f:
                c = f.read()
            color = "yellow"
            if day == "ja":
                color = "green"
            if can == "nein":
                color = "red"
            if not name + " <" in c:
                with open("./gameSurvey.txt", "a", encoding="utf-8") as f:
                    f.write(f"<br/><details><summary>{name} <font color='{color}'>●</font></summary><br/>Lieblingsspiel: {fav}<br/>Weiteres: {fur}<br/>Kann kommen: {can}<br/>Bleibt alle Tage: {day}<br/></details>")
                return SCHABLONEN["evaluateGameSurvey"].decoded().format(EVALUATE_GAME_INSERT)
            else:
                return SCHABLONEN["evaluateGameSurvey"].decoded().format(EVALUATE_GAME_INSERT_ERROR.format("Iam interfuisti."))
        else:
            return SCHABLONEN["evaluateGameSurvey"].decoded().format(EVALUATE_GAME_INSERT_ERROR.format("Subscriptio identitatis falsa."))
    except:
        return SCHABLONEN["evaluateGameSurvey"].decoded().format(EVALUATE_GAME_INSERT_ERROR.format("Error."))


def main(path: str):
    match path:
        case "/version":
            return __version__
        case "/main":
            return SCHABLONEN["main"].decodedContext(globals())
        case "/stats":
            return STATS.export_stats()
        case "/gameSurveyInit":
            return SCHABLONEN["gameSurveyInit"].decoded()
        case "/viewGameSurvey":
            with open("./gameSurvey.txt", "r") as f:
                return ipban(SCHABLONEN["viewGameSurvey"].decodedContext(globals()).format(f.read()), "noParents", ip)
        case "/private/evaluateGameSurvey":
            return saveGameSurvey(fs)
        case "/private/gameSurvey":
            return SCHABLONEN["gameSurvey"].decoded()
        case "/" | _:
            return "Not found..."
app = makeApplicationObject(main, getStats=True)

if __name__ == "__main__":
    server = setUpServer(app)
    server.serve_forever()