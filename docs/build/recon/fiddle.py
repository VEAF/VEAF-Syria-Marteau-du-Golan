"""Client minimal du hook dcs-fiddle (VEAF) : exécute du Lua dans DCS et rend le résultat."""
import base64, json, os, sys, urllib.request

TOKEN = os.path.join(os.environ["USERPROFILE"], "dcs-fiddle-token.txt")
USER = sys.argv[3] if len(sys.argv) > 3 else None


def run(lua, env="default", port=12081, user="veaf"):
    pw = open(TOKEN, encoding="utf-8").read().strip()
    path = base64.b64encode(lua.encode()).decode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/{path}?env={env}")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode())
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


if __name__ == "__main__":
    print(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "default"))
