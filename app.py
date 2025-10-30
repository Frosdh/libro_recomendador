import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="📚 Recomendador Inteligente de Libros",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado con colores llamativos
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    h1 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2, h3 {
        color: #ffffff;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de estado de sesión
if 'ratings' not in st.session_state:
    # Datos iniciales de libros
    books = [
        "Cien Años de Soledad", "1984", "El Principito", 
        "Don Quijote", "Harry Potter", "El Alquimista",
        "Orgullo y Prejuicio", "Crimen y Castigo", 
        "El Gran Gatsby", "Moby Dick"
    ]
    
    users = ["Ana", "Luis", "Carlos", "María", "José"]
    
    # Calificaciones iniciales aleatorias
    st.session_state.ratings = pd.DataFrame(
        np.random.randint(1, 6, size=(len(users), len(books))),
        index=users,
        columns=books
    )
    
    # Historial de interacciones
    st.session_state.history = []
    
    # Parámetros de aprendizaje
    st.session_state.epsilon = 0.3  # Factor de exploración
    st.session_state.total_interactions = 0
    st.session_state.rewards = []

# Título principal
st.markdown("<h1 style='text-align: center;'>📚 SISTEMA INTELIGENTE DE RECOMENDACIÓN DE LIBROS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 18px;'>Agente basado en Aprendizaje por Refuerzo Simulado</p>", unsafe_allow_html=True)

# Sidebar con información del algoritmo
with st.sidebar:
    st.markdown("### 🎯 Algoritmo de Aprendizaje")
    st.markdown("""
    <div class='info-box'>
    <b>Estrategia ε-greedy:</b><br>
    • <b>Exploración (ε)</b>: Recomienda libros aleatorios<br>
    • <b>Explotación (1-ε)</b>: Usa similitud coseno<br>
    • Se adapta con cada interacción
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Métricas de Aprendizaje")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Interacciones", st.session_state.total_interactions, 
                 delta="+1" if st.session_state.total_interactions > 0 else None)
    with col2:
        epsilon_pct = int(st.session_state.epsilon * 100)
        st.metric("Exploración", f"{epsilon_pct}%")
    
    if st.session_state.rewards:
        avg_reward = np.mean(st.session_state.rewards[-10:])
        st.metric("Recompensa Promedio", f"{avg_reward:.2f}")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Agente Interactivo", "📈 Matriz de Conocimiento", "🧠 Análisis", "📖 Documentación"])

with tab1:
    st.markdown("## 🤖 Interacción con el Agente")
    
    col1, col2 = st.columns([2, 1])
    
   
with tab4:
    st.markdown("## 📖 Documentación Técnica")
    
    st.markdown("""
    <div class='info-box'>
    <h3>🎯 Descripción del Problema</h3>
    <p>
    Un sistema de recomendación debe sugerir libros relevantes a usuarios basándose en sus preferencias.
    El desafío es balancear entre recomendar libros conocidos (explotación) y descubrir nuevos intereses (exploración).
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
    <h3>⚙️ Algoritmo Implementado: ε-Greedy</h3>
    <pre style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;'>
PSEUDOCÓDIGO:

Inicializar:
    ε = 0.3  // Factor de exploración inicial
    ratings = matriz_de_calificaciones()
    
Función recomendar(usuario):
    si random() < ε:
        // EXPLORACIÓN
        libro = seleccionar_aleatorio(libros)
    sino:
        // EXPLOTACIÓN
        mejor_libro = max_calificado(usuario)
        similitud = calcular_similitud_coseno(ratings)
        libro = más_similar(mejor_libro, similitud)
    
    retornar libro

Función actualizar_conocimiento(usuario, libro, calificación):
    // Actualizar matriz de conocimiento
    ratings[usuario][libro] = calificación
    
    // Calcular recompensa
    reward = (calificación - 1) / 4  // Normalizar [0, 1]
    
    // Decrementar exploración (más explotación con el tiempo)
    ε = max(0.1, ε × 0.95)
    
    retornar reward
    </pre>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='warning-box'>
    <h3>🔬 Componentes del Sistema</h3>
    <ol>
        <li><b>Matriz de Conocimiento:</b> Almacena calificaciones usuario-libro</li>
        <li><b>Similitud Coseno:</b> Mide similitud entre libros basada en patrones de calificación</li>
        <li><b>Estrategia ε-greedy:</b> Balance entre exploración y explotación</li>
        <li><b>Sistema de Recompensas:</b> Feedback para mejorar recomendaciones</li>
        <li><b>Decaimiento de ε:</b> Reduce exploración gradualmente</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white;'>
    <p>🚀 Sistema Inteligente de Recomendación | Desarrollado con Streamlit & Python</p>
    <p>💡 Aprendizaje por Refuerzo Simulado con estrategia ε-greedy</p>
</div>
""", unsafe_allow_html=True)