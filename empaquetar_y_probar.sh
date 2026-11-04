#!/usr/bin/env bash
# ==============================================================================
# Script de empaquetado y verificación incremental para Prácticas de Visión Artificial
# Asignatura: Fundamentos de Sistemas de Imagen y Visión (FSIV) — EPS UCO
# ==============================================================================

set -euo pipefail

# Colores para la salida en consola
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Directorio base del repositorio de prácticas
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuración del estudiante
LOGIN="i42cagoj"

# Mostrar ayuda
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    echo "Uso: $0 [opciones] [ejercicio1 ejercicio2 ...]"
    echo ""
    echo "Opciones:"
    echo "  -l, --login <login>    Especifica el login UCO (por defecto: i42cagoj)"
    echo "  -h, --help             Muestra esta ayuda"
    echo ""
    echo "Comportamiento incremental por defecto:"
    echo "  Si no se indican ejercicios específicos, el script detecta automáticamente"
    echo "  todos los directorios que correspondan a ejercicios (contengan CMakeLists.txt)"
    echo "  y excluye builds, directorios ocultos (.git, .kilo, .vscode), y tutoriales."
    echo ""
    exit 0
fi

# Parsear posible argumento de login
EJERCICIOS_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        -l|--login)
            LOGIN="$2"
            shift 2
            ;;
        *)
            EJERCICIOS_ARGS+=("$1")
            shift
            ;;
    esac
done

# ------------------------------------------------------------------------------
# Detección automática incremental de ejercicios
# ------------------------------------------------------------------------------
EJERCICIOS=()

