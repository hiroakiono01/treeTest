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
            return;
        }

        // 現在選択されているセルを取得
        const selectedCell = grid.selection.getCell();
        if (!selectedCell) {
            return false;
        }

        // ブラウザのデフォルト挙動を抑制
        event.preventDefault();

        // 編集中の場合は編集を終了させる
        if (grid.config.$editable) {
            grid.editEnd();
            // 編集が正常に終了できなかった（バリデーションエラー等）場合は移動しない
            if (grid.config.$editable) {
                return false;
            }
        }

        // セルの移動処理を実行（Shiftキーが押されていれば逆方向: -1、通常は正方向: 1）
        moveSelectionLikeTab(grid, selectedCell, event.shiftKey ? -1 : 1);

        return false;
    });
}

/**
 * 実際のセル移動とスクロールを制御する内部関数
 */
function moveSelectionLikeTab(grid, selectedCell, direction) {
    // 非表示ではない（有効な）列のリストを取得
    const visibleColumns = grid.config.columns.filter(column => !column.hidden);
    const columnIndex = visibleColumns.indexOf(selectedCell.column);
    const rowIndex = grid.data.getIndex(String(selectedCell.row.id));

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

    // フォーカスの移動と自動スクロール
    grid.selection.setCell(nextRowId, nextColumnId);
    grid.scrollTo(String(nextRowId), String(nextColumnId));
}
