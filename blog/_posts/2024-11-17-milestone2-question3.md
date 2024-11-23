---
layout: post
title: Modèles de base
milestone: 2
question: 3
auteurs: Nathan Cormerais
---

Après avoir entaîné un classifieur de type *Logistic Regression* seulement basé sur la distance, on obtient une précision de `0.91` sur l'ensemble de validation. Cependant, après avoir généré une matrice de confusion pour évaluer les prédictions faites par le modèle sur l'ensemble de validation, on remarque que le modèle ne prédit jamais la classe `1` (but) pour les tirs de l'ensemble de données. Et ce, peu importe si le tir est vraiment un but ou non (*true label*).

Cela pourrait être dû à un manque de tirs qui mènent à un but dans les données d'entraînement par rapport aux tirs qui ne mènent pas à un but. En effet, les données pour les deux classes (`0` ou `1`) n'ont pas la même taille et cela crée donc un désiquilibre entre les classes qui pourraient expliquer ce problème. De plus, se baser uniquement sur la distance peut aussi en être la cause car cette caractéristique n'offre peut-être pas assez de variance dans les données pour que le modèle puisse correctement différencier les buts des tirs sans résultat.
 
### Évaluation des performances (figures)

![image](/public/base_models_visualizations/roc.png)
![image](/public/base_models_visualizations/taux_but.png)
![image](/public/base_models_visualizations/cumul_buts.png)
![image](/public/base_models_visualizations/calibration.png)

En observant la figure montrant le ROC et l'aire sous la courbe (AUC), on remarque que les modèles sont identiques en termes de AUC (0.70). Cette mesure signifie que les modèles sont plutôt bons pour catégoriser les tirs en buts (1) et non buts (0). Cependant, la figure représentant l'évolution du taux de but ainsi que celle représentant le pourcentage de buts cumulé démontrent une similtude entre les modèles **distance** et **distance + angle**. En se basant sur ces figures, on peut en déduire que la caractéristique **angle** n'est pas vraiment importante pour prédire la probabilité qu'un tir soit un but ou non. La similiraté entre les modèles **distance** et **distance + angle** démontre bien que la caractéristique **angle** n'impactera pas vraiment les probabilités de but prédites par le modèle. Il semblerait donc que la **distance** suffit afin d'obtenir des résultats corrects avec un modèle de régression logistique.

### Runs (wandb)

Liens vers les runs pour le modèle basé sur:
- **Distance**: [distance_only_run](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/9t89uzux)
- **Angle**: [angle_only_run](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/ticgb8hk)
- **Distance et angle**: [angle_and_distance_run](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/runs/2firv1lt)
