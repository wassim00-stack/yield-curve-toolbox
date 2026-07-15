import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def executer_bootstrapping():
    print("Initialisation des obligations du marché...")
    
    # Données du marché : Obligations avec coupons annuels
    # Un prix de 100 signifie que l'obligation vaut son pair.
    marchandises = {
        "Maturite": [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0],
        "Taux_Coupon": [0.0, 0.0, 0.02, 0.025, 0.03, 0.035, 0.04],
        "Prix": [98.5, 96.0, 100.2, 101.0, 99.5, 98.2, 97.0]
    }
    
    df = pd.DataFrame(marchandises)
    taux_zero_coupon = []
    
    print("Calcul des taux Zéro-Coupon par récurrence (Bootstrapping)...")
    
    for i, row in df.iterrows():
        t = row["Maturite"]
        c = row["Taux_Coupon"]
        p = row["Prix"]
        
        # Pour les obligations à court terme sans coupon (Zero-Coupon d'origine)
        if c == 0.0:
            r = -np.log(p / 100) / t
        else:
            # Pour les obligations avec coupons, on soustrait la valeur actualisée
            # des coupons précédents pour isoler le flux final
            valeur_coupons_actualises = 0.0
            for j in range(i):
                t_precedent = df.loc[j, "Maturite"]
                r_precedent = taux_zero_coupon[j]
                # Flux du coupon annuel calculé au prorata
                flux_coupon = c * 100 * (t_precedent if j == 0 else (t_precedent - df.loc[j-1, "Maturite"]))
                valeur_coupons_actualises += flux_coupon * np.exp(-r_precedent * t_precedent)
            
            # Extraction du taux zéro-coupon final
            flux_final = 100 + (c * 100)
            r = -np.log((p - valeur_coupons_actualises) / flux_final) / t
            
        taux_zero_coupon.append(r)
        
    df["Taux_Zero_Coupon"] = taux_zero_coupon
    # Conversion en pourcentage pour l'affichage
    df["Taux_Zero_Coupon_Pct"] = df["Taux_Zero_Coupon"] * 100
    
    return df

if __name__ == "__main__":
    resultats = executer_bootstrapping()
    print("\n--- Résultats du Bootstrapping ---")
    print(resultats[["Maturite", "Taux_Coupon", "Prix", "Taux_Zero_Coupon_Pct"]].to_string(index=False))
    
    # Graphique de comparaison
    plt.figure(figsize=(9, 5))
    plt.plot(resultats["Maturite"], resultats["Taux_Zero_Coupon_Pct"], marker="o", color="darkred", label="Courbe Zéro-Coupon (Bootstrapped)")
    plt.title("Construction de la Courbe Taux Zéro-Coupon")
    plt.xlabel("Maturité (Années)")
    plt.ylabel("Taux d'intérêt (%)")
    plt.legend()
    plt.grid(True)
    plt.show()