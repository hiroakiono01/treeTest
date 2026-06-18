// dhx-grid-enter-nav.js

/**
 * DHTMLX GridでEnterキーをTabキーのように動作させる共通関数
 * @param {dhx.Grid} grid - 初期化済みのDHTMLX Gridインスタンス
 */
function enableGridEnterNavigation(grid) {
    // 1. キーダウンイベントの登録
    grid.events.on("beforeKeyDown", event => {
        // Enterキー以外、または装飾キー（Ctrl/Alt/Meta）が押されている場合は無視
        if (event.key !== "Enter" || event.ctrlKey || event.altKey || event.metaKey) {
            return true; // 処理を続行
        }

        // 現在選択されているセルを取得 (Suite 9 仕様)
        const selectedCell = grid.selection.getCells();
        if (!selectedCell || selectedCell.length === 0) {
            return true;
        }
        // 最初に選択されているセルを対象にする
        const currentCell = selectedCell[0];

        // ブラウザのデフォルト挙動を抑制
        event.preventDefault();

        // 編集中の場合は編集を終了させる (Suite 9 仕様)
        if (grid.edit.getEditCell()) {
            grid.edit.end();
            // バリデーション等で編集終了できなかった場合は移動しない
            if (grid.edit.getEditCell()) {
                return false;
            }
        }

        // セルの移動処理を実行（Shiftキーが押されていれば逆方向: -1、通常は正方向: 1）
        moveSelectionLikeTab(grid, currentCell, event.shiftKey ? -1 : 1);

        return false; // デフォルトのEnter挙動をキャンセル
    });
}

/**
 * 実際のセル移動とスクロールを制御する内部関数
 */
function moveSelectionLikeTab(grid, selectedCell, direction) {
    // 非表示ではない（有効な）列のリストを取得 (grid.config.columns ではなく grid.getColumns())
    const visibleColumns = grid.getColumns().filter(column => !column.hidden);
    const columnIndex = visibleColumns.findIndex(column => column.id === selectedCell.column.id);
    const rowIndex = grid.data.getIndex(selectedCell.row.id);

    let nextColumnIndex = columnIndex + direction;
    let nextRowIndex = rowIndex;

    // 右端に到達したら次の行の左端へ
    if (nextColumnIndex >= visibleColumns.length) {
        nextColumnIndex = 0;
        nextRowIndex++;
    }

    // 左端（逆戻り時）に到達したら前の行の右端へ
    if (nextColumnIndex < 0) {
        nextColumnIndex = visibleColumns.length - 1;
        nextRowIndex--;
    }

    // 上限・下限の行を超えた場合は処理を終了
    if (nextRowIndex < 0 || nextRowIndex >= grid.data.getLength()) {
        return;
    }

    const nextRowId = grid.data.getId(nextRowIndex);
    const nextColumnId = visibleColumns[nextColumnIndex].id;

    // フォーカスの移動と自動スクロール (Suite 9 仕様)
    grid.selection.setCell(nextRowId, nextColumnId);
    grid.scrollTo(nextRowId, nextColumnId);
}

