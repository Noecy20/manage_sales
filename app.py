from flask import Flask, flash, redirect, render_template, request, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from functools import wraps
from datetime import datetime
import random
import string
import pymysql
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from flask_mail import Mail, Message
import plotly.express as px
import pyodbc
import plotly.graph_objects as go
import random
import string

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'allahnoemie43@gmail.com'
app.config['MAIL_PASSWORD'] = 'qslr uchn bodf nqpb'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# ? Les informations pour la connexion à ma db 
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='gestionstock_bd'
)



app.config['SECRET_KEY'] = 'secret key'


@app.route('/')
def accueil():
    cursor = conn.cursor()
    s = "SELECT COUNT(*) AS nombre_produits FROM produits"
    cursor.execute(s)
    
    count_prod = cursor.fetchone()  # Utilisez fetchone() pour obtenir la première ligne de résultat
    nombre_total_produits = count_prod[0]
    
    c = "SELECT COUNT(*) AS nombre_client FROM client"
    cursor.execute(c)
    
    count_client = cursor.fetchone()  # Utilisez fetchone() pour obtenir la première ligne de résultat
    nombre_total_client = count_client[0]  

    f = "SELECT COUNT(*) AS nombre_fournisseur FROM fournisseurs"
    cursor.execute(f)
    
    count_fournisseur= cursor.fetchone()  # Utilisez fetchone() pour obtenir la première ligne de résultat
    nombre_total_fournisseur = count_fournisseur[0] 
    return render_template("dashboard.html", nombre_total_client=nombre_total_client, nombre_total_produits=nombre_total_produits, nombre_total_fournisseur=nombre_total_fournisseur)



# @app.route("/data")
# def get_data():
#     cur = conn.cursor()

#     # Exemple : Obtenir les ventes par mois pour le graphique
#     cur.execute(
#         "SELECT DATE_FORMAT(date, '%Y-%m') AS month, COUNT(*) AS total_sales FROM ventes GROUP BY month"
#     )
#     sales_data = cur.fetchall()

#     # Exemple : Obtenir les données pour le meilleur produit vendu
#     cur.execute(
#         "SELECT produit, COUNT(*) AS total_sales FROM ventes GROUP BY produit ORDER BY total_sales DESC LIMIT 1"
#     )
#     best_product = cur.fetchone()

#     # Exemple : Obtenir les données pour les top 5 des meilleurs clients
#     cur.execute(
#         "SELECT name, COUNT(*) AS total_purchases FROM ventes GROUP BY name ORDER BY total_purchases DESC LIMIT 5"
#     )
#     top_clients = cur.fetchall()

#     cur.execute(
#         # Tableau des ventes de produits
#         """
#         SELECT v.produit, v.type, SUM(v.quantite) AS total_quantity, SUM(v.prix_vente) AS total_sales, v.id_utilisateur, u.nom 
#         FROM ventes AS v
#         JOIN utilisateurs AS u ON v.id_utilisateur = u.id_utilisateur
#         GROUP BY v.produit
#         """
#     )
#     product_sales = cur.fetchall()

#     # Obtenir les ventes par utilisateur pour le graphique
#     cur.execute(
#         """
#         SELECT u.nom, SUM(v.prix_vente) AS total_sales
#         FROM ventes AS v
#         JOIN utilisateurs AS u ON v.id_utilisateur = u.id_utilisateur 
#         GROUP BY u.nom
#         """
#     )
#     user_sales = cur.fetchall()

#     # Obtenir les ventes par type de produit pour le graphique
#     cur.execute(
#         """SELECT type, SUM(quantite) AS total_quantity, SUM(prix_vente) AS total_sales FROM ventes GROUP BY type"""
#     )
#     type_sales = cur.fetchall()

#     # Calculer le prix moyen de vente pour l'ensemble des ventes
#     cur.execute("SELECT AVG(prix_vente) AS avg_price FROM ventes")
#     overall_avg_price = cur.fetchone()[0]

