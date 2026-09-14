from PyWSGIRef import *

__version__ = "1.0.1"
APP_NAME = "PyWSGIREF PROJECT TEMPLATE"

BETA.enable()

addSchablone("main", loadFromFile("./templates/main.pyhtml"))

def main(path: str):
    match path:
        case "/version":
            return __version__
        case "/main":
            return SCHABLONEN["main"].decodedContext(globals())
        case "/stats":
            return STATS.export_stats()
        case "/" | _:
            return "Not found..."
app = makeApplicationObject(main, getStats=True)

if __name__ == "__main__":
    server = setUpServer(app)
    server.serve_forever()