if [ ${#EJERCICIOS_ARGS[@]} -gt 0 ]; then
    # El usuario especificó manualmente qué ejercicios incluir
    EJERCICIOS=("${EJERCICIOS_ARGS[@]}")
else
    # Modo incremental automático: buscar todos los directorios válidos de prácticas
    for d in "${BASE_DIR}"/*/; do
        [ -d "$d" ] || continue
        nombre="$(basename "$d")"

        # 1. Ignorar carpetas ocultas (ej: .git, .kilo, .vscode, .cache, .readme)
        [[ "$nombre" =~ ^\. ]] && continue

        # 2. Ignorar carpetas de compilación (ej: build, build-*, cmake-build-*)
        [[ "$nombre" =~ build ]] && continue

        # 3. Ignorar carpetas temporales o de tests (ej: tmp*, Testing)
        [[ "$nombre" =~ ^(tmp|Testing) ]] && continue

        # 4. Ignorar el tutorial inicial de OpenCV (P0 no evaluable)
        [[ "$nombre" =~ tutorial ]] && continue

        # 5. Debe ser un proyecto con CMakeLists.txt
        if [ -f "${d}/CMakeLists.txt" ]; then
            EJERCICIOS+=("$nombre")
        fi
    done
fi

if [ ${#EJERCICIOS[@]} -eq 0 ]; then
    echo -e "${RED}[ERROR] No se encontraron directorios de ejercicios para empaquetar.${NC}"
    exit 1
fi

ZIP_NAME="${LOGIN}.zip"
DEST_ZIP="${BASE_DIR}/${ZIP_NAME}"

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  Verificación y Empaquetado Incremental — Visión Artificial     ${NC}"
echo -e "${BLUE}================================================================${NC}"
echo -e "Estudiante / Login UCO: ${YELLOW}${LOGIN}${NC}"
echo -e "Ejercicios detectados (${#EJERCICIOS[@]}):  ${CYAN}${EJERCICIOS[*]}${NC}"
echo -e "Archivo destino:        ${YELLOW}${DEST_ZIP}${NC}"
echo ""

# ------------------------------------------------------------------------------
# 1. Comprobaciones previas en el directorio de trabajo
# ------------------------------------------------------------------------------
echo -e "${BLUE}[1/4] Comprobando existencia de los ejercicios, REPORT.md y objetos precompilados...${NC}"

for EJ in "${EJERCICIOS[@]}"; do
    EJ_PATH="${BASE_DIR}/${EJ}"
    if [ ! -d "${EJ_PATH}" ]; then
        echo -e "${RED}[ERROR] No se encuentra el directorio del ejercicio: ${EJ_PATH}${NC}"
        exit 1
    fi

    if [ ! -f "${EJ_PATH}/CMakeLists.txt" ]; then
        echo -e "${RED}[ERROR] No se encontró CMakeLists.txt en ${EJ_PATH}${NC}"
        exit 1
    fi

    if [ ! -f "${EJ_PATH}/REPORT.md" ]; then
        echo -e "${RED}[ERROR] Falta el archivo REPORT.md en ${EJ_PATH}${NC}"
        echo -e "${RED}La normativa exige obligatoriamente un REPORT.md en cada ejercicio.${NC}"
        exit 1
    fi

    # Detección y verificación de objetos precompilados requeridos (.o)
    REQS_O=$(grep -oE '\b[a-zA-Z0-9_.-]+\.o\b' "${EJ_PATH}/CMakeLists.txt" 2>/dev/null | sort -u || true)
    OBJ_INFO=""
    if [ -n "${REQS_O}" ]; then
        for OBJ in ${REQS_O}; do
            if [ -f "${EJ_PATH}/${OBJ}" ]; then
                OBJ_INFO="${OBJ_INFO} [Precompilado: ${OBJ}]"
            else
                echo -e "${RED}[ERROR] Objeto precompilado '${OBJ}' requerido por CMakeLists.txt no existe en ${EJ_PATH}${NC}"
                exit 1
            fi
        done
    fi

    echo -e "  - ${GREEN}OK:${NC} ${EJ} (CMakeLists.txt y REPORT.md presentes)${CYAN}${OBJ_INFO}${NC}"
done

# ------------------------------------------------------------------------------
# 2. Generación del paquete ZIP con estructura limpia
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}[2/4] Generando estructura limpia y empaquetando en ${ZIP_NAME}...${NC}"

SUCCESS=0
STAGE_DIR=$(mktemp -d -t fsiv_stage_XXXXXX)
TRAP_CLEANUP() {
    rm -rf "${STAGE_DIR}" 2>/dev/null || true
    if [ -n "${TEST_DIR:-}" ] && [ -d "${TEST_DIR:-}" ]; then
        rm -rf "${TEST_DIR}" 2>/dev/null || true
    fi
    if [ "${SUCCESS}" -ne 1 ]; then
        if [ -f "${DEST_ZIP}" ]; then
            rm -f "${DEST_ZIP}"
            echo -e "\n${RED}========================================================================${NC}"
            echo -e "${RED}[FALLO DE ENTREGA] Se eliminó ${DEST_ZIP} por no superar la validación.${NC}"
            echo -e "${RED}Corrige los errores indicados arriba antes de volver a intentarlo.${NC}"
            echo -e "${RED}========================================================================${NC}\n"
        fi
    fi
}
trap TRAP_CLEANUP EXIT

TARGET_STUDENT_DIR="${STAGE_DIR}/${LOGIN}"
mkdir -p "${TARGET_STUDENT_DIR}"

# Exclusiones para evitar binarios temporales, datos pesados y librerías dinámicas
# Moodle límite: 500 KB. Se incluyen explícitamente objetos precompilados de test (.o)
RSYNC_EXCLUDES=(
    "--exclude=data/"
    "--exclude=*.pdf"
    "--exclude=.readme*"
    "--exclude=.vscode/"
    "--exclude=build*"
    "--exclude=.cache*"
    "--exclude=Testing*"
    "--exclude=*-macos.o"
    "--include=test_common_code*.o"
    "--include=*.cpp.o"
    "--include=test_*.o"
    "--exclude=*.o"
    "--exclude=*.a"
    "--exclude=*.so"
    "--exclude=*~"
    "--exclude=*.swp"
    "--exclude=.git*"
    "--exclude=.kilo*"
)

for EJ in "${EJERCICIOS[@]}"; do
    echo -e "  Copiando fuentes de ${EJ}..."
    mkdir -p "${TARGET_STUDENT_DIR}/${EJ}"
    rsync -a "${RSYNC_EXCLUDES[@]}" "${BASE_DIR}/${EJ}/" "${TARGET_STUDENT_DIR}/${EJ}/"

    # Asegurar copia explícita de cualquier objeto .o requerido por CMakeLists
    REQS_O=$(grep -oE '\b[a-zA-Z0-9_.-]+\.o\b' "${BASE_DIR}/${EJ}/CMakeLists.txt" 2>/dev/null | sort -u || true)
    if [ -n "${REQS_O}" ]; then
        for OBJ in ${REQS_O}; do
            if [ ! -f "${TARGET_STUDENT_DIR}/${EJ}/${OBJ}" ]; then
                cp -p "${BASE_DIR}/${EJ}/${OBJ}" "${TARGET_STUDENT_DIR}/${EJ}/${OBJ}"
            fi
            echo -e "    ${GREEN}✓${NC} Incluido objeto precompilado: ${CYAN}${OBJ}${NC}"
        done
    fi

    # Optimizar peso eliminando símbolos de depuración de la copia en el stage
    if command -v strip >/dev/null 2>&1; then
        for obj in "${TARGET_STUDENT_DIR}/${EJ}"/*.o; do
            if [ -f "$obj" ]; then
                strip --strip-unneeded "$obj" 2>/dev/null || true
            fi
        done
    fi
done

# Creación del zip con compresión máxima
rm -f "${DEST_ZIP}"
if command -v zip >/dev/null 2>&1; then
    (
        cd "${STAGE_DIR}"
        zip -9 -r -q "${DEST_ZIP}" "${LOGIN}"
    )
elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import sys, zipfile, os
stage_dir, login, dest_zip = sys.argv[1], sys.argv[2], sys.argv[3]
with zipfile.ZipFile(dest_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    target_dir = os.path.join(stage_dir, login)
    for root, dirs, files in os.walk(target_dir):
        for f in sorted(files):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, stage_dir)
            zf.write(full_path, rel_path)
" "${STAGE_DIR}" "${LOGIN}" "${DEST_ZIP}"
elif command -v 7z >/dev/null 2>&1; then
    (
        cd "${STAGE_DIR}"
        7z a -tzip -mx=9 "${DEST_ZIP}" "${LOGIN}" >/dev/null
    )
else
    echo -e "${RED}[ERROR] No se encontró ninguna utilidad de compresión (zip, python3 o 7z).${NC}"
    exit 1
fi

ZIP_BYTES=$(stat -c%s "${DEST_ZIP}")
ZIP_SIZE_KB=$(( (ZIP_BYTES + 1023) / 1024 ))
MAX_BYTES=512000 # Límite de Moodle: 500 KB

echo -e "${GREEN}  ZIP generado correctamente:${NC} ${DEST_ZIP} (${ZIP_SIZE_KB} KB)"

if [ "${ZIP_BYTES}" -gt "${MAX_BYTES}" ]; then
    if [ ${#EJERCICIOS[@]} -gt 1 ]; then
        echo -e "${YELLOW}[AVISO] El archivo (${ZIP_SIZE_KB} KB) supera el límite de Moodle (500 KB) por acumulación de ${#EJERCICIOS[@]} ejercicios con objetos precompilados.${NC}"
        echo -e "${YELLOW}Para la entrega oficial de una práctica concreta en Moodle, puedes empaquetarla individualmente:${NC}"
        echo -e "${CYAN}  $0 <nombre_ejercicio>${NC}"
    else
        echo -e "${RED}[AVISO] El archivo generado (${ZIP_SIZE_KB} KB) supera el límite de subida de Moodle (500 KB).${NC}"
    fi
else
    echo -e "${GREEN}  ✓ Tamaño dentro del límite de Moodle (máx 500 KB): ${ZIP_SIZE_KB} KB < 500 KB${NC}"
fi

# ------------------------------------------------------------------------------
# 3. Simulación estricta de la secuencia de comprobación del profesor
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}[3/4] Probando la secuencia de comprobación oficial del profesor...${NC}"
echo -e "Secuencia a ejecutar en un directorio temporal aislado:"
echo -e "  unzip ${ZIP_NAME}"
echo -e "  cd ${LOGIN}"
for EJ in "${EJERCICIOS[@]}"; do
    echo -e "  cd ${EJ}"
    echo -e "  mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../.."
done
echo ""

TEST_DIR=$(mktemp -d -t fsiv_test_XXXXXX)
cp "${DEST_ZIP}" "${TEST_DIR}/"

cd "${TEST_DIR}"

# Descompresión
echo -e "-> Descomprimiendo ${YELLOW}${ZIP_NAME}${NC}..."
if command -v unzip >/dev/null 2>&1; then
    if ! unzip -q "${ZIP_NAME}"; then
        echo -e "${RED}[FALLO] Error al descomprimir ${ZIP_NAME}${NC}"
        exit 1
    fi
elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], 'r') as zf:
    zf.extractall('.')
" "${ZIP_NAME}"
elif command -v 7z >/dev/null 2>&1; then
    7z x -y "${ZIP_NAME}" >/dev/null
fi

if [ ! -d "${LOGIN}" ]; then
    echo -e "${RED}[FALLO] La descompresión no generó el directorio raíz '${LOGIN}' exigido por la normativa.${NC}"
    exit 1
fi

cd "${LOGIN}"

# Descubrimiento dinámico de carpetas de ejercicios dentro del ZIP descomprimido
EJERCICIOS_ZIP=()
for item in */; do
    [ -d "$item" ] || continue
    ej_nombre="${item%/}"
    [[ "$ej_nombre" =~ ^\. ]] && continue
    if [ -f "${ej_nombre}/CMakeLists.txt" ]; then
        EJERCICIOS_ZIP+=("${ej_nombre}")
    fi
done

if [ ${#EJERCICIOS_ZIP[@]} -eq 0 ]; then
    echo -e "${RED}[FALLO] No se encontraron carpetas con CMakeLists.txt dentro de '${LOGIN}'${NC}"
    exit 1
fi

# Comprobación dinámica de cada ejercicio encontrado
for EJ in "${EJERCICIOS_ZIP[@]}"; do
    echo -e "\n========================================================"
    echo -e "-> Probando ejercicio dinámicamente: ${YELLOW}${EJ}${NC}"
    echo -e "========================================================"

    echo -e "-> ${YELLOW}cd ${EJ}${NC}"
    cd "${EJ}"

    if [ ! -f "REPORT.md" ]; then
        echo -e "${RED}[FALLO] Falta REPORT.md en '${LOGIN}/${EJ}'${NC}"
        exit 1
    fi

    # Verificar que los objetos precompilados requeridos están presentes
    REQS_O=$(grep -oE '\b[a-zA-Z0-9_.-]+\.o\b' "CMakeLists.txt" 2>/dev/null | sort -u || true)
    if [ -n "${REQS_O}" ]; then
        for OBJ in ${REQS_O}; do
            if [ ! -f "${OBJ}" ]; then
                echo -e "${RED}[FALLO] Objeto precompilado requerido '${OBJ}' no está presente en '${LOGIN}/${EJ}'${NC}"
                exit 1
            fi
            echo -e "  ${GREEN}✓${NC} Objeto precompilado verificado en el ZIP: ${CYAN}${OBJ}${NC}"
        done
    fi

    # Ejecución de la secuencia de comprobación:
    # mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../..
    echo -e "-> ${YELLOW}mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../..${NC}"
    mkdir -p build && cd build

    if ! cmake .. > /dev/null; then
        echo -e "${RED}[FALLO] Falló la configuración de CMake en ${EJ}${NC}"
        exit 1
    fi

    if ! make -j"$(nproc)"; then
        echo -e "${RED}[FALLO] Falló la compilación (make) en ${EJ}${NC}"
        exit 1
    fi

    if [ -x "./test_common_code" ]; then
        if ! ./test_common_code; then
            echo -e "${RED}[FALLO] Los tests unitarios no se superaron en ${EJ}${NC}"
            exit 1
        fi
    elif [ -f "CTestTestfile.cmake" ]; then
        if ! ctest --output-on-failure; then
            echo -e "${RED}[FALLO] Los tests (ctest) no se superaron en ${EJ}${NC}"
            exit 1
        fi
    fi

    cd ../..
    echo -e "${GREEN}  ✓ Ejercicio ${EJ} compiló y superó los tests con éxito.${NC}"
done
# ------------------------------------------------------------------------------
# 4. Resultado final
# ------------------------------------------------------------------------------
SUCCESS=1
echo -e "\n${BLUE}[4/4] Resultado final de la validación:${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo -e "${GREEN}  ¡ENHORABUENA! La entrega cumple 100% con la normativa oficial.       ${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo -e "Archivo listo para subir a Moodle: ${YELLOW}${DEST_ZIP}${NC} (${ZIP_SIZE_KB} KB)"
echo -e "Estructura del archivo comprobada:"
echo -e "  |- ${LOGIN}"
for EJ in "${EJERCICIOS[@]}"; do
    echo -e "     |- ${EJ} (con REPORT.md, objetos precompilados y tests 100% superados)"
done
echo ""
