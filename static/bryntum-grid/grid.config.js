import {AjaxStore, TreeGrid, StringHelper} from './grid.module.js';

const store = new AjaxStore({
  createUrl: "http://127.0.0.1:8000/api/estimate_info/",
  readUrl: "/api/estimate_info/",
  updateUrl: "http://127.0.0.1:8000/api/estimate_info/",
  deleteUrl: "http://127.0.0.1:8000/api/estimate_info/",
  autoLoad: true,
  autoCommit: true,
  useRestfulMethods: true,
  tree: true,
  children: true,
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
        store.updateUrl = `estimate_info/${itemId}/`;
      }
    },
  },

});

let newEstimateCount = 0;

const tree = new TreeGrid({
  appendTo: document.body,
  features: {
    filter: true,
    stripe: true,
    summary: true,
  },

  tbar: [
    {
      type: "buttongroup",
      items: [
        {
          type: "button",
          ref: "addButton",
          color: "b-green",
          icon: "b-fa-plus-circle",
          margin: "0 8 0 0",
          text: "Add",
          tooltip: "Adds a new row (at bottom)",
          onAction: () => {
            const counter = ++newEstimateCount,
              added = grid.store.add({
                estimate_name: `New estimate ${counter}`,
                cls: `new_estimate_${counter}`,
              });

            grid.selectedRecord = added[0];
          },
        },
        {
          type: "button",
          ref: "removeButton",
          color: "b-red",
          icon: "b-fa b-fa-trash",
          text: "Remove",
          tooltip: "Removes selected record(s)",
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
      ],
    },

  ],

  store,

  columns: [
        { field : 'id', text : 'id', flex : 1 },
        { field : 'parentId', text : 'parent', flex : 1 },
        { field : 'estimate_no', text : 'estimate_no', flex : 1 },
        { type : 'tree', field : 'detail_name', text : 'detail_name', flex : 1 },
        { field : 'budget_quantity', text : 'budget_quantity', flex : 1 },
        { field : 'budget_unit', text : 'budget_unit', flex : 1 },
        { field : 'budget_price', text : 'budget_price', flex : 1 },
        { field : 'budget_amount', text : 'budget_amount', flex : 1 },
  ],

});

const {addButton, removeButton} = grid.widgetMap;