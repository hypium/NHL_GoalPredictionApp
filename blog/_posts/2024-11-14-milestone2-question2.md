---
layout: post
title: Ingénierie des caractéristiques I
milestone: 2
question: 2
auteurs: Nathan Cormerais
---

![image](/public/shots_goals_visualizations/histogramme_tirs_distance.png)

En observant cet histogramme, on remarque qu'il y a une concentration de tirs proches, voir très proches du filet de but. En effet, il semblerait que les tirs sont majoritairement tirés entre 1 et 20 mètres du filet. De plus, les tirs sont généralement transformés en but lorsque le tir est relativement proche, soit à moins de 15m. Cependant, on constate qu'il n'y a aucun but à plus de 70m du filet.

![image](/public/shots_goals_visualizations/histogramme_tirs_angle.png)

On remarque qu'il y a une forte concentration de tirs à un angle de 0 ou bien entre -20 et -40 degrés ainsi que 20 et 40 degrés. Ce diagramme démontre aussi que les tirs ont plus de chance de se transformer en but si l'angle est nul (0 degré) ou bien faible (`-20` - `-40` degrés ou `20` - `40` degrés).

![image](/public/shots_goals_visualizations/histogramme_tirs_distance_angle.png)

Cet histogramme démontre la relation entre la distance et l'angle pour les tirs. On remarque grâce à cet histogramme, que les tirs ont une plus grande probabilité de but lorsque l'angle est proche de 0 (entre `-50` et `50` degrés) et que la distance est inférieure à 60 mètres. L'intersection où un tir a le plus souvent été converti en but est avec un angle compris entre 0 et 10 degrés et une distance d'environ 10 mètres du filet.

![image](/public/shots_goals_visualizations/taux_buts_distance.png)

Cette figure montre que le taux de but diminue au fur et à mesure que la distance par rapport au filet augmente. Cela confirme notamment l'impression perçue en observant les figures précédentes, car il semblerait qu'au delà de 10 mètres du filet, le taux de but est très faible.

![image](/public/shots_goals_visualizations/taux_buts_angle.png)

Grâce à cette figure, on remarque que les taux de but est assez conséquent lorsque l'angle par rapport au filet est très grand (> 100 degrés) ou lorsque l'angle est très petit (0 - 10 degrés).

![image](/public/shots_goals_visualizations/histogramme_buts_distance.png)

Cet histogramme montre qu'il y a beaucoup moins de tirs effectués face à un filet vide que de tirs effectués face à un filet non vide. On remarque aussi que les buts ont majoritairement eu lieu lorsque le tir s'est trouvé à une distance comprise entrre 10 et 20 métres du filet. Cela confirme d'autant plus les conjectures émises plus tôt, c'est-à-dire que les buts probiennent majoritairement de tirs effectués proche du filet. 

En observant le *dataframe* contenant tous les événements de chaque match, nous avons pris un échantillon au hasard parmis les événements de tir qui sont catégorisé comme "but dans un filet vide" et avons analysé les buts via des vidéos *highlights* des matchs concernés sur YouTube. Dans l'échantillon anaylsé, chaque tir décrit dans les données comme étant face à un filet vide était correctement classifié. Nous avons donc trouvé aucune donnée anormale, et une recherche plus approfondie est nécessaire afin de distinguer les données anormales des données saines.
