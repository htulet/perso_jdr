import random as rd
import numpy as np

CARAC = ['Force', 'Dextérité', 'Intelligence', 'Présence', 'Perception']

def reroll_stats(pts_to_reroll, base_stats):
    new_stats = base_stats.copy()
    for _ in range(pts_to_reroll):
        new_stats[rd.randint(0, len(base_stats)-1)]+=1
    
    if max(new_stats) > 18:
        return reroll_stats(pts_to_reroll, base_stats)
    else:
        return new_stats

def reroll_stats_extr(pts_to_reroll, base_stats):
    new_stats = base_stats.copy()
    for _ in range(pts_to_reroll):
        weights = [s for s in new_stats] 
        chosen = rd.choices(range(len(new_stats)), weights=weights)[0]
        new_stats[chosen] += 1

    if max(new_stats) > 18:
        return reroll_stats_extr(pts_to_reroll, base_stats)

    return new_stats


base_pts = 48
base_corps = 10

base_pts-= (base_corps - 2)

base_stats = [2, 2, 2, 2, 2]

new_stats = reroll_stats_extr(base_pts, base_stats)
for i in range(len(new_stats)):
    print(f"{CARAC[i]} : {new_stats[i]}")
print("\n")