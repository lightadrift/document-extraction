import { create } from 'zustand'


export interface Item {
  id: string | null;
  name: string;
  price: string;
}

export interface Payment {
  name: string;
  company: string;
  email: string;
  address: string;
  phone: string;
  account_number: string;
  due_date: string;
}

export interface Receipts {
  id: string;
  date: string;
  company: string;
  phone: string;
  address: string;
  items: Item[];
  subtotal: string;
  total: string;
  tax: string;
  payment: Payment;
}

interface StoreType {
 list_receipt: Array<Receipts>
 updateListReceipts: (new_rcps: Array<Receipts>) => void;
}

export const useReceiptStore = create<StoreType>((set) => ({
  list_receipt: [], 
  updateListReceipts: (new_rcps: Array<Receipts>) => set((state) => ({list_receipt: [...state.list_receipt, ...new_rcps]}))
}))