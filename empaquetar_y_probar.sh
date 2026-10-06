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
echo -e "${BLUE}[1/4] Comprobando existencia de los ejercicios y REPORT.md...${NC}"

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

    echo -e "  - ${GREEN}OK:${NC} ${EJ} (CMakeLists.txt y REPORT.md presentes)"
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

# Exclusiones para evitar archivos residuales, temporales y carpetas de build
RSYNC_EXCLUDES=(
    "--exclude=build*"
    "--exclude=.cache*"
    "--exclude=Testing*"
    "--exclude=*.o"
    "--exclude=*.a"
    "--exclude=*.so"
    "--exclude=*~"
    "--exclude=*.swp"
    "--exclude=.git*"
    "--exclude=.kilo*"
)

for EJ in "${EJERCICIOS[@]}"; do
    echo -e "  Copiando ${EJ} de forma limpia..."
    mkdir -p "${TARGET_STUDENT_DIR}/${EJ}"
    rsync -a "${RSYNC_EXCLUDES[@]}" "${BASE_DIR}/${EJ}/" "${TARGET_STUDENT_DIR}/${EJ}/"
done

# Creación del zip
rm -f "${DEST_ZIP}"
(
    cd "${STAGE_DIR}"
    zip -r -q "${DEST_ZIP}" "${LOGIN}"
)

ZIP_SIZE=$(du -h "${DEST_ZIP}" | cut -f1)
echo -e "${GREEN}  ZIP generado correctamente:${NC} ${DEST_ZIP} (${ZIP_SIZE})"

# ------------------------------------------------------------------------------
# 3. Simulación estricta de la secuencia de comprobación del profesor
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}[3/4] Probando la secuencia de comprobación oficial del profesor...${NC}"
echo -e "Secuencia a ejecutar en un directorio temporal aislado:"
echo -e "  unzip ${ZIP_NAME}"
echo -e "  cd ${LOGIN}"
for EJ in "${EJERCICIOS[@]}"; do
    echo -e "  cd ${EJ} && mkdir build && cd build && cmake .. && make && ./test_common_code && cd ../.."
done
echo ""

TEST_DIR=$(mktemp -d -t fsiv_test_XXXXXX)
cp "${DEST_ZIP}" "${TEST_DIR}/"

cd "${TEST_DIR}"

# Descompresión
echo -e "-> Ejecutando: ${YELLOW}unzip ${ZIP_NAME}${NC}"
if ! unzip -q "${ZIP_NAME}"; then
    echo -e "${RED}[FALLO] Error al descomprimir ${ZIP_NAME}${NC}"
    exit 1
fi

if [ ! -d "${LOGIN}" ]; then
    echo -e "${RED}[FALLO] La descompresión no generó el directorio raíz '${LOGIN}' exigido por la normativa.${NC}"
    exit 1
fi

cd "${LOGIN}"

# Comprobación de cada ejercicio
for EJ in "${EJERCICIOS[@]}"; do
    echo -e "\n========================================================"
    echo -e "-> Probando ejercicio: ${YELLOW}${EJ}${NC}"
    echo -e "========================================================"

    if [ ! -d "${EJ}" ]; then
        echo -e "${RED}[FALLO] No existe el subdirectorio '${EJ}' dentro de '${LOGIN}'${NC}"
        exit 1
    fi

    if [ ! -f "${EJ}/REPORT.md" ]; then
        echo -e "${RED}[FALLO] Falta REPORT.md en '${LOGIN}/${EJ}'${NC}"
        exit 1
    fi

    cd "${EJ}"
    
    echo -e "-> ${YELLOW}mkdir build && cd build${NC}"
    mkdir -p build && cd build

    echo -e "-> ${YELLOW}cmake ..${NC}"
    if ! cmake .. > /dev/null; then
        echo -e "${RED}[FALLO] Falló la configuración de CMake en ${EJ}${NC}"
        exit 1
    fi

    echo -e "-> ${YELLOW}make -j$(nproc)${NC}"
    if ! make -j"$(nproc)"; then
        echo -e "${RED}[FALLO] Falló la compilación (make) en ${EJ}${NC}"
        exit 1
    fi

    echo -e "-> ${YELLOW}./test_common_code${NC}"
    if ! ./test_common_code; then
        echo -e "${RED}[FALLO] Los tests unitarios no se superaron en ${EJ}${NC}"
        exit 1
    fi

    echo -e "${GREEN}  ✓ Ejercicio ${EJ} superó la compilación y los tests con éxito.${NC}"
    cd ../..
done

# ------------------------------------------------------------------------------
# 4. Resultado final
# ------------------------------------------------------------------------------
SUCCESS=1
echo -e "\n${BLUE}[4/4] Resultado final de la validación:${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo -e "${GREEN}  ¡ENHORABUENA! La entrega cumple 100% con la normativa oficial.       ${NC}"
echo -e "${GREEN}========================================================================${NC}"
echo -e "Archivo listo para subir a Moodle: ${YELLOW}${DEST_ZIP}${NC} (${ZIP_SIZE})"
echo -e "Estructura del archivo comprobada:"
echo -e "  |- ${LOGIN}"
for EJ in "${EJERCICIOS[@]}"; do
    echo -e "     |- ${EJ} (con REPORT.md y tests 100% superados)"
done
echo ""
