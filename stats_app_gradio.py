import gradio as gr
import random as rd
import plotly.graph_objects as go

CARAC = ['Force', 'Dextérité', 'Intelligence', 'Présence', 'Perception']

def reroll_stats(pts_to_reroll, base_stats):
    new_stats = base_stats.copy()
    for _ in range(pts_to_reroll):
        new_stats[rd.randint(0, len(base_stats)-1)] += 1
    if max(new_stats) > 18:
        return reroll_stats(pts_to_reroll, base_stats)
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

# Fonction pour générer le graphique
def generate_stats_chart(base_pts, base_corps, mode):
    pts_to_reroll = base_pts - (base_corps - 2)
    base_stats = [2, 2, 2, 2, 2]

    if mode == "Équilibré":
        new_stats = reroll_stats(pts_to_reroll, base_stats)
    else:
        new_stats = reroll_stats_extr(pts_to_reroll, base_stats)

    # Couleurs selon valeur
    colors = []
    for val in new_stats:
        if val >= 16:
            colors.append("blue")
        elif val >= 12:
            colors.append("green")
        elif val >= 9:
            colors.append("yellow")
        elif val >= 6:
            colors.append("orange")
        else:
            colors.append("red")

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

    return fig

# --- Interface Gradio ---
with gr.Blocks() as demo:
    gr.Markdown("## 🎲 Générateur de statistiques JdR avec graphique coloré")

    base_pts = gr.Number(label="Nombre total de points à répartir", value=48)
    base_corps = gr.Number(label="Valeur de Corps", value=10)
    mode = gr.Radio(["Équilibré", "Extrême"], label="Mode de répartition", value="Équilibré")

    generate_button = gr.Button("Générer")
    output_chart = gr.Plot(label="Graphique des statistiques")

    generate_button.click(fn=generate_stats_chart, inputs=[base_pts, base_corps, mode], outputs=output_chart)

demo.launch(share=True)
