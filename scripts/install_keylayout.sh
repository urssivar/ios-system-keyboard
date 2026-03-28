#!/bin/bash
# install_keylayout.sh — устанавливает .keylayout файлы на macOS
#
# Использование:
#   ./install_keylayout.sh                     # установить все .keylayout
#   ./install_keylayout.sh tyv.keylayout       # установить один файл
#   ./install_keylayout.sh --list              # показать доступные
#   ./install_keylayout.sh --uninstall         # удалить все установленные
#
# После установки:
#   1. Откройте «Системные настройки» → «Клавиатура» → «Источники ввода»
#   2. Нажмите «+» → «Другие» (Others)
#   3. Найдите установленную раскладку по названию
#   4. Добавьте и переключитесь на неё

set -euo pipefail

KEYLAYOUT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/Library/Keyboard Layouts"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}ℹ${NC}  $1"; }
ok()    { echo -e "${GREEN}✓${NC}  $1"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $1"; }
err()   { echo -e "${RED}✗${NC}  $1"; }

# ── List available layouts ───────────────────────────────────────────────────

list_layouts() {
    echo ""
    echo "Доступные раскладки / Available layouts:"
    echo ""
    local count=0
    for f in "$KEYLAYOUT_DIR"/*.keylayout; do
        [ -f "$f" ] || continue
        local name
        name=$(grep -oP 'name="\K[^"]+' "$f" | head -1)
        local base
        base=$(basename "$f")
        printf "  %-35s  %s\n" "$base" "$name"
        ((count++))
    done
    echo ""
    if [ "$count" -eq 0 ]; then
        warn "Не найдено .keylayout файлов в $KEYLAYOUT_DIR"
    else
        info "Найдено $count раскладок"
    fi
}

# ── Install ──────────────────────────────────────────────────────────────────

install_layout() {
    local src="$1"
    local base
    base=$(basename "$src")

    if [ ! -f "$src" ]; then
        err "Файл не найден: $src"
        return 1
    fi

    mkdir -p "$INSTALL_DIR"
    cp "$src" "$INSTALL_DIR/$base"
    ok "Установлен: $base"
}

install_all() {
    local count=0
    for f in "$KEYLAYOUT_DIR"/*.keylayout; do
        [ -f "$f" ] || continue
        install_layout "$f"
        ((count++))
    done

    if [ "$count" -eq 0 ]; then
        err "Не найдено .keylayout файлов в $KEYLAYOUT_DIR"
        exit 1
    fi

    echo ""
    ok "Установлено $count раскладок в $INSTALL_DIR"
    post_install_message
}

install_specific() {
    local target="$1"

    # Try exact path first
    if [ -f "$target" ]; then
        install_layout "$target"
        post_install_message
        return
    fi

    # Try in keylayout dir
    if [ -f "$KEYLAYOUT_DIR/$target" ]; then
        install_layout "$KEYLAYOUT_DIR/$target"
        post_install_message
        return
    fi

    # Try adding .keylayout extension
    if [ -f "$KEYLAYOUT_DIR/$target.keylayout" ]; then
        install_layout "$KEYLAYOUT_DIR/$target.keylayout"
        post_install_message
        return
    fi

    err "Файл не найден: $target"
    echo "  Попробуйте: $0 --list"
    exit 1
}

# ── Uninstall ────────────────────────────────────────────────────────────────

uninstall_all() {
    if [ ! -d "$INSTALL_DIR" ]; then
        info "Нечего удалять — папка $INSTALL_DIR не существует"
        return
    fi

    local count=0
    for f in "$INSTALL_DIR"/*.keylayout; do
        [ -f "$f" ] || continue
        local base
        base=$(basename "$f")
        rm "$f"
        ok "Удалён: $base"
        ((count++))
    done

    if [ "$count" -eq 0 ]; then
        info "Нет установленных .keylayout файлов"
    else
        echo ""
        ok "Удалено $count раскладок"
        echo ""
        warn "Перезагрузите Mac или выйдите из сессии для применения"
    fi
}

# ── Post-install message ─────────────────────────────────────────────────────

post_install_message() {
    echo ""
    echo "┌─────────────────────────────────────────────────────┐"
    echo "│  Что дальше / What's next:                         │"
    echo "│                                                     │"
    echo "│  1. Откройте «Системные настройки»                 │"
    echo "│     System Settings → Keyboard → Input Sources      │"
    echo "│                                                     │"
    echo "│  2. Нажмите «+» → «Другие» (Others)               │"
    echo "│                                                     │"
    echo "│  3. Найдите раскладку по названию                  │"
    echo "│                                                     │"
    echo "│  4. Если раскладка не появилась —                   │"
    echo "│     перезагрузите Mac или выйдите из сессии         │"
    echo "└─────────────────────────────────────────────────────┘"
    echo ""
}

# ── Main ─────────────────────────────────────────────────────────────────────

case "${1:-}" in
    --list|-l)
        list_layouts
        ;;
    --uninstall|-u)
        uninstall_all
        ;;
    --help|-h)
        echo "Установщик клавиатурных раскладок для macOS"
        echo ""
        echo "Использование:"
        echo "  $0                     Установить все раскладки"
        echo "  $0 tyv.keylayout       Установить одну раскладку"
        echo "  $0 tyv                 Установить одну (без расширения)"
        echo "  $0 --list              Показать доступные раскладки"
        echo "  $0 --uninstall         Удалить все установленные"
        echo "  $0 --help              Показать эту справку"
        ;;
    "")
        info "Установка всех раскладок из $KEYLAYOUT_DIR"
        echo ""
        install_all
        ;;
    *)
        install_specific "$1"
        ;;
esac
