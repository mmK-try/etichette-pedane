import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
import datetime
import os

def genera_pdf_professionale(dati):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # [cite_start]Coordinate calibrate per il tuo foglio (4 etichette) [cite: 1, 2]
    quadranti = [
        (0, height/2),       # In alto a sinistra
        (width/2, height/2), # In alto a destra
        (0, 0),              # In basso a sinistra
        (width/2, 0)         # In basso a destra
    ]

    for i, scheda in enumerate(dati):
        if scheda['attiva']:
            x_off, y_off = quadranti[i]
            
            # Logo (deve essere presente nella cartella come logo.png)
            if os.path.exists("logo.png"):
                c.drawImage("logo.png", x_off + 15*mm, y_off + 75*mm, width=70*mm, preserveAspectRatio=True, mask='auto')
            
            # [cite_start]Linea estetica BS Meccanica [cite: 1, 2]
            c.setStrokeColorRGB(0.8, 0, 0) 
            c.line(x_off + 10*mm, y_off + 70*mm, x_off + 95*mm, y_off + 70*mm)
            
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 12)
            # [cite_start]Inserimento dati basati sul tuo template [cite: 1, 2]
            c.drawString(x_off + 15*mm, y_off + 62*mm, f"ORD. Nr: {scheda['ordine']}")
            c.drawString(x_off + 60*mm, y_off + 62*mm, f"del: {scheda['data']}")
            
            c.setFont("Helvetica", 11)
            c.drawString(x_off + 15*mm, y_off + 50*mm, f"Disegno: {scheda['disegno']}")
            c.drawString(x_off + 15*mm, y_off + 40*mm, f"Quantità: {scheda['quantita']}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFACCIA ---
st.set_page_config(page_title="BS Meccanica Smart Label", page_icon="⚙️")
st.title("Generatore Etichette BS Meccanica")

# Pannello di controllo laterale
with st.sidebar:
    st.header("⚙️ Impostazioni")
    ord_def = st.text_input("Ordine predefinito")
    data_def = st.date_input("Data predefinita", datetime.date.today())

dati_finali = []
# [cite_start]Layout a due colonne per richiamare la struttura del foglio [cite: 1, 2]
col1, col2 = st.columns(2)

for i in range(4):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.subheader(f"Etichetta {i+1}")
        attiva = st.checkbox(f"Stampa etichetta {i+1}", value=True, key=f"att_{i}")
        ord_val = st.text_input("ORD. Nr", value=ord_def, key=f"o_{i}")
        data_val = st.text_input("Data", value=data_def.strftime("%d/%m/%Y"), key=f"d_{i}")
        dis_val = st.text_input("Disegno", key=f"dis_{i}")
        qta_val = st.text_input("Quantità", key=f"q_{i}")
        dati_finali.append({"attiva": attiva, "ordine": ord_val, "data": data_val, "disegno": dis_val, "quantita": qta_val})

if st.button("Genera PDF per Stampa", use_container_width=True):
    pdf = genera_pdf_professionale(dati_finali)
    st.download_button(label="📥 Scarica PDF Pronto", data=pdf, file_name="stampa_bs.pdf", mime="application/pdf")