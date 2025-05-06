import streamlit as st
import pandas as pd
import matplotlib.pyplot
import plotly.express as px
import altair as alt

st.title("DataNest: the smart place for smart data")

file_caricato=st.file_uploader("Upload a CSV/XLSX file:", type=["csv", "xlsx"])

# Inizializza la session_state
if "dataset_originale" not in st.session_state:
    st.session_state.dataset_originale=None
if "dataset_modificato" not in st.session_state:
    st.session_state.dataset_modificato=None
# Inizializza variabile per popup annulla
if "mostra_popup_annulla" not in st.session_state:
    st.session_state.mostra_popup_annulla=False

if file_caricato is not None:
    if file_caricato.name.endswith(".csv"):
        st.session_state.dataset_originale=pd.read_csv(file_caricato)
    elif file_caricato.name.endswith(".xlsx"):
        st.session_state.dataset_originale=pd.read_excel(file_caricato)
    # Se il dataset originale è stato caricato, copia in dataset_modificato
    if st.session_state.dataset_originale is not None:
        st.session_state.dataset_modificato=st.session_state.dataset_originale.copy()
    st.write("The file was uploaded successfully!")
    # Paragrafo n°1: Data Preview
    st.subheader("Data Preview")
    st.text("In this section, you can view and, if you wish, edit any data you want.")
    scelta_dataset_modificabile=st.checkbox("Check here if you want to be able to edit the attached file.")
    if scelta_dataset_modificabile==True:
        st.success("⚠️ The file can be edited! Uncheck the option above if you don't want that.")
        st.session_state.dataset_modificato=st.data_editor(st.session_state.dataset_modificato, num_rows="dynamic")
    else:
        st.error("⚠️ The file is NOT editable! Check the option above if you want to change that.")
        st.dataframe(st.session_state.dataset_originale)
    if scelta_dataset_modificabile==True:
        pulsante_annulla_modifiche=st.button("Cancel the changes on the file", key="pulsante_annulla_modifiche")
        if pulsante_annulla_modifiche:
            st.session_state.mostra_popup_annulla=True
        if st.session_state.mostra_popup_annulla==True:
            with st.container():
                st.warning("Are you sure you want to cancel all the changes made to the file?")
                colonna_conferma_operazione, colonna_annulla_operazione=st.columns(2)
                with colonna_conferma_operazione:
                    pulsante_colonna_conferma_operazione=st.button("OK, I’m sure")
                    if pulsante_colonna_conferma_operazione==True:
                        st.session_state.dataset_modificato=st.session_state.dataset_originale.copy()
                        st.success("⚠️ Changes successfully canceled!")
                        st.session_state.mostra_popup_annulla=False
                        st.write("The file has been restored to its original version:")
                        st.dataframe(st.session_state.dataset_originale, use_container_width=True)
                with colonna_annulla_operazione:
                        pulsante_colonna_annulla_operazione=st.button("No, stop the current operation")
                        if pulsante_colonna_annulla_operazione==True:
                            st.success("⚠️ The operation has been canceled. The changes to the file were not removed.")
                            st.session_state.mostra_popup_annulla=False
    # Paragrafo n°2: Data Summary
    st.subheader("Data Summary")
    st.write("In this section, you can view a summary of your data, including basic statistics and information about the file.")
    if scelta_dataset_modificabile==True:
        dataset_finale=st.session_state.dataset_modificato
    else:
        dataset_finale=st.session_state.dataset_originale
    st.write(dataset_finale.describe())
    # Paragrafo n°3: Filter Data
    st.subheader("Filter Data")
    st.write("In this section, you can filter your data based on specific values in one of the columns. Select a column and then a value to filter by.")
    lista_colonne_dataset=dataset_finale.columns.tolist()
    colonna_selezionata_menu=st.selectbox("Select a column to filter the data:", lista_colonne_dataset)
    valori_unici_dataset=dataset_finale[colonna_selezionata_menu].unique()
    valore_selezionato_menu=st.selectbox("Select a value to filter the data:", valori_unici_dataset)
    dataset_finale_filtrato=dataset_finale[dataset_finale[colonna_selezionata_menu]==valore_selezionato_menu]
    st.write(dataset_finale_filtrato)
    # Paragrafo n°4: Plot Data
    st.subheader("Plot Data")
    st.write("In this section, you can create different types of charts to visualize the data. Choose the columns you want to plot and select the chart type.")
    valore_asse_x_colonna=st.selectbox("Select the column to use for the X axis in the chart:", lista_colonne_dataset)
    valore_asse_y_colonna=st.selectbox("Select the column to use for the Y axis in the chart:", lista_colonne_dataset)
    pulsante_genera_grafici=st.button("Generate plots (charts)")
    # Grafici a linee
    st.write("Line charts:")
    st.line_chart(dataset_finale.set_index(valore_asse_x_colonna)[valore_asse_y_colonna])
    grafico_linea_interattivo=px.line(dataset_finale, x=valore_asse_x_colonna, y=valore_asse_y_colonna, markers=True)
    st.plotly_chart(grafico_linea_interattivo)
    # Grafici a barre
    st.write("Bar charts:")
    st.bar_chart(dataset_finale.set_index(valore_asse_x_colonna)[valore_asse_y_colonna])
    grafico_barre_ordinato=px.bar(dataset_finale.sort_values(by=valore_asse_y_colonna), x=valore_asse_y_colonna, y=valore_asse_x_colonna, orientation="h")
    st.plotly_chart(grafico_barre_ordinato)
    # Grafici a aree
    st.write("Area charts:")
    st.area_chart(dataset_finale.set_index(valore_asse_x_colonna)[valore_asse_y_colonna])
else:
    st.write("Waiting for file upload...")
    st.write("No file uploaded yet.")