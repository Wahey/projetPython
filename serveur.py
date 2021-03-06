from libs.bottle import route, template, get, post, request, run, static_file
import sqlite3


# Home page
@get('/')
def login():
    return template('tpl/login')

# Access to the search page
@post('/')
def do_login():
    return index()


# Search page and main page
@get('/index')
def index():
    # Connection to the database
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    activite = []
    installation = []
    # Query in the database -> activite table 
    for row in cursor.execute("select nom from activite group by nom"):
        if row not in activite:
            if(row != ""):
                activite.append(row)
    # Query in the database -> installation table
    for row in cursor.execute("select ville from installation group by nom"):
        if row not in installation:
            if(row != ""):
                installation.append(row)
    # Sort results
    activite.sort()
    installation.sort()
    return template('tpl/index', activite=activite, installation=installation)

# Different requests according to the search criteria
def check_requete(activite, installation):
    requete = "select i.adresse, i.ville, e.nom, a.nom, e.lat, e.long from installation i join equipement e on i.numero_instal = e.numero_installation join activite a on a.numero_equipement = e.numero_equipement"
    if(activite == "" and installation != ""):
        requete = "select i.adresse, i.ville, e.nom, a.nom, e.lat, e.long from installation i join equipement e on i.numero_instal = e.numero_installation join activite a on a.numero_equipement = e.numero_equipement where LOWER(i.ville) = LOWER(\""+installation+"\")"
    elif(activite != "" and installation == ""):
        requete = "select i.adresse, i.ville, e.nom, a.nom, e.lat, e.long from installation i join equipement e on i.numero_instal = e.numero_installation join activite a on a.numero_equipement = e.numero_equipement where a.nom LIKE \"%"+activite+"%\""
    elif(activite != "" and installation != ""):
        requete = "select i.adresse, i.ville, e.nom, a.nom, e.lat, e.long from installation i join equipement e on i.numero_instal = e.numero_installation join activite a on a.numero_equipement = e.numero_equipement where LOWER(i.ville) = LOWER(\""+installation+"\") and a.nom LIKE \"%"+activite+"%\""
    return requete

# Access to the result page
@post('/index')
def do_index():
    # Connection to the database
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    resultat = []
    # Run the check_requete method
    requete = check_requete(request.forms.get('activite'), request.forms.get('installation'))
    for row in cursor.execute(requete):
        resultat.append(row)
    return template('tpl/result', resultat=resultat)

# Access to the page with the Google map
@get('/map/<lat>/<long>')
def map(lat, long):
    return template('tpl/map', lat = lat, long = long)

# Method which allows to access to extern files like js or images
@route('/static/<filename>', name='static')
def serve_static(filename):
    return static_file(filename, root="static")

# Port on which the connection is established
run(host='localhost', port=8080)