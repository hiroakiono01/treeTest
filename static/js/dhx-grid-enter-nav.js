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
    grid.events.on("beforeKeyDown", function (event) {
            console.log("event.keyCode", event.keyCode, "event.isComposing", event.isComposing)
            //const selectedCell = grid.selection.getCell();
            // const currentColumn = selectedCell.column;
            // const currentRow = selectedCell.row;
            // 1. 日本語の漢字変換（IME）中のEnterキーは処理をスキップ
            if (event.isComposing || event.keyCode === 229) {
                // // 現在編集中のセル情報を取得
                // const selectedCell = grid.selection.getCell();
                // if (!selectedCell) return true;
                //
                // const rowId = selectedCell.row.id;
                // const colId = selectedCell.column.id;
                //
                // // 非同期（次のフレーム）で実行することで、DHTMLXの強制Blurを上書きしてフォーカスを戻す
                // requestAnimationFrame(() => {
                //     // 一度選択状態を再セット
                //     grid.selection.setCell(rowId, colId);
                //     // 即座に編集モードを再開し、カーソル（フォーカス）をセット
                //     grid.editCell(rowId, colId);
                // });
                //event.stopPropagation();
                return true;
            }

            // --- ここから下に、通常のEnterキーや矢印キーなどの移動処理を書く ---
            const selectedCell = grid.selection.getCell();
            if (!selectedCell) return; // セルが選択されていない場合の安全対策

            // 2. Enterキーが押された場合のみ処理
            if (event.keyCode === 13) {
                console.log("event.keyCode", event.keyCode, "event.isComposing", event.isComposing)
                // 現在選択されているセルの情報を取得
                const selectedCell = grid.selection.getCell();
                if (!selectedCell || !selectedCell.row || !selectedCell.column) return;

                // 3. 現在編集中の場合は、先に編集を確定（保存）して閉じる
                grid.editEnd()


                // イベントのデフォルト挙動（ブラウザ独自の改行など）を防止
                event.preventDefault();

                const currentRow = selectedCell.row;
                const currentColumn = selectedCell.column;

                // グリッド内の全列情報を取得して現在のインデックスを特定
                const columns = grid.config.columns;
                const currentColIndex = columns.findIndex(col => col.id === currentColumn.id);

                let nextRow = currentRow;
                let nextColIndex = currentColIndex + 1;

                // 3. 右の列がない（行の末尾）場合は、次の行の最初の列へ移動
                if (nextColIndex >= columns.length) {
                    nextColIndex = 0;

                    // 現在の行の位置（インデックス）を取得
                    const currentIndex = grid.data.getIndex(currentRow.id);
                    const nextIndex = currentIndex + 1;
                    console.log("currentIndex", currentIndex)

                    // 次の行が存在しない（最終行の末尾）場合は処理を終了
                    if (nextIndex >= grid.data.getLength()) return;

                    // 次の行のIDを取得し、そこから行データオブジェクトを取得
                    const nextRowId = grid.data.getId(nextIndex);
                    nextRow = grid.data.getItem(nextRowId);

                }

                const nextColumn = columns[nextColIndex];

                // 4. 次のセルを選択状態にして編集モードを開始
                grid.selection.setCell(nextRow.id, nextColumn.id); // セルを選択

                // 編集可能な列であれば編集モードを起動
                if (nextColumn.editable !== false) {
                    // 選択直後の処理を確実にするため、少しだけタイミングをずらして編集を開始
                    setTimeout(() => {
                        grid.editCell(nextRow.id, nextColumn.id);
                    }, 50);
                    // grid.editCell(nextRow.id, nextColumn.id);
                }
            }
        }
    )
}








