"use client";

import { Receipts, useReceiptStore } from "@/store/ReceiptsStore";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getExpandedRowModel,
  Row,
  useReactTable,
} from "@tanstack/react-table";
import { Fragment, useEffect, useState } from "react";

let test: Receipts[] = [
  {
    id: "12345",
    date: "1° de dezembro de 2025",
    company: "INDÚSTRIAS SALEM",
    phone: "(12) 3456-7890",
    address: "Rua do Ouro, 123 Belém, PA",
    items: [
      {
        id: null,
        name: "Serviço 1",
        price: "R$ 123",
      },
      {
        id: null,
        name: "Serviço 2",
        price: "R$ 123",
      },
      {
        id: null,
        name: "Serviço 3",
        price: "R$ 123",
      },
    ],
    total: "R$ 492",
    subtotal: "R$ 492",
    tax: "R$ 0",
    payment: {
      name: "NATÁLIA SILVA",
      company: "Banco Ouro Preto",
      email: "ola@grandesite.com.br",
      address: "Rua Alegre, 123 - Cidade Brasileira",
      phone: "(12) 3456-7890",
      account_number: "1234-5678",
      due_date: "16/01/2026",
    },
  },
  {
    id: "4553543",
    date: "1° de dezembro de 2025",
    company: "INDÚSTRIAS SALEM",
    phone: "(12) 3456-7890",
    address: "Rua do Ouro, 123 Belém, PA",
    items: [
      {
        id: null,
        name: "Serviço 1",
        price: "R$ 123",
      },
      {
        id: null,
        name: "Serviço 2",
        price: "R$ 123",
      },
      {
        id: null,
        name: "Serviço 3",
        price: "R$ 123",
      },
    ],
    total: "R$ 492",
    subtotal: "R$ 492",
    tax: "R$ 0",
    payment: {
      name: "NATÁLIA SILVA",
      company: "Banco Ouro Preto",
      email: "ola@grandesite.com.br",
      address: "Rua Alegre, 123 - Cidade Brasileira",
      phone: "(12) 3456-7890",
      account_number: "1234-5678",
      due_date: "16/01/2026",
    },
  },
];

const columnHelper = createColumnHelper<Receipts>();

const columns = [
  {
    header: () => null,
    id: "expander",
    cell: ({ row }: { row: Row<Receipts> }) => {
      return (
        <button onClick={row.getToggleExpandedHandler()}>
          {row.getIsExpanded() ? "-" : "+"}
        </button>
      );
    },
  },
  columnHelper.accessor("id", {
    id: "id",
    header: () => "ID",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("date", {
    id: "date",
    header: () => "date",
    cell: (info) => info.getValue(),
  }),
  
  columnHelper.accessor("total", {
    id: "total",
    header: () => "Total",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("subtotal", {
    id: "subtotal",
    header: () => "subtotal",
    cell: (info) => info.getValue(),
  }),
];


type ExpandedState = true | Record<string, boolean>

export default function DisplayReceipts() {
  const store = useReceiptStore((state) => state.list_receipt);
  const [data, setData] = useState<Receipts[]>([]);

  const [expanded, setExpanded] = useState<ExpandedState>({});

  useEffect(() => {
    console.log(store);
    setData(test);
  }, [store]);

  const table = useReactTable({
    data,
    columns,
    getRowCanExpand: (row) => true,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    state: {
      expanded: expanded,
    },
    onExpandedChange: setExpanded,
  });

  return (
    <>
      <table className=" bg-zinc-900 border border-slate-600 border-solid m-4">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className={`w-64 ${header.id === "expander" ? "w-8" : ""}`}
                  style={{ padding: "0.5rem" }}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table
            .getRowModel()
            .rows.slice(0, 10)
            .map((row) => {
              return (
                <Fragment key={row.id}>
                  <tr className=" text-center" key={row.id}>
                    {row.getVisibleCells().map((cell) => {
                      return (
                        <td
                          className={`p-1 ${
                            cell.column.id === "expander" ? "w-1" : ""
                          }`}
                          key={cell.id}
                        >
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </td>
                      );
                    })}
                  </tr>
                  {row.getIsExpanded() && (
                    <tr >
                      <td colSpan={columns.length}>
                        <table className="w-full">
                          <thead>
                            <tr>
                              <th>Item Name</th>
                              <th>Price</th>
                            </tr>
                          </thead>
                          <tbody>
                            {row.original.items.map((item, index) => (
                              <tr key={index}>
                                <td>{item.name}</td>
                                <td>{item.price}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  )}
                </Fragment>
              );
            })}
        </tbody>
      </table>
    </>
  );
}