import random
import json
import os

class LabyrinteMage:
    def __init__(self):
        self.nom_joueur = ""
        self.energie = 10
        self.salles_parcourues = 0
        self.historique_directions = []
        self.inventaire = {"potions": 0, "amulettes": 0}
        self.difficulte = "normal"
        
        # Énigmes possibles
        self.enigmes = [
            {"question": "Combien font 7 + 8 ?", "reponse": "15"},
            {"question": "Quelle est la capitale de la France ?", "reponse": "paris"},
            {"question": "Combien de côtés a un triangle ?", "reponse": "3"},
            {"question": "Quel est le résultat de 12 × 3 ?", "reponse": "36"},
            {"question": "Comment dit-on 'bonjour' en anglais ?", "reponse": "hello"},
            {"question": "Combien font 20 - 7 ?", "reponse": "13"},
            {"question": "Quelle couleur obtient-on en mélangeant rouge et bleu ?", "reponse": "violet"},
            {"question": "Combien y a-t-il de jours dans une semaine ?", "reponse": "7"}
        ]
    
    def afficher_menu_principal(self):
        """Affiche le menu d'accueil et les règles du jeu"""
        print("=" * 50)
        print("🧙‍♂️  LE LABYRINTHE DU MAGE  🧙‍♂️")
        print("=" * 50)
        print()
        print("📜 RÈGLES DU JEU :")
        print("• Tu es un apprenti mage coincé dans un labyrinthe magique")
        print("• Tu commences avec 10 points d'énergie")
        print("• Chaque déplacement te coûte 1 point d'énergie")
        print("• Tu peux gagner ou perdre de l'énergie selon les salles")
        print("• Si ton énergie atteint 0, tu meurs")
        print("• Survie à 10 salles pour gagner !")
        print()
        
        self.nom_joueur = input("Quel est ton nom, apprenti mage ? ").strip()
        if not self.nom_joueur:
            self.nom_joueur = "Mage Mystérieux"
        
        print(f"\nBienvenue, mage {self.nom_joueur} !")
        
        # Choix de difficulté (bonus)
        print("\nChoisissez votre niveau de difficulté :")
        print("1. Facile (plus d'énergie)")
        print("2. Normal")
        print("3. Difficile (moins d'énergie)")
        
        choix_diff = input("Votre choix (1-3) : ").strip()
        if choix_diff == "1":
            self.difficulte = "facile"
            self.energie = 15
            print("Mode facile activé ! Vous commencez avec 15 points d'énergie.")
        elif choix_diff == "3":
            self.difficulte = "difficile"
            self.energie = 7
            print("Mode difficile activé ! Vous ne commencez qu'avec 7 points d'énergie.")
        else:
            print("Mode normal sélectionné !")
        
        input("\nAppuyez sur Entrée pour commencer l'aventure...")
        print("\n" + "=" * 50)
    
    def choisir_direction(self):
        """Demande au joueur de choisir une direction"""
        directions_valides = ["N", "S", "E", "O"]
        
        while True:
            print(f"\nTour {self.salles_parcourues + 1} – Énergie : {self.energie}")
            if self.inventaire["potions"] > 0 or self.inventaire["amulettes"] > 0:
                print(f"💼 Inventaire : {self.inventaire['potions']} potions, {self.inventaire['amulettes']} amulettes")
            
            direction = input("Choisissez une direction (N/S/E/O) : ").upper().strip()
            
            if direction in directions_valides:
                return direction
            else:
                print("❌ Direction invalide ! Utilisez N, S, E ou O.")
    
    def generer_salle_aleatoire(self):
        """Génère aléatoirement le type de salle rencontrée"""
        types_salles = ["vide", "piege", "enigme", "tresor"]
        poids = [40, 30, 25, 5]  # Probabilités en pourcentage
        
        return random.choices(types_salles, weights=poids, k=1)[0]
    
    def salle_vide(self):
        """Gère une salle vide"""
        messages = [
            "Salle vide. Un silence mystique règne ici...",
            "Une salle déserte aux murs couverts de mousse ancienne.",
            "Cette salle semble abandonnée depuis des siècles.",
            "Vous entendez vos pas résonner dans cette salle vide."
        ]
        print(f"🏛️  {random.choice(messages)}")
        print("Aucun effet sur votre énergie.")
    
    def salle_piege(self):
        """Gère une salle piégée"""
        degats_possibles = [2, 3]
        if self.difficulte == "facile":
            degats_possibles = [1, 2]
        elif self.difficulte == "difficile":
            degats_possibles = [3, 4]
        
        degats = random.choice(degats_possibles)
        
        # Vérifier si le joueur a une amulette
        if self.inventaire["amulettes"] > 0:
            print("🛡️  Votre amulette vous protège partiellement du piège !")
            degats = max(1, degats - 1)
            self.inventaire["amulettes"] -= 1
        
        pieges = [
            f"💀 Salle piégée ! Des dards empoisonnés jaillissent du mur ! Vous perdez {degats} points d'énergie.",
            f"🕳️  Vous tombez dans une fosse ! Vous perdez {degats} points d'énergie.",
            f"⚡ Un éclair magique vous frappe ! Vous perdez {degats} points d'énergie.",
            f"🔥 Des flammes surgissent du sol ! Vous perdez {degats} points d'énergie."
        ]
        
        print(random.choice(pieges))
        self.energie -= degats
    
    def salle_enigme(self):
        """Gère une salle avec énigme"""
        enigme = random.choice(self.enigmes)
        print("🧩 Salle énigme ! Un esprit gardien vous pose une question :")
        print(f"❓ {enigme['question']}")
        
        reponse = input("Votre réponse : ").strip().lower()
        
        if reponse == enigme['reponse'].lower():
            gain = 2 if self.difficulte == "difficile" else 1
            print(f"✅ Bonne réponse ! Vous gagnez {gain} point(s) d'énergie !")
            self.energie += gain
        else:
            print(f"❌ Mauvaise réponse ! La bonne réponse était : {enigme['reponse']}")
            print("L'esprit disparaît sans vous récompenser.")
    
    def salle_tresor(self):
        """Gère une salle avec trésor (bonus)"""
        tresors = ["potion", "amulette", "energie"]
        tresor = random.choice(tresors)
        
        if tresor == "potion":
            self.inventaire["potions"] += 1
            print("🧪 Vous trouvez une potion de soin ! (Utilisable avec 'P')")
        elif tresor == "amulette":
            self.inventaire["amulettes"] += 1
            print("🛡️  Vous trouvez une amulette protectrice ! (Protection automatique)")
        else:  # energie
            gain = random.randint(2, 4)
            self.energie += gain
            print(f"💎 Vous trouvez un cristal d'énergie ! Vous gagnez {gain} points !")
    
    def utiliser_potion(self):
        """Permet au joueur d'utiliser une potion"""
        if self.inventaire["potions"] > 0:
            soin = random.randint(3, 5)
            self.energie += soin
            self.inventaire["potions"] -= 1
            print(f"🧪 Vous utilisez une potion et récupérez {soin} points d'énergie !")
            return True
        else:
            print("❌ Vous n'avez aucune potion !")
            return False
    
    def traiter_salle(self, type_salle):
        """Traite le type de salle rencontré"""
        if type_salle == "vide":
            self.salle_vide()
        elif type_salle == "piege":
            self.salle_piege()
        elif type_salle == "enigme":
            self.salle_enigme()
        elif type_salle == "tresor":
            self.salle_tresor()
    
    def sauvegarder_partie(self):
        """Sauvegarde la partie dans un fichier (bonus)"""
        donnees = {
            "nom_joueur": self.nom_joueur,
            "energie": self.energie,
            "salles_parcourues": self.salles_parcourues,
            "historique_directions": self.historique_directions,
            "inventaire": self.inventaire,
            "difficulte": self.difficulte
        }
        
        try:
            with open(f"sauvegarde_{self.nom_joueur.lower()}.json", "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=2, ensure_ascii=False)
            print(f"💾 Partie sauvegardée dans sauvegarde_{self.nom_joueur.lower()}.json")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")
    
    def charger_partie(self):
        """Charge une partie sauvegardée (bonus)"""
        nom_fichier = f"sauvegarde_{self.nom_joueur.lower()}.json"
        
        if os.path.exists(nom_fichier):
            try:
                with open(nom_fichier, "r", encoding="utf-8") as f:
                    donnees = json.load(f)
                
                self.energie = donnees["energie"]
                self.salles_parcourues = donnees["salles_parcourues"]
                self.historique_directions = donnees["historique_directions"]
                self.inventaire = donnees["inventaire"]
                self.difficulte = donnees["difficulte"]
                
                print("💾 Partie chargée avec succès !")
                return True
            except Exception as e:
                print(f"❌ Erreur lors du chargement : {e}")
                return False
        return False
    
    def afficher_fin_de_jeu(self, victoire):
        """Affiche le message de fin de jeu personnalisé"""
        print("\n" + "=" * 50)
        
        if victoire:
            print("🎉 VICTOIRE ! 🎉")
            print(f"Bravo {self.nom_joueur} ! Vous avez survécu et quitté le labyrinthe !")
            print(f"Énergie restante : {self.energie}")
        else:
            print("💀 DÉFAITE 💀")
            print(f"Hélas {self.nom_joueur}, vous avez succombé dans le labyrinthe...")
            print(f"Vous avez parcouru {self.salles_parcourues} salles avant de tomber.")
        
        print(f"\nChemin suivi : {', '.join(self.historique_directions) if self.historique_directions else 'Aucun'}")
        
        if self.inventaire["potions"] > 0 or self.inventaire["amulettes"] > 0:
            print(f"Inventaire final : {self.inventaire['potions']} potions, {self.inventaire['amulettes']} amulettes")
        
        print("=" * 50)
        
        # Proposer de sauvegarder l'historique
        if input("\nVoulez-vous sauvegarder votre historique ? (o/n) : ").lower().startswith('o'):
            self.sauvegarder_historique()
    
    def sauvegarder_historique(self):
        """Sauvegarde l'historique dans un fichier texte (bonus)"""
        nom_fichier = f"historique_{self.nom_joueur.lower()}.txt"
        
        try:
            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write(f"HISTORIQUE DE PARTIE - {self.nom_joueur}\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Difficulté : {self.difficulte}\n")
                f.write(f"Salles parcourues : {self.salles_parcourues}\n")
                f.write(f"Énergie finale : {self.energie}\n")
                f.write(f"Chemin : {', '.join(self.historique_directions)}\n")
                f.write(f"Inventaire final : {self.inventaire}\n")
            
            print(f"📝 Historique sauvegardé dans {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de l'historique : {e}")
    
    def jouer(self):
        """Boucle principale du jeu"""
        self.afficher_menu_principal()
        
        # Proposer de charger une partie
        if input(f"\nVoulez-vous charger une partie sauvegardée pour {self.nom_joueur} ? (o/n) : ").lower().startswith('o'):
            if not self.charger_partie():
                print("Nouvelle partie commencée.")
        
        # Boucle de jeu principale
        while self.salles_parcourues < 10 and self.energie > 0:
            # Proposer d'utiliser une potion
            if self.inventaire["potions"] > 0:
                if input("\nVoulez-vous utiliser une potion ? (o/n) : ").lower().startswith('o'):
                    self.utiliser_potion()
            
            # Choix de direction
            direction = self.choisir_direction()
            self.historique_directions.append(direction)
            
            # Coût du déplacement
            self.energie -= 1
            
            # Génération et traitement de la salle
            type_salle = self.generer_salle_aleatoire()
            self.traiter_salle(type_salle)
            
            # Incrémenter le compteur de salles
            self.salles_parcourues += 1
            
            # Proposer de sauvegarder
            if self.salles_parcourues % 3 == 0:  # Tous les 3 tours
                if input("\nVoulez-vous sauvegarder votre progression ? (o/n) : ").lower().startswith('o'):
                    self.sauvegarder_partie()
        
        # Fin de jeu
        victoire = self.salles_parcourues >= 10 and self.energie > 0
        self.afficher_fin_de_jeu(victoire)


def main():
    """Fonction principale"""
    print("Initialisation du Labyrinthe du Mage...")
    jeu = LabyrinteMage()
    jeu.jouer()
    
    # Proposer de rejouer
    if input("\nVoulez-vous rejouer ? (o/n) : ").lower().startswith('o'):
        main()
    else:
        print("Merci d'avoir joué au Labyrinthe du Mage ! 🧙‍♂️")


if __name__ == "__main__":
    main()