import gradio as gr
import random as rd
import numpy as np

CARAC = ['Force', 'Dextérité', 'Intelligence', 'Présence', 'Perception']

# --- Core logic ---
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

# --- Function to be called by Gradio ---
def generate_stats(base_pts, base_corps, mode):
    pts_to_reroll = base_pts - (base_corps - 2)
    base_stats = [2, 2, 2, 2, 2]

    if mode == "Équilibré":
        new_stats = reroll_stats(pts_to_reroll, base_stats)
    else:
        new_stats = reroll_stats_extr(pts_to_reroll, base_stats)

    results = "\n".join(f"{CARAC[i]} : {new_stats[i]}" for i in range(len(new_stats)))
    return results

# --- Gradio interface ---
with gr.Blocks(title="Générateur de stats JdR") as demo:
    gr.Markdown("## 🎲 Générateur de statistiques JdR\nEntrez vos paramètres puis cliquez sur **Générer**.")

    base_pts = gr.Number(label="Nombre total de points à répartir", value=48)
    base_corps = gr.Number(label="Valeur de Corps", value=10)
    mode = gr.Radio(["Équilibré", "Extrême"], label="Mode de répartition", value="Équilibré")
    
    generate_button = gr.Button("Générer les statistiques")
    output_box = gr.Textbox(label="Résultat", lines=10)

    generate_button.click(fn=generate_stats, inputs=[base_pts, base_corps, mode], outputs=output_box)

demo.launch(share=True)
