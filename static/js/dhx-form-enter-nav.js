// dhx-form-enter-nav.js

/**
 * DHTMLX FormでEnterキーをTabキーのように動作させる共通関数（Suite 9対応）
 * @param {dhx.Form} form - 初期化済みのDHTMLX Formインスタンス
 */
function enableFormEnterNavigation(form) {
    // Form全体のキーダウンイベントを監視
    // ※Suite 9の引数仕様: event(ネイティブイベント), name(コントロール名), id(要素内ID)
    form.events.on("keydown", function (event, name) {

        // --- 修正ポイント：IME入力（漢字変換）中のEnterキー確定時は処理をスキップ ---
        // 1. IME入力中（boolean型の判定）なら処理をスキップ
        if (event.isComposing) {
            return;
        }

        // 2. ブラウザがキーをProcess（string型）と偽装している場合も処理をスキップ
        if (event.key === "Process") {
            return;
        }

        // Enterキー（KeyCode 13）以外、または装飾キー（Ctrl/Alt/Meta）は無視
        if (event.key !== "Enter" || event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }

        // 現在フォーカスがあるアイテム（name）が取得できない場合は処理しない
        if (!name) return;

        // テキストエリア（複数行入力）内での通常の改行は許可する
        const activeItem = form.getItem(name);
        if (activeItem && activeItem.config.type === "textarea") {
            return;
        }

        // ブラウザ標準のEnterキー挙動（勝手なフォーム送信など）をストップ
        event.preventDefault();

        // フォーム内の「フォーカスを当てたいコントロール」のname属性リストを動的に作成
        const focusableNames = [];
        form.forEach(function (item) {
            const type = item.config.type;
            const isHidden = item.config.hidden;
            const isDisabled = item.config.disabled;

            // フォーカス移動の対象にしたいコントロールタイプを定義
            // (input, select, combo, datepicker, timepicker など)
            const isFocusableType = ["input", "select", "combo", "datepicker", "timepicker", "textarea", "checkbox", "radioGroup", "toggleGroup"].includes(type);

            // 非表示や無効化されていない、有効な入力項目だけをリスト化
            if (isFocusableType && !isHidden && !isDisabled) {
                focusableNames.push(item.config.name);
            }
        });

        // 現在のフォーカス位置（インデックス）を取得
        const currentIndex = focusableNames.indexOf(name);
        if (currentIndex === -1) return;

        // Shiftキーが押されているかで進行方向を決定
        if (event.shiftKey) {
            // Shift + Enter：前の要素へ（先頭なら最後の要素へループ）
            const prevIndex = currentIndex === 0 ? focusableNames.length - 1 : currentIndex - 1;
            form.setFocus(focusableNames[prevIndex]);
        } else {
            // Enterのみ：次の要素へ（最後尾なら先頭の要素へループ）
            const nextIndex = currentIndex === focusableNames.length - 1 ? 0 : currentIndex + 1;
            form.setFocus(focusableNames[nextIndex]);
        }
    });
}
