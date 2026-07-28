// レイアウトの設定オブジェクトのみを共通化してエクスポート
window.MySharedLayoutConfig = {
    type: "line",
    rows: [
        {
            id: "my_header_container",
            height: "40px",
            css: "my-layout-header",
            html: `
        <div style="display: flex; width: 100%; height: 100%; align-items: center;">
                        <div class="header-left" style="flex: 1; width: 33.33%; text-align: left; margin-left: 10px;">
                <span id="header_client_no"></span>
                <span id="header_client_name"></span>
            </div>
            <div class="header-center" style="flex: 1; width: 33.33%; text-align: center;">
                <span id="header_report_title"></span>
                <span id="header_estimate_no"></span>
                <span id="header_estimate_name"></span>
            </div>
            <div class="header-right" style="flex: 1; width: 33.33%; text-align: right;"></div>
        </div>
    `

        },
        {
            id: "toolbar_container",
            height: "60px",
            css: "layout-header"
        },
        {
            id: "main_content_row",
            cols: [
                {
                    id: "sidebar_container",
                    rows: [
                        { id: "sidebar_cell" }
                    ],
                    header: "検索",
                    align: "center",
                    collapsable: true,
                    width: "400px",
                    css: "sidebar-border-left" // ★ここに作成したCSSクラスを指定します

                },
                {
                    id: "grid_and_page_container",
                    rows: [
                        { id: "grid_cell" },

                        {
                            id: "pagination_cell",
                            height: "60px"
                        }
                    ],
                    css: "layout-content"
                }
            ]
        },
        {
            id: "footer_cell",
            html: "Copyright &copy; kag holdings inc 2026",
            height: "30px",
            css: "layout-footer"
        }
    ]
};