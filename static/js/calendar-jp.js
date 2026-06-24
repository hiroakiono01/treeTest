function setupJapaneseCalendar(formInstance, controlName) {
    if (!formInstance) return;

    // 1. カレンダーの日本語化（未設定の場合のみ効果あり）
    const localeJa = {
        monthsShort: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        months: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        daysShort: ["日", "月", "火", "水", "木", "金", "土"],
        days: ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"]
    };
    dhx.i18n.setLocale("calendar", localeJa);

    // 2. 指定されたコントロールからカレンダーオブジェクトを取得
    const datepickerControl = formInstance.getItem(controlName);
    if (!datepickerControl) return;

    const calendar = datepickerControl.getWidget();

    // 3. 土日・祝日の色分け設定
    calendar.config.mark = function(date) {
        const day = date.getDay(); // 0:日, 6:土
        const isHoliday = holiday_jp.isHoliday(date); // 外部ライブラリ判定

        if (day === 0 || isHoliday) {
            return "cal-sunday-holiday";
        }
        if (day === 6) {
            return "cal-saturday";
        }
    };

    // 4. 設定を反映して再描画
    calendar.paint();
}