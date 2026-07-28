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
    grid.events.on("beforeKeyDown", event => {
        if (event.key !== "Enter" && event.key !== "Tab" || event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }

        const currentCell = grid.selection.getCell();
        if (!currentCell) {
            return false;
        }

        event.preventDefault();
        event.stopPropagation();

        if (grid.config.$editable) {
            grid.editEnd();

            if (grid.config.$editable) {
                return false;
            }
        }


        // if (grid.config.$editable) {
        //
        //
        //     if (grid.config.$editable) {
        //         return false;
        //     }
        // }

        moveSelectionLikeTab(grid, currentCell, event.shiftKey ? -1 : 1);
        // 2. ★【最重要】移動が完了した「直後の最新の選択セル」をもう一度取得
        const nextCell = grid.selection.getCell();

        if (nextCell && nextCell.column.editable !== false) {
            // Gridの内部処理（枠の移動）が落ち着くのを30ミリ秒だけ待ってから、自動で編集モードにする
            setTimeout(() => {
                grid.editCell(nextCell.row.id, nextCell.column.id);
            }, 30);
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