#     # Calculer le prix moyen de vente pour chaque produit
#     cur.execute(
#         "SELECT produit, AVG(prix_vente) AS avg_price FROM ventes GROUP BY produit"
#     )
#     product_avg_prices = cur.fetchall()

#     cur.close()

#     return jsonify(
#         {
#             "sales_data": sales_data,
#             "best_product": best_product,
#             "top_clients": top_clients,
#             "product_sales": product_sales,
#             "user_sales": user_sales,
#             "type_sales": type_sales,
#             "overall_avg_price": overall_avg_price,
#             "product_avg_prices": product_avg_prices,
#         }
#     )


@app.route("/data")
def get_data():
    cur = conn.cursor()

    # Obtenir les ventes par mois pour le graphique
    cur.execute(
        "SELECT DATE_FORMAT(date_vente, '%Y-%m') AS month, COUNT(*) AS total_sales FROM ventes GROUP BY month"
    )
    sales_data = cur.fetchall()

    # Obtenir les données pour le meilleur produit vendu
    cur.execute(
        "SELECT id_prod, COUNT(*) AS total_sales FROM ventes GROUP BY id_prod ORDER BY total_sales DESC LIMIT 1"
    )
    best_product_id = cur.fetchone()[0]

    # Obtenir les données pour les top 5 des meilleurs clients
    cur.execute(
        "SELECT id_utilisateur, COUNT(*) AS total_purchases FROM ventes GROUP BY id_utilisateur ORDER BY total_purchases DESC LIMIT 5"
    )
    top_clients = cur.fetchall()

    # Obtenir les ventes de chaque produit
    cur.execute(
        """
        SELECT v.id_prod, p.nom_prod, p.id_type, SUM(v.quantite) AS total_quantity, SUM(v.montant) AS total_sales
        FROM ventes AS v
        JOIN produits AS p ON v.id_prod = p.id_prod 
        GROUP BY v.id_prod
        """
    )
    product_sales = cur.fetchall()

    # Obtenir les ventes par utilisateur pour le graphique
    cur.execute(
        """
        SELECT u.nom_prenom, SUM(v.montant) AS total_sales
        FROM ventes AS v
        JOIN utilisateurs AS u ON v.id_utilisateur = u.id_utilisateur 
        GROUP BY u.nom_prenom
        """
    )
    user_sales = cur.fetchall()

    # Obtenir les ventes par type de produit pour le graphique
    cur.execute(
        """SELECT p.id_type, SUM(v.quantite) AS total_quantity, SUM(v.montant) AS total_sales FROM ventes AS v
           JOIN produits AS p ON v.id_prod = p.id_prod
           GROUP BY p.id_type"""
    )
    type_sales = cur.fetchall()

    # Calculer le prix moyen de vente pour l'ensemble des ventes
    cur.execute("SELECT AVG(montant) AS avg_price FROM ventes")
    overall_avg_price = cur.fetchone()[0]

    # Calculer le prix moyen de vente pour chaque produit
    cur.execute(
        "SELECT id_prod, AVG(montant) AS avg_price FROM ventes GROUP BY id_prod"
    )
    product_avg_prices = cur.fetchall()

    cur.close()

    return jsonify(
        {
            "sales_data": sales_data,
            "best_product_id": best_product_id,
            "top_clients": top_clients,
            "product_sales": product_sales,
            "user_sales": user_sales,
            "type_sales": type_sales,
            "overall_avg_price": overall_avg_price,
            "product_avg_prices": product_avg_prices,
        }
    )




# Fonction pour générer un mot de passe aléatoire
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password

# ! Mécanisme de protection pour obligier le user à se connecter
# ? Utiliser le décorateur @login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_utilisateur' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
            return redirect(url_for('inscription'))
        return f(*args, **kwargs)
    return decorated_function

# # ? Login user
# @app.route('/connexion', methods=['GET', 'POST'])
# def connexion():
    
#     # ? Utilisons un curseur pour exécuter nos requêtes SQL
#     cursor = conn.cursor()

