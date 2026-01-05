import {AjaxStore, Grid, StringHelper} from './grid.module.js';

const store = new AjaxStore({
  createUrl: "/api/estimate_info/",
  readUrl: "/api/estimate_info/",
  updateUrl: "/api/estimate_info/",
  deleteUrl: "/estimate_info/",
  autoLoad: true,
  autoCommit: true,
  useRestfulMethods: true,
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
        store.updateUrl = `/api/estimate_info/${itemId}/`;
      }
    },
  },

});


const grid = new Grid({
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
    {type: "rownumber"},
    {
      text: "Estimate Name",
      field: "estimate_name",
      width: 260,
      editor: {
        type: 'textfield',
        required: true
      },
    },

    {
      text: "Estimate No",
      field: "estimate_no",
      width: 250,
    },


  ],

});

const {addButton, removeButton} = grid.widgetMap;