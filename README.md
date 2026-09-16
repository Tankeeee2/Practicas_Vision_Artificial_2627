# Prácticas de Fundamentos de Sistemas de Imagen y Visión (FSIV)

Repositorio de prácticas de la asignatura **Fundamentos de Sistemas de Imagen y Visión (FSIV)** del Grado en Ingeniería Informática (Mención en Computación), Escuela Politécnica Superior de Córdoba (**EPS-UCO**).

Curso Académico: **2026 / 2027**

---

## 📌 Descripción de la Asignatura y Prácticas

La parte práctica de la asignatura está orientada al diseño, implementación y experimentación con algoritmos fundamentales de **Visión por Computador** y **Procesamiento Digital de Imágenes**.

A lo largo del curso se profundiza de forma progresiva en:
- Representación, espacios de color (RGB, HSV, escala de grises) y conversión de rangos dinámicos.
- Operaciones radiométricas de punto: ajuste de contraste, brillo, corrección gamma y ecualización de histogramas.
- Filtrado espacial lineal y no lineal, detección de gradientes, bordes y convolución.
- Segmentación por umbralización, máscaras cromáticas y análisis morfológico.
- Detección y descripción de características, transformaciones geométricas y visión estéreo / seguimiento.

---

## 🛠️ Tecnologías y Herramientas

- **Lenguaje:** C++ (estándar C++17 o superior).
- **Biblioteca central:** [OpenCV](https://opencv.org/) (Open Source Computer Vision Library).
- **Sistema de construcción:** [CMake](https://cmake.org/) (versión 3.10+).
- **Compilador:** `gcc` / `g++` sobre Linux.

---

## 📁 Estructura del Repositorio

Cada práctica se gestiona de manera modular e independiente con su propia configuración de CMake:

```text
PracticasVision_2627/
├── PRACTICA_01/
│   ├── CMakeLists.txt
│   ├── src/          # Código fuente (.cpp, .hpp)
│   └── data/         # Imágenes o vídeos de prueba
├── PRACTICA_02/
│   └── ...
└── README.md
```

---

## ⚙️ Compilación y Ejecución

Para compilar cualquiera de los proyectos con CMake:

1. Entrar en el directorio de la práctica concreta:
   ```bash
   cd PRACTICA_XX
   ```

2. Configurar el directorio de construcción:
   ```bash
   cmake -B build
   ```

3. Compilar el proyecto:
   ```bash
   cmake --build build
   ```

4. Ejecutar el binario generado con sus argumentos e imágenes correspondientes:
   ```bash
   ./build/nombre_ejecutable [opciones] [ruta_imagen]
   ```

---

## 💡 Buenas Prácticas

- Mantener la separación entre el código fuente, los datos de entrada/prueba y el directorio `build/`.
- Gestión de parámetros por línea de comandos mediante `cv::CommandLineParser`.
- No subir binarios ni carpetas de construcción al control de versiones.
