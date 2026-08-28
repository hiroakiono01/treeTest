// dhx-grid-enter-nav.js

// dhx-grid-enter-nav.js

/**
 * DHTMLX GridでEnterキーをTabキーのように動作させる共通関数
 * @param {dhx.Grid} grid - 初期化済みのDHTMLX Gridインスタンス
 */
// dhx-grid-enter-nav.js
// dhx-grid-enter-nav.js

/**
 * DHTMLX GridでEnterキーをTabキーのように動作させる共通関数
 * @param {dhx.Grid} grid - 初期化済みのDHTMLX Gridインスタンス
 */
function enableGridEnterNavigation(grid) {


    // メインのキーナビゲーション処理
    grid.events.on("beforeKeyDown", event => {
        // 💡 IME（日本語）変換中のEnterキー入力を完全に無視する
        if (event.isComposing || event.keyCode === 229) {
            return true; // イベントを通常通り通過させ、Gridの移動処理をスキップ
        }

        // 1. 基本的な修飾キーやEnter/Tab以外のキーは無視
        if ((event.key !== "Enter" && event.key !== "Tab") || event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }

        const currentCell = grid.selection.getCell();
        if (!currentCell) {
            return false;
        }

        event.preventDefault();
        event.stopPropagation();

        // 2. 編集中の場合は編集を終了させる
        if (grid.config.$editable) {
            grid.editEnd();
            if (grid.config.$editable) {
                return false;
            }
        }
        // シフトキーの状態によって移動方向を決定 (三項演算子を使わず安全に記述)
        let direction = 1;
        if (event.shiftKey) {
            direction = -1;
        }
        // 3. 次のセルへ移動
        moveSelectionLikeTab(grid, currentCell, direction);

        // 4. 移動完了後のセルを取得して自動編集モードにする
        const nextCell = grid.selection.getCell();
        if (nextCell && nextCell.column.editable !== false) {
            setTimeout(() => {
                grid.editCell(nextCell.row.id, nextCell.column.id);
            }, 50);
        }

        return false;
    });
}

function moveSelectionLikeTab(grid, selectedCell, direction) {
    const visibleColumns = grid.config.columns.filter(column => !column.hidden);
    const columnIndex = visibleColumns.indexOf(selectedCell.column);
    const rowIndex = grid.data.getIndex(String(selectedCell.row.id));

    let nextColumnIndex = columnIndex + direction;
    let nextRowIndex = rowIndex;

    if (nextColumnIndex >= visibleColumns.length) {
        nextColumnIndex = 0;
        nextRowIndex++;
    }

    if (nextColumnIndex < 0) {
        nextColumnIndex = visibleColumns.length - 1;
        nextRowIndex--;
    }

    if (nextRowIndex < 0 || nextRowIndex >= grid.data.getLength()) {
        return;
    }

    const nextRowId = grid.data.getId(nextRowIndex);
    const nextColumnId = visibleColumns[nextColumnIndex].id;
    grid.selection.setCell(nextRowId, nextColumnId);
    grid.scrollTo(String(nextRowId), String(nextColumnId));
}









