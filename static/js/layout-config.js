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
                <!-- flex: 1 で残りのスペースをすべて占有させます -->
                <div class="header-left" style="flex: 1; text-align: left; margin-left: 10px;">
                    <span id="header_client_no"></span>
                    <span id="header_client_name"></span>
                </div>
                <!-- flex: 0 0 auto で幅を自動（コンテンツ幅）にし、margin: 0 auto で中央に寄せます -->
                <div class="header-center" style="flex: 0 0 auto; margin: 0 auto; text-align: center;">
                    <span id="header_report_title"></span>
                    <span id="header_estimate_no"></span>
                    <span id="header_estimate_name"></span>
                </div>
                <!-- 完全に中央に揃えるため、右側にも見えない等幅のスペース（ダミー）を置くと完璧に中央揃えになります -->
                <div class="header-right" style="flex: 1;"></div>
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