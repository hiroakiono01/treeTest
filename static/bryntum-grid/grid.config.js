import {AjaxStore, TreeGrid, StringHelper, Combo, GridRowModel, Toast} from './grid.module.js';


// 金額の計算
class Item extends GridRowModel {
    static fields = [
        { name : 'estimate_no' },
        { name : 'detail_name' },
        { name : 'budget_price', type : 'number', defaultValue : 0 },
        { name : 'budget_quantity', type : 'number', defaultValue : 0 },
        // Calculated field
        { name : 'budget_amount', type : 'number', defaultValue : 0, calculate : record => record.budget_price * record.budget_quantity }
    ];
}

// Transform a parent node to a leaf node when all its children are removed
Item.convertEmptyParentToLeaf = true;

// 単位のデータをサーバーから取得
const response = await fetch("/api/unit_info/");
const unitItems = await response.json();

const store = new AjaxStore({
    createUrl: "/api/estimateD_info/",
    readUrl: "/api/estimateD_info/",
    updateUrl: "/api/estimateD_info/",
    deleteUrl: "/api/estimateD_info/",
    autoLoad: true,
    autoCommit: false,
    useRestfulMethods: true,
    transformFlatData : true,
    sendAsFormData : true,
    tree: true,
    modelClass : Item,
    parentIdParamName : "parent",

    httpMethods: {
    read: "GET",
    create: "POST",
    update: "PATCH",
    delete: "DELETE",
    },
    listeners: {

        beforeRequest: (event) => {
            if (event.action === "create") {
                const newItem = event.body.data[0];
                delete newItem.id;
                event.body = newItem;
            }
            if (event.action === "update") {
                const updatedItem = event.body.data[0];
                const itemId = updatedItem.id;
                delete updatedItem.id;
                event.body = updatedItem;
                store.updateUrl = `/estimate_info/${itemId}/`;
            }
                if (event.action === "delete") {
                const itemIds = event.body.ids;
                store.deleteUrl = `/estimate_info/${itemIds[0]}/`;
            }
        },
    },
});

let newPlayerCount = 0;

const　grid = new TreeGrid({
    appendTo: document.body,
    store,
    modelClass : Item,
    features: {
        filter: false,
        stripe: true,
        summary: true,
        sort    :false,
        rowReorder : true,
    },
    // Show changed cells
    showDirty : true,
    listeners : {
        selectionChange({ selection }) {
            removeButton.disabled = !selection.length;
            resetButton.disabled = false;
    }
    },
    tbar: [
        {
            type: "buttongroup",
            ref:'addButtonGroup',
            items: [
                {
                    type: "button",
                    ref: "addButton",
                    color: "b-green",
                    icon: "fa-plus-circle",
                    margin: "0 8 0 0",
                    text: "Add",
                    tooltip: "Adds a new row (at bottom)",
                    onAction: () => {

                        const counter = ++newPlayerCount,
                        added = grid.store.add({
                            name: `New player ${counter}`,
                            cls: `new_player_${counter}`,
                        });
                    grid.selectedRecord = added[0];
                    submitButton.disabled = false;
                    resetButton.disabled = false;
                    },
                },
                {
                    type     : 'button',
                    ref      : 'insertButton',
                    icon     : 'fa fa-plus-square',
                    text     : 'Insert',
                    tooltip  : 'Inserts a new row (below selected or at top)',
                    onAction : async () => {
                                            const counter = ++newPlayerCount;
                                            let added;

                                            if (grid.selectedRecords) {
                                                const selectedRecord = grid.selectedRecord;

                                                added = selectedRecord.appendChild({
                                                    name : `New player ${counter}`,
                                                    cls  : `new_player_${counter}`
                                                });
                                                if (!selectedRecord.isLeaf && !selectedRecord.isExpanded(grid.store)){
                                                    await grid.expand(selectedRecord);
                                                }
                                            } else {

                                            added   = grid.store.insert(0, {
                                                name : `New player ${counter}`,
                                                cls  : `new_player_${counter}`
                                            });

                                        }
                        grid.selectedRecord = added[0];
                        submitButton.disabled = false;
                        resetButton.disabled = false;
                    }
                },
            ]
        },
        {
            type: "button",
            ref: "removeButton",
            color: "red",
            icon: "fa-trash",
            text: "Remove",
            tooltip: "Removes selected record(s)",
            disabled : true,
            onAction: () => {
                const selected = grid.selectedRecords;
                if (selected && selected.length) {
                    const store = grid.store,
                    nextRecord = store.getNext(selected[selected.length - 1]),
                    prevRecord = store.getPrev(selected[0]);
                    store.remove(selected);
                    grid.selectedRecord = nextRecord || prevRecord;
                }
            },
        },

        {
            type     : 'button',
            ref      : 'submitButton',
            text     : 'Submit',
            icon     : "fa-pen-to-square",
            cls      : 'b-green',
            tooltip  : 'Sync changes to the server (added, modified and removed rows)',
            disabled : false,
            onAction : async() => {
                // Logic to sync change to the server
                await grid.store.commit();
                Toast.show('Changes synced to server');
            }
        },
        {
            type     : 'button',
            ref      : 'expandAllButton',
            icon     : 'fa-angle-double-down',
            text     : 'Expand all',
            onAction : () => grid.expandAll()
        },
        {
            type     : 'button',
            ref      : 'collapseAllButton',
            icon     : 'fa-angle-double-up',
            text     : 'Collapse all',
            onAction : () => grid.collapseAll()
        },
        '->',
        {
            type     : 'button',
            ref      : 'resetButton',
            color    : 'b-red',
            icon     : 'fa fa-recycle',
            text     : 'Reset',
            tooltip  : 'Reset rows',
            disabled : true,
            onAction : () => grid.store.load({ reset : true }).then(() => Toast.show('Database was reset'))
        }
    ],




    columns: [
        { type :  "tree" , field : 'detail_name', text : 'detail_name', required: true, flex : 1},
        { text : 'ParentIndex', field : 'parentIndex', hidden : false , flex : 1},
        { field : 'estimate_no', text : 'estimate_no', flex : 1 },
        { type : 'number', field : 'budget_quantity', text : 'budget_quantity', flex : 1 },
        {
            field : 'budget_unit',
            text : 'budget_unit',
            renderer : ({ value, column }) => {
                const editor = column.editor;
                return editor.store.getById(value)?.[editor.displayField] || value;
            },
            editor : {
                type :'combo',
                editable: false,
                autoExpand :true,
                items:unitItems,
                valueField :'id',
                displayField:'unit_name',
                },
            flex : 1

        },
        { type : 'number', field : 'budget_price', text : 'budget_price', flex : 1 },
    //        { type : 'aggregate', field : 'budget_amount', text : 'budget_amount', flex : 1 },
        {
            type : 'aggregate',
            text : 'budget_amount',
            field : 'budget_amount',
            width : 190,
            sum : 'sum',
            align : 'end',
            summaryRenderer : ({ sum }) => `Total amount: ${sum}`,
        }
    ],

    onChange() {
        submitButton.disabled = false;
        resetButton.disabled =  false;
//            this.features.summary.selectedOnly = !this.features.summary.selectedOnly;
        }
});

const {addButtonGroup, removeButton, submitButton, resetButton} = grid.widgetMap;