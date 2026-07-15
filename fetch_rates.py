import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def recuperer_taux_actuels():
    # Définition des tickers Yahoo Finance pour les différentes maturités
    # ^IRX (3 mois), ^FVX (5 ans), ^TNX (10 ans), ^TYX (30 ans)
    tickers = {
        0.25: "^IRX",
        5.0: "^FVX",
        10.0: "^TNX",
        30.0: "^TYX"
    }
    
    taux_recuperes = {}
    
    print("Connexion à Yahoo Finance et extraction des taux...")
    
    for maturite, ticker in tickers.items():
        data = yf.Ticker(ticker)
        # Récupération de la dernière valeur de clôture disponible
        historique = data.history(period="1d")
        if not historique.empty:
            derniere_valeur = historique["Close"].iloc[-1]
            taux_recuperes[maturite] =ConcreteValue = derniere_valeur
            print(f"Maturité {maturite} ans : {derniere_valeur:.2f}%")
            
    # Conversion en DataFrame Pandas pour faciliter les futurs calculs
    df_courbe = pd.DataFrame(list(taux_recuperes.items()), columns=["Maturite", "Taux"])
    df_courbe = df_courbe.sort_values(by="Maturite").reset_index(drop=True)
    return df_courbe

if __name__ == "__main__":
    donnees_courbe = recuperer_taux_actuels()
    
    # Aperçu rapide sous forme de graphique brut
    plt.figure(figsize=(8, 5))
    plt.plot(donnees_courbe["Maturite"], donnees_courbe["Taux"], marker="o", linestyle="-", color="blue")
    plt.title("Aperçu de la Courbe des Taux Réels")
    plt.xlabel("Maturité (en années)")
    plt.ylabel("Taux d'intérêt (%)")
    plt.grid(True)
    plt.show()
    
