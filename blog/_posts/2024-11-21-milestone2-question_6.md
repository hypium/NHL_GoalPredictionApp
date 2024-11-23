---
layout: post
title: Faites de votre mieux!
milestone: 2
question: 6
auteurs: Nathan Cormerais
---

### Figures (comparaison des performances)

Dans le cadre des expériences, nous avons étudié 3 approches en utilisant les modèles suivants:
- `MLPClassifier` (réseau de neuronnes) avec *fine-tuning* des hyperparamètres
- `XGBClassifier` avec *fine-tuning* des hyperparamètres
- `XGBClassifier` avec *fine-tuning* des hyperparamètres et sélection des caractéristiques

Les figures ci-dessous illustrent les performances des modèles, les modèles de base, c'est-à-dire sans *fine-tune* ni de sélection des caractéristiques optimales, sont inclus afin de comparer les performances et vérifier que notre approche permet bien d'améliorer les performances.

** *Pour les figures ci-dessous, nous écrivons: `+`/`-` pour signifier que nous incluons cette méthode ou non*

### ROC
![image](/public/advanced_models_visualizations/roc.png)
### Taux de buts
![image](/public/advanced_models_visualizations/taux_de_but.png)
### Pourcentage de buts cumulés
![image](/public/advanced_models_visualizations/cumul.png)

Avec les 3 figures ci-dessus, on observe très peu de différences entre les modèles `XGBClassifier` sans *fine-tune* des hyperparamètres et celui avec. En effet, en se basant seulement sur ces figures, on pourrait faire l'hypothèse que *fine-tuner* les hyperparamètres ne procure aucune amélioration des performances. Cependant, nous démontrerons dans la figure ci-dessous que le *fine-tuning* des hyperparamètres permet d'obtenir de meilleures performances et de meilleures prédictions.

### Diagramme de fiabilité
![image](/public/advanced_models_visualizations/fiabilite.png)

On remarque avec les courbes de fiabilité que le modèle `XGBClassifier`, avec *fine-tuning* des hyperparamètres et sélection des caractéristiques optimales, est le modèle le plus calibré. Par rapport aux autres figures où les modèles `XGBClassifier (+hypeparameters +features)` et `XGBClassifier(-hyperparameters +features)` sont similaires, leurs courbes de fiabilité sont ici très différentes car les prédicitions du modèle `XGBClassifier (+hypeparameters +features)` sont nettement mieux calibrées.

En plus de ces figures, nous avons utilisé 4 métriques pour évaluer les performances des modèles entraînés dans cette partie:
- **Perte logarithmique** (*log loss*)
- **Score de Brier**
- **ROC** (aire sous la courbe)
- **Précision** (*accuracy*)

La perte logarithmique permet de mesurer l'incertitude des prédictions faîtes par le modèle. Ce métrique permet donc d'évaluer chaque modèle par rapport à sa capacité à produire des probabilités qui reflètent bien les résultats réels. Le score de Brier permet de mesurer la calibration des probabilités des prédictions. L'aire sous la courbe (ROC-AUC) permet de comparer les taux de vrais positifs et de faux positifs. Enfin, nous avons utilisé la précision comme autre métrique pour mesurer la proportion de cas correctement prédits. Les résultats pour les 3 approches sont retranscrits dans le tableau ci-dessous:

| Modèle | Perte logartihmique | Score Brier | ROC/AUC | Précision |
| MLP *(fine-tune HP\*)* | 0.29432 | 0.083607 | 0.71618 | 0.90205 |
| XGB *(fine-tune HP\*)* | 0.29446 | 0.083612 | 0.71566 | 0.902 |
| XGB *(fine-tune HP\* + features selection)* | **0.26871** | **0.076712** | **0.7781** | **0.90704** |

\*HP: hyperparamètres

On remarque avec ces métriques quantitifs, que le modèle `XGBClassifier` après avoir *fine-tune* ses hyperparamètres et sélectionné les caractéristiques optimales, permet d'obtenir de meilleures performances.

### Conclusion/Meilleur modèle

En observant les résultats, la meilleure performance a été enregistrée en utilisant le classifieur `XGBClassifier` et en augmentant ses performances en combinant les techniques:
- **Fine-tuning des hyperparamètres**
- **Sélection des caractéristiques optimales**

Donc le modèle `XGBClassifier (fine-tune hyperparamètre et sélection des caractéristiques)` est le meilleur modèle d'après nos expériences ([run wandb](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/eqiitp2n)).

### Runs (wandb)

Liens vers les runs pour le modèle basé sur:
- **MLP (fine-tune hyperparamètres)**: [mlp-hp_finetuned](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/g532jndd)
- **XGBClassifier (fine-tune hyperparamètres)**: [xgb-hp_finetuned](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/2mimwsz4)
- **XGBClassifier (fine-tune hyperparamètre et sélection des caractéristiques)**: [xgb-hp_finetuned+feature_selection](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/eqiitp2n)
