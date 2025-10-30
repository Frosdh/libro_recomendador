# 📚 Sistema de Recomendación de Libros con Aprendizaje

Sistema interactivo de recomendación basado en aprendizaje por refuerzo simulado con estrategia ε-greedy.

## 🚀 Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución
```bash
streamlit run app.py
```

## 🎯 Características

- **Aprendizaje por Refuerzo Simulado**: Estrategia ε-greedy
- **Interfaz Visual Llamativa**: Colores vibrantes (rojo, celeste, amarillo)
- **Análisis en Tiempo Real**: Métricas y gráficos interactivos
- **Documentación Completa**: Pseudocódigo y análisis incluido

## 📊 Componentes

1. **Agente Interactivo**: Obtén recomendaciones y califica libros
2. **Matriz de Conocimiento**: Visualiza calificaciones y similitudes
3. **Análisis**: Ventajas, limitaciones y aplicaciones reales
4. **Documentación**: Pseudocódigo y explicación técnica

## 🧠 Algoritmo

El sistema usa **ε-greedy**:
- **Exploración (ε)**: Recomienda libros aleatorios para descubrir preferencias
- **Explotación (1-ε)**: Recomienda libros similares usando similitud coseno
- **Aprendizaje**: ε disminuye gradualmente para favorecer explotación