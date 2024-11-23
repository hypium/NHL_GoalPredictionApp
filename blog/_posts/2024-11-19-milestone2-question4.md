---
layout: post
title: Ingénierie des caractéristiques II
milestone: 2
question: 4
auteurs: Daniel Lofeodo
---
Maintenant que nous avons obtenu des résultats de base, plusieurs caractéristiques supplémentaires ont été intégrées. Cela inclut des caractéristiques déjà disponibles dans le jeu de données nettoyé lors de l'étape 1, ainsi que de nouvelles fonctionnalités créées à partir d'informations combinées provenant d'autres caractéristiques. Les caractéristiques suivantes ont été rajoutées:

| Caractéristique         | Description                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| game_id                  | Identifiant unique du jeu.                                                                              |
| play_num                 | Numéro du play dans le jeu.                                                                            |
| period                   | Période dans laquelle le play a eu lieu.                                                               |
| is_goal                  | Indique si le tir a été un but (valeur binaire).                                                      |
| x_coord                  | Coordonnée x du joueur sur la patinoire, normalisé sur un côté, en pieds.                           |
| y_coord                  | Coordonnée y du joueur sur la patinoire, en pieds.                                                     |
| shot_type                | Type de tir (slap, snap, tip-in, wrist, etc.).                                                          |
| is_empty_net             | Si le guardient de but était absent dans le filet (valeur binaire).                                    |
| distance                 | Distance en pieds entre le joueur et le filet au moment du play.                                       |
| angle_to_goal            | Angle en degrés entre le joueur et le filet.                                                           |
| game_seconds             | Temps écoulé en secondes depuis le début du jeu.                                                    |
| last_event_type          | Type de l'événement précédent (code d'indetification).                                              |
| last_event_x_coord       | Coordonéées x en pieds du play précédent.                                                          |
| last_event_y_coord       | Coordonéées y en pieds du play précédent.                                                           |
| time_since_last_event    | Temps ecoulées en secondes depuis le dernier play.                                                     |
| distance_from_last_event | Distance en pieds parcourue depuis le dernier play.                                                   |
| rebound                  | Indique si le dernier play était également un tir (valeur booléenne).                                |
| angle_change             | Changement d'angle en degrés entre le dernier play et le tir actuel.                                   |
| speed                    | Vitesse en pieds par seconde (distance parcourue depuis le dernier play divisée par le temps écoulé) |
| time_since_powerplay     | Temps écoulé en secondes depuis qu'une équipe est en powerplay (0 si aucune équipe).                |
| away_skaters             | Nombre de joueurs de l'équipe adverse sur la glace.                                                    |
| home_skaters             | Nombre de joueurs de l'équipe résidente sur la glace.                                                 |

Une dataframe complète contenant tous les tirs du jeu de Winnipeg vs. Washington du 12 mars 2018 peut être accédée en suivant le lien suivant: [wpg_v_wsh_2017021065](https://wandb.ai/IFT6758-2024-A02/IFT6758.2024-A02/artifacts/dataset/wpg_v_wsh_2017021065/v0/files/wpg_v_wsh_2017021065.table.json).
