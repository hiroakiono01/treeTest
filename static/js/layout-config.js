// レイアウトの設定オブジェクトのみを共通化してエクスポート
window.MySharedLayoutConfig = {
    type: "line",
    rows: [
        {
            id: "toolbar_container",
            height: "60px",
            css: "layout-header"
        },
        {
            id: "main_content_row",
            cols: [
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
            html: "Copyright &copy; kag holdings inc 2025",
            height: "30px",
            css: "layout-footer"
        }
    ]
};
