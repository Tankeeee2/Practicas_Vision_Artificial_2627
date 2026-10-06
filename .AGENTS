# Normativa de Entrega de Prácticas — Visión Artificial (FSIV 26/27)

Este documento establece las directrices obligatorias y protocolos de entrega para las prácticas de Fundamentos de Sistemas de Imagen y Visión (FSIV) en la EPS-UCO.

## 👤 Datos del Estudiante
- **Login UCO:** `i42cagoj`
- **Plataforma de referencia:** ThinStation / Linux con OpenCV y CMake

---

## 📜 Normativa Oficial de Entrega

1. **Autoría y defensa:** El código lo has desarrollado tú mismo y, por lo tanto, podrás defenderlo en persona si eres requerido para ello.
2. **Formato del archivo comprimido:**
   - Nombre de archivo obligatorio: `<tu-login-uco>.zip` (Ejemplo: `i42cagoj.zip`).
   - Al descomprimirse, **debe** generar exactamente la siguiente estructura de carpetas:
     ```text
     |- <tu-login-uco>
        |- <carpeta con ejercicio1>
        |- <carpeta con ejercicio2>
     ```
   - No deben incluirse carpetas de compilación (`build/`), archivos temporales de IDE (`.vscode/`, `.cache/`), carpetas de tests (`Testing/`), ni binarios compilados o archivos objeto (`.o`).
3. **Versión de fuentes:** Las fuentes deben corresponder siempre con la última versión de la práctica disponible en Moodle.
4. **Compilación estricta:** Debe compilar sin errores usando CMake y Make en Linux/ThinStation.
5. **Secuencia de comprobación oficial del profesor:**
   ```bash
   unzip <tu-login-uco>.zip
   cd <tu-login-uco>
   cd <carpeta ejercicio 1>
   mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../..
   cd <carpeta ejercicio 2>
   mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../..
   ```
6. **Memoria (REPORT.md):**
   - La carpeta de fuentes de **cada ejercicio** realizado debe contener obligatoriamente un fichero `REPORT.md`.
   - **Estilo de redacción directo y de estudiante (Cero textos kilométricos o sobrecargados):**
     - Nada de descripciones teóricas extensas ni explicaciones redundantes.
     - Simplemente indicar que se ha completado el código requerido pasando todos los tests.
     - Listar los tests unitarios del ejercicio y si pasaron (`Ok`) o no.
     - Aclarar de forma honesta si queda alguna parte pendiente (o si no queda ninguna).
     - Bloque del enlace al vídeo de YouTube y desglose de capítulos.
   - Enlace opcional a un vídeo subido a YouTube (5 a 10 minutos máximo).
   - **Estructura del vídeo:**
     - Debe estar estructurado en **capítulos de YouTube**:
       - Capítulo 1 titulado `"Introducción"` con el objetivo de la práctica.
       - Para cada parámetro importante, un capítulo titulado `"Parámetro XXXX"` mostrando la ejecución interactiva y razonando el "por qué" teórico de los efectos al variar dicho parámetro.
     - En el vídeo debe mostrarse la imagen del estudiante (cámara en una ventana pequeña).
     - Sincronización estricta de audio y vídeo, sin leer un guion.
     - *Sin esta estructura de capítulos no se evaluará el vídeo.*

> **ADVERTENCIA:** NO CUMPLIR ESTA NORMATIVA IMPLICA QUE LA PRÁCTICA NO SERÁ CORREGIDA.

---

## 🛠️ Herramientas de Empaquetado y Verificación

Se proporciona el script `empaquetar_y_probar.sh` en la raíz del repositorio para automatizar:
1. **Detección automática e incremental de ejercicios:** Escanea la raíz del repositorio e incluye todos los directorios válidos que contienen proyectos (`CMakeLists.txt`), acumulándolos progresivamente en cada entrega conforme avanza el curso.
2. **Filtrado estricto:** Ignora automáticamente directorios ocultos (`.git`, `.kilo`, `.vscode`, `.cache`), carpetas de construcción (`build*`), carpetas de test temporales (`Testing`, `tmp*`) y tutoriales no evaluables (`*tutorial*`).
3. **Copia limpia:** Excluye binarios compilados, archivos objeto (`*.o`), librerías (`*.a`, `*.so`) y archivos temporales (`*~`, `*.swp`).
4. **Generación del paquete comprimido:** `i42cagoj.zip` con la raíz `<login>/`.
5. **Prueba estricta en entorno aislado:** Reproduce la secuencia de corrección del profesor para cada ejercicio acumulado (`unzip` -> `mkdir build` -> `cmake ..` -> `make` -> `./test_common_code`).
6. **Verificación de `REPORT.md`:** Comprueba que cada ejercicio contenga su memoria.
7. **Protección anti-fallos:** Si cualquier test, compilación o requisito falla, elimina el ZIP de inmediato y notifica el error.

### Uso:
```bash
# Modo incremental por defecto (detecta automáticamente todos los ejercicios acumulados)
./empaquetar_y_probar.sh

# Especificar manualmente ciertos ejercicios si se desea
./empaquetar_y_probar.sh cbg_process chroma_key

# Especificar otro login
./empaquetar_y_probar.sh --login otro_login
```
