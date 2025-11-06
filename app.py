import streamlit as st
import numpy as np
import pandas as pd
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Agente de Recomendación con Aprendizaje",
    page_icon=" ",
    layout="wide"
)

# Inicialización de datos
# Inicialización de datos
@st.cache_data
def get_books():
    return [
        # --- REALISMO MÁGICO ---
        {"id": 1, "title": "Cien años de soledad", "author": "Gabriel García Márquez", "genre": "Realismo mágico"},
        {"id": 8, "title": "Rayuela", "author": "Julio Cortázar", "genre": "Realismo mágico"},
        {"id": 11, "title": "Pedro Páramo", "author": "Juan Rulfo", "genre": "Realismo mágico"},
        {"id": 12, "title": "La casa de los espíritus", "author": "Isabel Allende", "genre": "Realismo mágico"},

        # --- DISTOPÍA ---
        {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Distopía"},
        {"id": 13, "title": "Un mundo feliz", "author": "Aldous Huxley", "genre": "Distopía"},
        {"id": 14, "title": "Fahrenheit 451", "author": "Ray Bradbury", "genre": "Distopía"},

        # --- FILOSOFÍA ---
        {"id": 3, "title": "El principito", "author": "Antoine de Saint-Exupéry", "genre": "Filosofía"},
        {"id": 15, "title": "Meditaciones", "author": "Marco Aurelio", "genre": "Filosofía"},
        {"id": 16, "title": "Así habló Zaratustra", "author": "Friedrich Nietzsche", "genre": "Filosofía"},
        {"id": 17, "title": "La república", "author": "Platón", "genre": "Filosofía"},

        # --- HISTORIA ---
        {"id": 4, "title": "Sapiens", "author": "Yuval Noah Harari", "genre": "Historia"},
        {"id": 18, "title": "Homo Deus", "author": "Yuval Noah Harari", "genre": "Historia"},
        {"id": 19, "title": "Los pilares de la Tierra", "author": "Ken Follett", "genre": "Historia"},
        {"id": 20, "title": "Breve historia del tiempo", "author": "Stephen Hawking", "genre": "Historia"},

        # --- ROMANCE ---
        {"id": 5, "title": "Orgullo y prejuicio", "author": "Jane Austen", "genre": "Romance"},
        {"id": 21, "title": "Romeo y Julieta", "author": "William Shakespeare", "genre": "Romance"},
        {"id": 22, "title": "Bajo la misma estrella", "author": "John Green", "genre": "Romance"},
        {"id": 23, "title": "Posdata: Te amo", "author": "Cecelia Ahern", "genre": "Romance"},

        # --- SUSPENSO / MISTERIO ---
        {"id": 6, "title": "El código Da Vinci", "author": "Dan Brown", "genre": "Suspenso"},
        {"id": 9, "title": "La sombra del viento", "author": "Carlos Ruiz Zafón", "genre": "Suspenso"},
        {"id": 24, "title": "Asesinato en el Orient Express", "author": "Agatha Christie", "genre": "Suspenso"},
        {"id": 25, "title": "El silencio de los corderos", "author": "Thomas Harris", "genre": "Suspenso"},

        # --- CIENCIA Y DIVULGACIÓN ---
        {"id": 10, "title": "El gen egoísta", "author": "Richard Dawkins", "genre": "Ciencia"},
        {"id": 26, "title": "Cosmos", "author": "Carl Sagan", "genre": "Ciencia"},
        {"id": 27, "title": "El universo en una cáscara de nuez", "author": "Stephen Hawking", "genre": "Ciencia"},
        {"id": 28, "title": "Pensar rápido, pensar despacio", "author": "Daniel Kahneman", "genre": "Ciencia"},

        # --- CIENCIA FICCIÓN ---
        {"id": 7, "title": "Dune", "author": "Frank Herbert", "genre": "Ciencia ficción"},
        {"id": 29, "title": "Fundación", "author": "Isaac Asimov", "genre": "Ciencia ficción"},
        {"id": 30, "title": "Neuromante", "author": "William Gibson", "genre": "Ciencia ficción"},
        {"id": 31, "title": "Snow Crash", "author": "Neal Stephenson", "genre": "Ciencia ficción"},

        # --- FANTASÍA ---
        {"id": 32, "title": "El señor de los anillos", "author": "J.R.R. Tolkien", "genre": "Fantasía"},
        {"id": 33, "title": "Harry Potter y la piedra filosofal", "author": "J.K. Rowling", "genre": "Fantasía"},
        {"id": 34, "title": "Las crónicas de Narnia", "author": "C.S. Lewis", "genre": "Fantasía"},
        {"id": 35, "title": "La rueda del tiempo", "author": "Robert Jordan", "genre": "Fantasía"},

        # --- POESÍA ---
        {"id": 36, "title": "Veinte poemas de amor y una canción desesperada", "author": "Pablo Neruda", "genre": "Poesía"},
        {"id": 37, "title": "Hojas de hierba", "author": "Walt Whitman", "genre": "Poesía"},
        {"id": 38, "title": "Ariel", "author": "Sylvia Plath", "genre": "Poesía"},

        # --- AUTOAYUDA / MOTIVACIÓN ---
        {"id": 39, "title": "Los 7 hábitos de la gente altamente efectiva", "author": "Stephen Covey", "genre": "Autoayuda"},
        {"id": 40, "title": "Cómo ganar amigos e influir sobre las personas", "author": "Dale Carnegie", "genre": "Autoayuda"},
        {"id": 41, "title": "El monje que vendió su Ferrari", "author": "Robin Sharma", "genre": "Autoayuda"},
        {"id": 42, "title": "Piense y hágase rico", "author": "Napoleon Hill", "genre": "Autoayuda"},

        # --- EDUCACIÓN / PSICOLOGÍA ---
        {"id": 43, "title": "El elemento", "author": "Ken Robinson", "genre": "Educación"},
        {"id": 44, "title": "La inteligencia emocional", "author": "Daniel Goleman", "genre": "Psicología"},
        {"id": 45, "title": "Mindset: La actitud del éxito", "author": "Carol Dweck", "genre": "Psicología"},
    ]


# Inicializar el estado de sesión
if 'q_table' not in st.session_state:
    books = get_books()
    q_table = {}
    for book in books:
        if book['genre'] not in q_table:
            q_table[book['genre']] = {}
        q_table[book['genre']][book['id']] = 0.0
    st.session_state.q_table = q_table

if 'history' not in st.session_state:
    st.session_state.history = []

if 'current_recommendation' not in st.session_state:
    st.session_state.current_recommendation = None

if 'total_interactions' not in st.session_state:
    st.session_state.total_interactions = 0

if 'learning_rate' not in st.session_state:
    st.session_state.learning_rate = 0.1

if 'exploration_rate' not in st.session_state:
    st.session_state.exploration_rate = 0.3

# Funciones del agente
def select_book_qlearning(books, q_table, exploration_rate):
    """Selecciona un libro usando estrategia epsilon-greedy"""
    if np.random.random() < exploration_rate:
        # Exploración: libro aleatorio
        return np.random.choice(books)
    else:
        # Explotación: mejor libro según Q-table
        best_book = None
        best_q = float('-inf')
        
        for book in books:
            q_value = q_table.get(book['genre'], {}).get(book['id'], 0)
            if q_value > best_q:
                best_q = q_value
                best_book = book
        
        return best_book if best_book else np.random.choice(books)

def update_q_value(q_table, book, reward, learning_rate):
    """Actualiza el valor Q usando la fórmula de Q-Learning"""
    genre = book['genre']
    book_id = book['id']
    
    old_q = q_table[genre][book_id]
    new_q = old_q + learning_rate * (reward - old_q)
    q_table[genre][book_id] = new_q
    
    return new_q

def get_top_genres(q_table):
    """Obtiene los géneros mejor valorados"""
    genre_scores = {}
    for genre, books in q_table.items():
        if books:
            genre_scores[genre] = np.mean(list(books.values()))
    
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_genres[:3]

# Interfaz principal
st.title(" Agente Inteligente: Sistema de Recomendación con Aprendizaje")
st.markdown("**Aprendizaje por Refuerzo (Q-Learning) aplicado a libros**")

# Descripción del problema
with st.expander(" Descripción del Problema", expanded=True):
    st.markdown("""
    El agente debe **aprender las preferencias del usuario** sobre libros mediante la interacción.
    Utiliza **Q-Learning**, un algoritmo de aprendizaje por refuerzo donde el agente:
    
    - **Explora**: Recomienda libros aleatorios inicialmente
    - **Aprende**: Ajusta valores Q según feedback ( = +1,  = -1)
    - **Explota**: Prioriza géneros y libros con mejor puntuación
    """)

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(" Interacciones", st.session_state.total_interactions)

with col2:
    success_count = len([h for h in st.session_state.history if h['feedback'] == 'Positivo'])
    success_rate = (success_count / st.session_state.total_interactions * 100) if st.session_state.total_interactions > 0 else 0
    st.metric(" Tasa de Éxito", f"{success_rate:.1f}%")

with col3:
    st.metric(" Exploración", f"{st.session_state.exploration_rate * 100:.0f}%")

# Layout principal
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader(" Recomendación del Agente")
    
    if st.session_state.current_recommendation is None:
        if st.button(" Obtener Recomendación", type="primary", use_container_width=True):
            books = get_books()
            book = select_book_qlearning(books, st.session_state.q_table, st.session_state.exploration_rate)
            st.session_state.current_recommendation = book
            st.rerun()
    else:
        book = st.session_state.current_recommendation
        
        # Mostrar libro recomendado
        st.info(f"""
        ###  {book['title']}
        **Autor:** {book['author']}  
        **Género:** {book['genre']}  
        **Q-Value:** {st.session_state.q_table[book['genre']][book['id']]:.3f}
        """)
        
        # Botones de feedback
        col_like, col_dislike = st.columns(2)
        
        with col_like:
            if st.button(" Me gusta", use_container_width=True):
                new_q = update_q_value(st.session_state.q_table, book, 1, st.session_state.learning_rate)
                
                st.session_state.history.append({
                    'book': book['title'],
                    'genre': book['genre'],
                    'feedback': 'Positivo',
                    'q_value': f"{new_q:.3f}",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                
                st.session_state.total_interactions += 1
                st.session_state.exploration_rate = max(0.05, st.session_state.exploration_rate - 0.01)
                st.session_state.current_recommendation = None
                st.rerun()
        
        with col_dislike:
            if st.button(" No me gusta", use_container_width=True):
                new_q = update_q_value(st.session_state.q_table, book, -1, st.session_state.learning_rate)
                
                st.session_state.history.append({
                    'book': book['title'],
                    'genre': book['genre'],
                    'feedback': 'Negativo',
                    'q_value': f"{new_q:.3f}",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                
                st.session_state.total_interactions += 1
                st.session_state.exploration_rate = max(0.05, st.session_state.exploration_rate - 0.01)
                st.session_state.current_recommendation = None
                st.rerun()
    
    # Géneros preferidos
    st.subheader("🏆 Géneros Preferidos")
    top_genres = get_top_genres(st.session_state.q_table)
    
    if top_genres:
        medals = ['🥇', '🥈', '🥉']
        for i, (genre, score) in enumerate(top_genres):
            progress = max(0, min(1, (score + 1) / 2))
            st.markdown(f"{medals[i]} **{genre}** - Score: {score:.3f}")
            st.progress(progress)
    else:
        st.info("El agente aún no tiene preferencias aprendidas")

with col_right:
    st.subheader(" Historial de Aprendizaje")
    
    if st.button(" Reiniciar Agente", use_container_width=True):
        for key in ['q_table', 'history', 'current_recommendation', 'total_interactions']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.exploration_rate = 0.3
        st.rerun()
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-15:])):
            color = "green" if item['feedback'] == 'Positivo' else "red"
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 4px solid {color};'>
                <strong>{item['book']}</strong><br/>
                <small>{item['genre']} | {item['feedback']} | Q: {item['q_value']} | {item['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay interacciones aún")

# Algoritmo y análisis
st.markdown("---")
st.header(" Algoritmo Q-Learning")

col_algo, col_analysis = st.columns(2)

with col_algo:
    st.code("""
# PSEUDOCÓDIGO Q-LEARNING

1. Inicialización:
   Q(género, libro) = 0 para todos

2. Para cada interacción:
   
   a) Selección (ε-greedy):
      Si rand() < ε:
         acción = libro_aleatorio()  # Explorar
      Sino:
         acción = max_Q(libros)      # Explotar
   
   b) Ejecutar acción y obtener recompensa:
      recompensa = +1 si 
      recompensa = -1 si 
   
   c) Actualizar Q-value:
      Q_nuevo = Q_viejo + α(recompensa - Q_viejo)
      
      donde α = learning_rate (0.1)
   
   d) Reducir exploración:
      ε = max(0.05, ε - 0.01)

3. Repetir hasta convergencia
    """, language="python")

with col_analysis:
    st.success("""
    ** Ventajas**
    - Aprende de la interacción sin supervisión
    - Se adapta a preferencias cambiantes
    - No requiere datos previos de entrenamiento
    - Mejora continuamente con el uso
    """)
    
    st.warning("""
    ** Limitaciones**
    - Necesita muchas interacciones iniciales
    - Exploración puede dar malas recomendaciones
    - Sensible a hiperparámetros
    - No considera contexto temporal
    """)
    
    st.info("""
    ** Aplicaciones Reales**
    - **Netflix/Spotify:** Recomendaciones personalizadas
    - **E-commerce:** Amazon, Alibaba (productos)
    - **Publicidad:** Google Ads, Facebook (optimización)
    - **Videojuegos:** Ajuste de dificultad dinámico
    """)

# Configuración avanzada
with st.expander(" Configuración Avanzada"):
    st.session_state.learning_rate = st.slider(
        "Tasa de Aprendizaje (α)", 
        0.01, 0.5, 
        st.session_state.learning_rate,
        help="Controla qué tan rápido el agente aprende de nuevas experiencias"
    )
    
    # Mostrar Q-Table completa
    if st.checkbox("Mostrar Q-Table completa"):
        q_data = []
        for genre, books in st.session_state.q_table.items():
            for book_id, q_value in books.items():
                book_info = next((b for b in get_books() if b['id'] == book_id), None)
                if book_info:
                    q_data.append({
                        'Libro': book_info['title'],
                        'Género': genre,
                        'Q-Value': f"{q_value:.3f}"
                    })
        
        df = pd.DataFrame(q_data)
        st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Proyecto de Agentes Inteligentes y Herramientas de IA - Bloque A: Ejercicios Aplicados</small>
</div>
""", unsafe_allow_html=True)