#     if request.method == 'POST':
#         email = request.form['email']
#         mot_de_passe = request.form['mot_de_passe']

#         select_query = "SELECT id_utilisateur, email, mot_de_passe FROM utilisateurs WHERE email = %s"
#         cursor.execute(select_query, (email,))
#         user = cursor.fetchone()

#         if user and bcrypt.check_password_hash(user[2], mot_de_passe):
#             session['id_utilisateur'] = user[0]
#             session['email'] = user[1]
#             flash('Connexion réussie!', 'success')
#             return redirect(url_for('accueil'))
#         else:
#             flash(f"Nom d'utilisateur ou mot de passe incorrect.", 'danger')

#     return render_template('connexion.html')

# Route de connexion
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    cursor = conn.cursor()

    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        select_query = """
        SELECT u.id_utilisateur, u.nom_prenom, u.mot_de_passe, r.statut
        FROM utilisateurs u
        JOIN roles r ON u.id_role = r.id_role
        WHERE u.email = %s
        """
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[2], mot_de_passe):
            session['id_utilisateur'] = user[0]
            session['nom_prenom'] = user[1]  # Nom complet de l'utilisateur
            session['role'] = user[3]  # Statut de l'utilisateur
            flash('Connexion réussie!', 'success')
            return redirect(url_for('accueil'))

        else:
            flash(f"Nom d'utilisateur ou mot de passe incorrect.", 'danger')

    return render_template('connexion.html')



# ? Route pour la déconnexion
@app.route('/logout')
@login_required
def deconnexion():
    session.pop('id_utilisateur', None)

    flash('Déconnexion réussie!', 'success')
    return redirect(url_for('accueil'))

    return render_template('connexion.html')

