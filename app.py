import streamlit as st
import pandas as pd
import os

# Configuración de la pestaña del navegador
st.set_page_config(
    page_title="Verificación de Participantes",
    page_icon="🎓",
    layout="centered"
)

# --- ESTILOS VISUALES PARA LA INTERFAZ ---
st.markdown("""
    <style>
    .main-title {
        color: #0F172A;
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #475569;
        font-size: 14px;
        text-align: center;
        margin-bottom: 25px;
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 20px;
    }
    .datos-box {
        background-color: #F8FAFC;
        border: 1px dashed #64748B;
        padding: 14px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .btn-whatsapp {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        font-weight: bold;
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 6px;
        text-align: center;
        font-size: 15px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease;
    }
    .btn-whatsapp:hover {
        background-color: #128C7E;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado visual
st.markdown('<div class="main-title">🎓 Verificación de Participantes</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ingrese su número de documento para validar su acreditación</div>', unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL ARCHIVO EXCEL ---
EXCEL_FILE = "nomina_egresados2025.xlsx"

# Enlaces de WhatsApp a los grupos de atención
# (Reemplace estos enlaces por los enlaces reales de invitación)
ENLACE_WHATSAPP = "https://chat.whatsapp.com/K5XNthkg9QC8swVwl8K0KV"

@st.cache_data
def cargar_datos(ruta_archivo):
    try:
        df = pd.read_excel(ruta_archivo, dtype={'N° de Cédula': str})
        df['N° de Cédula'] = df['N° de Cédula'].str.strip()
        return df, None
    except Exception as e:
        return None, str(e)

# Control de presencia del archivo
if not os.path.exists(EXCEL_FILE):
    st.info(f"💡 Archivo '{EXCEL_FILE}' no detectado en el repositorio.")
    st.stop()

df_datos, error_carga = cargar_datos(EXCEL_FILE)
if error_carga:
    st.error(f"❌ Error al abrir la nómina: {error_carga}")
    st.stop()

# Validación de las 4 columnas estructurales
columnas_requeridas = ['N° de Cédula', 'Nombre y Apellido', 'Curso Culminado', 'Cohorte']
columnas_faltantes = [col for col in columnas_requeridas if col not in df_datos.columns]
if columnas_faltantes:
    st.error(f"❌ La planilla Excel requiere las siguientes columnas exactas: {', '.join(columnas_faltantes)}")
    st.stop()

# --- INTERFAZ DE BÚSQUEDA ---
with st.form(key="form_consulta"):
    cedula_in = st.text_input(
        "Número de Cédula de Identidad:",
        placeholder="Ej: 1234567 (sin puntos)",
        help="Ingrese los dígitos de su documento de identidad sin puntos ni guiones."
    )
    btn_consultar = st.form_submit_button(label="🔍 Verificar Datos")

# --- PROCESAMIENTO ---
if btn_consultar or st.session_state.get('verificado', False):
    cedula_limpia = cedula_in.strip().replace(".", "").replace("-", "")
    
    if not cedula_limpia:
        st.warning("⚠️ Ingrese un número de cédula válido.")
    else:
        fila = df_datos[df_datos['N° de Cédula'] == cedula_limpia]
        
        if not fila.empty:
            st.session_state['verificado'] = True
            registro = fila.iloc[0]
            
            nombre = registro['Nombre y Apellido']
            ci = registro['N° de Cédula']
            curso = registro['Curso Culminado']
            cohorte = registro['Cohorte']
            
            st.success("✅ ¡Identidad Verificada! El registro figura en la nómina oficial.")
            
            # Retorno en filas ordenadas
            st.markdown("### 📋 Información del Participante:")
            st.write(f"**Nombre y Apellido:** {nombre}")
            st.write(f"**Número de Cédula:** {ci}")
            st.write(f"**Curso Culminado:** {curso}")
            st.write(f"**Cohorte:** {cohorte}")
            
            st.markdown("---")
            st.info("👋 Copie el siguiente bloque y envíelo al unirse al grupo de WhatsApp:")
            
            # Formato de texto para el portapapeles
            texto_copiar = (
                f"SOLICITUD DE MATRICULACIÓN:\n"
                f"• Nombre y Apellido: {nombre}\n"
                f"• Número de Cédula: {ci}\n"
                f"• Curso Culminado: {curso}\n"
                f"• Cohorte: {cohorte}\n"
                f"• Verificación: EXITOSA"
            )
            st.markdown(f'<div class="datos-box"><code style="color: #0F172A; font-weight: bold; white-space: pre-wrap;">{texto_copiar}</code></div>', unsafe_allow_html=True)
            
            confirmado = st.checkbox("👉 Confirmo que copié los datos y los enviaré al ingresar al grupo.")
            
            # Detección de perfil por palabra clave en el curso
          if confirmado:
    st.markdown(f'<a href="{ENLACE_WHATSAPP}" target="_blank" class="btn-whatsapp">💬 Unirse al Grupo de WhatsApp</a>', unsafe_allow_html=True)
            else:
                st.warning("🔒 Marque la casilla de confirmación para habilitar el botón de acceso.")
        else:
            st.session_state['verificado'] = False
            st.error("❌ El documento ingresado no figura en la nómina.")
            st.info("ℹ️ Si concluyó el curso y no figura en la lista, contacte a la coordinación académica.")

# Pie de página institucional
st.markdown("---")
st.markdown('<div class="footer">Sistema de Validación Institucional © 2026</div>', unsafe_allow_html=True)
