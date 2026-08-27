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
// let isJapaneseComposing = false;
//
// // ネイティブのイベントリスナーでページ全体のIME状態をキャッチする
// window.addEventListener("compositionstart", () => {
//     isJapaneseComposing = true;
// });
//
// window.addEventListener("compositionend", () => {
//     // 確定直後のEnterキーのkeydownイベントが先に走る場合があるため、
//     // わずかに遅らせてフラグを戻す
//     setTimeout(() => {
//         isJapaneseComposing = false;
//     }, 50);
// });

function enableGridEnterNavigation(grid) {
    // 💡【追加】エディタ起動時に、日本語変換確定のEnterキーがGrid本体に伝播するのを防ぐ
    grid.events.on("beforeEditStart", (rowId, colId) => {



        // エディタの要素が生成されるのをわずかに待つ
        setTimeout(() => {
            // 現在アクティブなグリッド内の入力要素を取得
            const editorInput = grid.getContainer().querySelector(".dhx_grid-editor, input, textarea");
            if (!editorInput) return;

            // 入力要素に直接イベントリスナーを付与
            editorInput.addEventListener("keydown", (e) => {
                // IME変換中、または変換確定直後のEnter（keyCode: 229 または isComposing）を完全にブロック
                if (e.isComposing || e.keyCode === 229) {
                    // Grid本体の beforeKeyDown イベントに到達させない
                    e.stopPropagation();
                }
            });
        }, 10);
    });

    // メインのキーナビゲーション処理
    grid.events.on("beforeKeyDown", event => {
        // 1. 基本的な修飾キーやEnter/Tab以外のキーは無視
        if ((event.key !== "Enter" && event.key !== "Tab" ) || event.ctrlKey || event.altKey || event.metaKey) {
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

        // 3. 次のセルへ移動
        moveSelectionLikeTab(grid, currentCell, event.shiftKey ? -1 : 1);

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









