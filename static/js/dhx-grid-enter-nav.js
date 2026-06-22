// dhx-grid-enter-nav.js

/**
 * DHTMLX GridでEnterキーをTabキーのように動作させる共通関数
 * @param {dhx.Grid} grid - 初期化済みのDHTMLX Gridインスタンス
 */
function enableGridEnterNavigation(grid) {
    grid.events.on("beforeKeyDown", event => {
        if (event.key !== "Enter" || event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }

        const selectedCell = grid.selection.getCell();

        if (!selectedCell) {
            return false;
        }

        event.preventDefault();

        if (grid.config.$editable) {
            grid.editEnd();

            if (grid.config.$editable) {
                return false;
            }
        }

        moveSelectionLikeTab(grid, selectedCell, event.shiftKey ? -1 : 1);

        return false;
    });

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
}