@app.route('/Inscription/', methods=['GET', 'POST'])
def inscription(): 
    cursor = conn.cursor()
    cursor.execute("SELECT statut FROM roles")
    roles = cursor.fetchall()

    if request.method == 'POST':
        nom_prenom = request.form['nom_prenom']
        genre = request.form['genre']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        id_role = request.form['role']  # Correction ici

        select_query = "SELECT id_utilisateur FROM utilisateurs WHERE email = %s"
        cursor.execute(select_query, (email,))
        user_exist = cursor.fetchone()

        if user_exist:
            flash("Cet utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur.", 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(mot_de_passe)
            
            insert_query = "INSERT INTO utilisateurs (nom_prenom, genre, email, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, (SELECT id_role FROM roles WHERE statut = %s))"


            # insert_query = "INSERT INTO utilisateurs (nom_prenom, genre, email, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (nom_prenom, genre, email, hashed_password, id_role))
            conn.commit()  # Ajout du commit

            cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE email = %s", (email,))
            id_utilisateur = cursor.fetchone()[0]

            session['id_utilisateur'] = id_utilisateur

            flash('Inscription réussie! Vous êtes maintenant connecté.', 'success')
            return redirect(url_for('connexion'))

    return render_template('connexion.html', roles=roles)


class User(UserMixin):
    pass

# Fonction pour charger un utilisateur à partir de la base de données
@login_manager.user_loader
def load_user(id_utilisateur):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE id_utilisateur = %s", (id_utilisateur,))
    user_data = cursor.fetchone()
    if user_data:
        user = User()
        id_utilisateur = user_data[0]  # ID de l'utilisateur
        return user
    return None













@app.route('/produit')
@login_required
def produit():
    cursor = conn.cursor()
    s = "SELECT p.id_prod, p.nom_prod, t.categorie_prod, p.prix_unitaire FROM produits p INNER JOIN typeproduits t ON p.id_type = t.id_type"
    cursor.execute(s)
    listProd = cursor.fetchall()
    print(s)
    return render_template('./display/produit.html', listProd=listProd)

@app.route('/formulaireproduit', methods=['POST', 'GET'])
@login_required
def formProd():
    if request.method == 'POST':
        nom_prod = request.form['nom_prod']
        prix_unitaire = request.form['prix_unitaire']
        id_type = request.form['id_type']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produits (nom_prod, id_type, prix_unitaire) VALUES (%s, %s, %s)", (nom_prod, id_type, prix_unitaire))
        conn.commit()
        flash('Produit ajouté !', 'success')
        return redirect(url_for('produit'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT id_type, categorie_prod FROM typeproduits")
        categories = cursor.fetchall()
        return render_template('./add/formProd.html', categories=categories)

#aller à la page modification produit après avoir cliquer sur modifier
@app.route("/Modifprod/<int:id_prod>",methods=['POST','GET'])
@login_required
def Modifprod(id_prod):
    if request.method=='POST':
        nom_prod = request.form['nom_prod']
        prix_unitaire = request.form['prix_unitaire']
        id_type = request.form['id_type']
        cursor = conn.cursor()
        cursor.execute("UPDATE produits SET nom_prod=%s, prix_unitaire=%s, id_type=%s WHERE id_prod=%s", (nom_prod, prix_unitaire, id_type, id_prod))
        conn.commit()
        flash('Produit Modifié !')
        return redirect(url_for("produit"))  # Redirige vers la route "produit" après la modification
    
    cursor = conn.cursor()
    cursor.execute("SELECT p.id_prod, p.nom_prod, t.id_type, p.prix_unitaire FROM produits p INNER JOIN typeproduits t ON p.id_type = t.id_type WHERE p.id_prod=%s",(id_prod,))
    data = cursor.fetchone()
    
    cursor.execute("SELECT id_type, categorie_prod FROM typeproduits")
    categories = cursor.fetchall()
    
    return render_template("./update/update_prod.html", data=data, categories=categories)

#aller à la page suppression produit après avoir cliquer sur suppimer
@login_required
@app.route("/SuppressionProduit/<int:id_prod>", methods=['GET'])
def DeleteProd(id_prod):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE id_prod=%s", (id_prod,))
    conn.commit()
    flash('Produit Supprimé !')
    return redirect(url_for("produit"))

@app.route('/typeprod')
@login_required
def typeprod():
    cursor = conn.cursor()
    s = "SELECT * FROM typeproduits"
    cursor.execute(s)#pour exécuter la requete
    listTypeProd = cursor.fetchall()
    return render_template('./display/typeprod.html', listTypeProd = listTypeProd)

@app.route('/formTypeprod', methods=['POST', 'GET'])
@login_required
def formTypeprod():
   if request.method == 'POST':
      categorie_prod = request.form['categorie_prod']
      cursor = conn.cursor()
      cursor.execute("INSERT INTO typeproduits (categorie_prod) VALUES (%s)", (categorie_prod,))
      conn.commit()
      flash('Categorie Ajouté !', 'success')
      return redirect(url_for("typeprod"))
   return render_template('./add/formTypeprod.html')

#aller à la page modification typeproduit après avoir cliquer sur modifier
@app.route("/Modiftypeproduit/<int:id_type>", methods=['POST', 'GET'])
@login_required
def Modiftypeproduit(id_type):
    if request.method=='POST':
        categorie_prod = request.form['categorie_prod']
        cursor = conn.cursor()
        cursor.execute("UPDATE typeproduits SET categorie_prod=%s WHERE id_type=%s", (categorie_prod, id_type))
        conn.commit()
        flash('Categorie du Produit Modifié !')
        return redirect(url_for("typeprod"))  # Redirige vers la route "typeprod" après la modification

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM typeproduits WHERE id_type=%s",(id_type,))
    data = cursor.fetchone()

    return render_template("./update/update_typeprod.html", data=data)
    
#aller à la page suppression typeproduit après avoir cliquer sur suppimer
@app.route("/SuppressionTypeProduit/<int:id_type>", methods=['GET'])
@login_required
def DeletetypeProd(id_type):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM typeproduits WHERE id_type=%s", (id_type,))
    conn.commit()
    flash('Type du Produit Supprimé !')
    return redirect(url_for("typeprod"))


@app.route('/vente')
@login_required
def vente():
    cursor = conn.cursor()
    s = """
    SELECT v.id_vente, t.categorie_prod, p.nom_prod, u.nom_prenom as nom_vendeur, v.date_vente, v.montant,v.quantite
    FROM ventes v
    INNER JOIN typeproduits t ON v.id_type = t.id_type
    INNER JOIN produits p ON v.id_prod = p.id_prod
    LEFT JOIN utilisateurs u ON v.id_utilisateur = u.id_utilisateur
"""
    cursor.execute(s)
    listVentes = cursor.fetchall()
    return render_template('./display/vente.html', listVentes=listVentes)

@app.route('/formVente', methods=['POST', 'GET'])
@login_required
def formVente():
    
    if request.method == 'POST':
        date_vente = request.form['date']
        quantite = request.form['quantite']
        # id_type = request.form['id_type']
        # id_utilisateur = request.form['id_utilisateur']
        id_prod = request.form['id_prod']
        id_utilisateur = int(session['id_utilisateur'])
        cursor = conn.cursor()
        cursor.execute('select prix_unitaire from produits where id_prod=%s',(id_prod,))
        prix_unitaire=cursor.fetchone()
        montant= int(prix_unitaire[0])*int(quantite)
        cursor.execute('select id_type from produits where id_prod=%s',(id_prod,))
        id_type=cursor.fetchone()
        cursor.execute("INSERT INTO ventes (id_type, id_prod, id_utilisateur, date_vente, quantite, montant) VALUES (%s, %s, %s, %s, %s, %s)", (int(id_type[0]), id_prod, id_utilisateur, date_vente, quantite, float(montant)))
        conn.commit()

        cursor = conn.cursor()
        cursor.execute('select quantite from stock where id_prod=%s', (id_prod,))
        quantite_stock=cursor.fetchone()
        new_quant = int(quantite_stock[0]) - int(quantite)
        cursor.execute("UPDATE stock SET quantite=%s WHERE id_prod=%s", ( new_quant, id_prod))
        conn.commit()

        flash('Vente ajoutée avec succès !', 'success')
        return redirect(url_for('vente'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT id_type, categorie_prod FROM typeproduits")
        categories = cursor.fetchall()

        cursor.execute("SELECT id_utilisateur, nom_prenom FROM utilisateurs WHERE id_role = 1")
        utilisateurs = cursor.fetchall()

        cursor.execute("SELECT id_prod, nom_prod FROM produits")
        produits = cursor.fetchall()

        return render_template('./add/formVente.html', categories=categories, utilisateurs=utilisateurs, produits=produits)

#aller à la page modification vente après avoir cliquer sur modifier
@app.route("/ModifVente/<int:id_vente>",methods=['POST','GET'])
@login_required
def ModifVente(id_vente):
    if request.method=='POST':
        date_vente = request.form['date']
        montant = request.form['montant']
        id_type = request.form['id_type']
        id_utilisateur = request.form['id_utilisateur']
        id_prod = request.form['id_prod']

        cursor = conn.cursor()
        cursor.execute("UPDATE ventes SET id_type=%s, id_prod=%s, id_utilisateur=%s, date_vente=%s, montant=%s WHERE id_vente=%s", (id_type, id_prod, id_utilisateur, date_vente, montant, id_vente))
        conn.commit()
        flash('Vente Modifiée !')
        return redirect(url_for("vente"))  # Redirige vers la route "vente" après la modification
        
    cursor = conn.cursor()
    cursor.execute("""
    SELECT v.id_vente, t.categorie_prod, p.nom_prod, u.nom_prenom as nom_vendeur, v.date_vente, v.montant
    FROM ventes v
    INNER JOIN typeproduits t ON v.id_type = t.id_type
    INNER JOIN produits p ON v.id_prod = p.id_prod
    INNER JOIN utilisateurs u ON v.id_utilisateur = u.id_utilisateur WHERE v.id_vente=%s""", (id_vente,))
    data = cursor.fetchone()
    
    cursor = conn.cursor()
    cursor.execute("SELECT id_type, categorie_prod FROM typeproduits")
    categories = cursor.fetchall()

    cursor.execute("SELECT id_utilisateur, nom_prenom FROM utilisateurs WHERE id_role = 1")
    utilisateurs = cursor.fetchall()

    cursor.execute("SELECT id_prod, nom_prod FROM produits")
    produits = cursor.fetchall()


    return render_template('./update/update_vente.html',data=data, categories=categories, utilisateurs=utilisateurs, produits=produits)



#aller à la page suppression vente après avoir cliquer sur suppimer
@app.route("/SuppressionVente/<int:id_vente>", methods=['GET'])
@login_required
def DeleteVente(id_vente):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventes WHERE id_vente=%s", (id_vente,))
    conn.commit()
    flash('Vente Supprimé !')
    return redirect(url_for("vente"))

@app.route('/client')
@login_required
def client():
    cursor = conn.cursor()
    s = "SELECT * FROM client"
    cursor.execute(s)#pour exécuter la requete
    listClient = cursor.fetchall()
    return render_template('./display/client.html', listClient = listClient)

@app.route('/fournisseur')
@login_required
def fournisseur():
    cursor = conn.cursor()
    s = "SELECT * FROM fournisseurs"
    cursor.execute(s)
    listfourn = cursor.fetchall()
    return render_template('./display/fournisseur.html',listfourn=listfourn)

@app.route('/formFourn', methods=['POST', 'GET'])
@login_required
def formFourn():
   if request.method == 'POST':
      nom_fournisseur = request.form['nom_fournisseur']
      adresse_fournisseur = request.form['adresse_fournisseur']
      email_fournisseur = request.form['email_fournisseur']
      telephone6_fournisseur = request.form['telephone6_fournisseur']
      
      cursor = conn.cursor()
      cursor.execute("INSERT INTO fournisseurs (nom_fournisseur,adresse_fournisseur,email_fournisseur,telephone6_fournisseur) VALUES (%s,%s,%s,%s)", (nom_fournisseur,adresse_fournisseur,email_fournisseur,telephone6_fournisseur))
      conn.commit()
      flash('Fournisseur Ajouté !', 'success')
      return redirect(url_for("fournisseur"))
   return render_template('./add/formFourn.html')


@app.route('/stock')
@login_required
def stock():
    cursor = conn.cursor()
    s = "SELECT s.id_stock, s.quantite, s.datemaj, p.nom_prod FROM stock s INNER JOIN produits p ON s.id_prod = p.id_prod"
    cursor.execute(s)
    listStock = cursor.fetchall()
    print(s)
    return render_template('./display/stock.html', listStock=listStock)

@app.route('/formulairestock', methods=['POST', 'GET'])
@login_required
def formStock():
    if request.method == 'POST':
        id_prod = request.form['id_prod']
        quantite = request.form['quantite']
        datemaj = request.form['datemaj']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stock ( id_prod, quantite, datemaj) VALUES (%s, %s, %s)", (id_prod, quantite, datemaj))
        conn.commit()
        flash('Stock ajouté !', 'success')
        return redirect(url_for('stock'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT id_prod, nom_prod FROM produits")
        produits = cursor.fetchall()
        return render_template('./add/formStock.html', produits=produits)

#aller à la page modification stock après avoir cliquer sur modifier
@app.route("/Modifstock/<int:id_stock>",methods=['POST','GET'])
@login_required
def Modifstock(id_stock):
    if request.method=='POST':
        id_prod = request.form['id_prod']
        quantite = request.form['quantite']
        datemaj = request.form['datemaj']
        cursor = conn.cursor()
        cursor.execute("UPDATE stock SET id_prod=%s, quantite=%s, datemaj=%s WHERE id_stock=%s", (id_prod, quantite, datemaj, id_stock))
        conn.commit()
        flash('Stock Modifié !')
        return redirect(url_for("stock"))  # Redirige vers la route "stock" après la modification
    
    cursor = conn.cursor()
    cursor.execute("SELECT s.id_stock, s.quantite, s.datemaj, p.id_prod FROM stock s INNER JOIN produits p ON s.id_prod = p.id_prod WHERE s.id_stock=%s",(id_stock,))
    data = cursor.fetchone()
    
    cursor.execute("SELECT id_prod, nom_prod FROM produits")
    produits = cursor.fetchall()
    
    return render_template("./update/update_stock.html", data=data, produits=produits)

#aller à la page suppression stock après avoir cliquer sur suppimer
@login_required
@app.route("/SuppressionStock/<int:id_stock>", methods=['GET'])
def DeleteStock(id_stock):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock WHERE id_stock=%s", (id_stock,))
    conn.commit()
    flash('Stock Supprimé !')
    return redirect(url_for("stock"))


@app.route('/users_admin')
@login_required
def users_admin():
    cursor = conn.cursor()
    s = "SELECT u.id_utilisateur, u.nom_prenom, u.genre, u.email, u.mot_de_passe, r.statut FROM utilisateurs u JOIN roles r ON u.id_role = r.id_role WHERE u.id_role = 3"
    cursor.execute(s)
    users_admin = cursor.fetchall()
    return render_template('./display/users_admin.html', users_admin=users_admin)


@app.route('/Gestion_de_compte_gestionnaire')
@login_required
def users_gesto():
    cursor = conn.cursor()
    s = "SELECT u.id_utilisateur, u.nom_prenom, u.genre, u.email, u.mot_de_passe, r.statut FROM utilisateurs u JOIN roles r ON u.id_role = r.id_role WHERE u.id_role = 2"

    cursor.execute(s)#pour exécuter la requete
    users_gesto = cursor.fetchall()
    return render_template('./display/users_gesto.html', users_gesto = users_gesto)

# @app.route('/Ajouter_un_nouveau_gestionnaire', methods=['POST', 'GET'])
# @login_required
# def formUsers_gesto():
#     cursor = conn.cursor()
#     cursor.execute("SELECT id_role, statut FROM roles")
#     roles = cursor.fetchall()
    
#     if request.method == 'POST':
#         nom_prenom = request.form['nom_prenom']
#         genre = request.form['genre']
#         email = request.form['email']
#         mot_de_passe = request.form['mot_de_passe']
#         id_role = request.form['role']  # Modification ici pour récupérer le rôle
        
#         cursor.execute("INSERT INTO utilisateurs (nom_prenom, genre, email, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, %s)", (nom_prenom, genre, email, mot_de_passe, id_role))
#         conn.commit()
#         flash('Utilisateur ajouté !', 'success')
#         return redirect(url_for("users_gesto"))
    
#     return render_template('./add/formGesto.html', roles=roles)

# Fonction pour générer un mot de passe aléatoire
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# @app.route('/Ajouter_un_nouveau_gestionnaire', methods=['POST', 'GET'])
# @login_required
# def formUsers_gesto():
#     cursor = conn.cursor()
#     cursor.execute("SELECT id_role, statut FROM roles")
#     roles = cursor.fetchall()
    
#     if request.method == 'POST':
#         nom_prenom = request.form['nom_prenom']
#         genre = request.form['genre']
#         email = request.form['email']
#         id_role = request.form['role']  # Modification ici pour récupérer le rôle
        
#         # Génération d'un mot de passe aléatoire
#         mot_de_passe = generate_random_password()
        
#         cursor.execute("INSERT INTO utilisateurs (nom_prenom, genre, email, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, %s)", (nom_prenom, genre, email, mot_de_passe, id_role))
#         conn.commit()
#         flash('Utilisateur ajouté !', 'success')
#         return redirect(url_for("users_gesto"))
    
#     return render_template('./add/formGesto.html', roles=roles)
@app.route('/Ajouter_un_nouveau_gestionnaire', methods=['POST', 'GET'])
@login_required
def formUsers_gesto():
    cursor = conn.cursor()
    cursor.execute("SELECT id_role, statut FROM roles")
    roles = cursor.fetchall()
    
    if request.method == 'POST':
        nom_prenom = request.form['nom_prenom']
        genre = request.form['genre']
        email = request.form['email']
        id_role = request.form['role']  # Modification ici pour récupérer le rôle
        
        # Génération d'un mot de passe aléatoire
        mot_de_passe = generate_random_password()
        
        # Insérer l'utilisateur dans la base de données avec le mot de passe généré
        cursor.execute("INSERT INTO utilisateurs (nom_prenom, genre, email, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, %s)", (nom_prenom, genre, email, mot_de_passe, id_role))
        conn.commit()
        
        # Envoyer un email à l'utilisateur avec son nom d'utilisateur (email) et le mot de passe généré
        msg = Message('Votre nouveau mot de passe', sender='allahnoemie43@gmail.com', recipients=[email])
        msg.body = f"Bonjour {nom_prenom},\nVotre mot de passe généré est: {mot_de_passe}\nUtilisez ce mot de passe pour vous connecter à votre compte.\nCordialement,\nVotre application"
        mail.send(msg)
        
        flash('Utilisateur ajouté !', 'success')
        return redirect(url_for("users_gesto"))
    
    return render_template('./add/formGesto.html', roles=roles)

@app.route('/Modifier_mon_compte_gestionnaire', methods=['POST', 'GET'])
@login_required
def reglage_gesto():

    return render_template('./display/reglage_gesto.html')
# #aller à la page modification typeproduit après avoir cliquer sur modifier
# @app.route("/Modiftypeproduit/<int:id_type>", methods=['POST', 'GET'])
# @login_required
# def Modiftypeproduit(id_type):
#     if request.method=='POST':
#         categorie_prod = request.form['categorie_prod']
#         cursor = conn.cursor()
#         cursor.execute("UPDATE typeproduits SET categorie_prod=%s WHERE id_type=%s", (categorie_prod, id_type))
#         conn.commit()
#         flash('Categorie du Produit Modifié !')
#         return redirect(url_for("typeprod"))  # Redirige vers la route "typeprod" après la modification

#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM typeproduits WHERE id_type=%s",(id_type,))
#     data = cursor.fetchone()

#     return render_template("./update/update_typeprod.html", data=data)
    
#aller à la page suppression typeproduit après avoir cliquer sur suppimer
# @app.route("/SuppressionTypeProduit/<int:id_type>", methods=['GET'])
# @login_required
# def DeletetypeProd(id_type):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM typeproduits WHERE id_type=%s", (id_type,))
#     conn.commit()
#     flash('Type du Produit Supprimé !')
#     return redirect(url_for("typeprod"))


@app.route('/Gestion_de_compte_vendeur')
@login_required
def users_vend():
    cursor = conn.cursor()
    s = "SELECT u.id_utilisateur, u.nom_prenom, u.genre, u.email, u.mot_de_passe, r.statut FROM utilisateurs u JOIN roles r ON u.id_role = r.id_role WHERE u.id_role = 1"

    cursor.execute(s)#pour exécuter la requete
    users_vend = cursor.fetchall()
    return render_template('./display/users_vend.html', users_vend = users_vend)

# @app.route('/analyse/')
# def analyse():
#     cursor = conn.cursor()
#     s = "SELECT COUNT(*) AS nombre_produits FROM produits"
#     cursor.execute(s)
    
#     count_prod = cursor.fetchone()  # Utilisez fetchone() pour obtenir la première ligne de résultat
#     nombre_total_produits = count_prod[0]  # Récupérez la valeur de la colonne nombre_produits du tuple
#     return render_template("dashboard.html", count_prod=nombre_total_produits)

if __name__ == "__main__":
    app.run(debug=True,port=3000)



