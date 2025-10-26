import streamlit as st
import random as rd
import numpy as np
import plotly.graph_objects as go

def reroll_stats(pts_to_reroll, base_stats):
    new_stats = base_stats.copy()
    for _ in range(pts_to_reroll):
        new_stats[rd.randint(0, len(base_stats)-1)] += 1
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


# --- Interface Streamlit ---

st.title("🎲 Générateur de répartition de stats JdR")
st.write("Répartissez vos points de caractéristiques selon deux modes : équilibré ou extrême.")

CARAC = ['Force', 'Dextérité', 'Intelligence', 'Présence', 'Perception']

# Entrées utilisateur
base_pts = st.number_input("Nombre total de points à répartir :", min_value=1, max_value=100, value=48)
base_corps = st.number_input("Valeur de Corps :", min_value=2, max_value=18, value=10)
mode = st.radio("Mode de répartition :", ["Équilibré", "Extrême"])

# Calcul du nombre de points à répartir sur les 5 stats
pts_to_reroll = base_pts - (base_corps - 2)
base_stats = [2, 2, 2, 2, 2]

if st.button("🎲 Générer les stats !"):
    if mode == "Équilibré":
        new_stats = reroll_stats(pts_to_reroll, base_stats)
    else:
        new_stats = reroll_stats_extr(pts_to_reroll, base_stats)

    st.subheader("Résultat :")
    for i in range(len(new_stats)):
        st.write(f"**{CARAC[i]}** : {new_stats[i]}")

    colors = []
    for val in new_stats:
        if val >= 15:
            colors.append("blue")
        elif val >= 12:
            colors.append("green")
        elif val >= 9:
            colors.append("yellow")
        elif val >= 6:
            colors.append("orange")
        else:
            colors.append("red")

    # Graphique Plotly
    fig = go.Figure(go.Bar(
        x=CARAC,
        y=new_stats,
        marker_color=colors
    ))

    fig.update_layout(
        yaxis=dict(range=[0,18], title="Valeur"),
        title="Répartition des statistiques",
        xaxis_title="Caractéristique"
    )

    st.plotly_chart(fig)