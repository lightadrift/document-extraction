
import { create } from "zustand";



interface Store<T> {
  value: T;
  setValue: (value: T) => void;
}

const createStore = <T extends unknown>(initialValue: T) => 
  create<Store<T>>((set) => ({
    value: initialValue,
    setValue: (value: T) => set(() => ({ value })),
  }));


interface ModelSelection {
  model: string,
  setModel: (i: string) => void
}



interface Error {
  error: string,
  setError: (i: string) => void
}




export const useUiStore = create((set) => ({
  isLoading: false,
  setIsLoading: (isLoading: boolean) => set(() => ({ isLoading: isLoading })),
}));

export const useUploadStore = create((set) => ({
  isFrameOpen: false,
  setIsFrameOpen: (isFrameOpen: boolean) =>
    set(() => ({ isFrameOpen: isFrameOpen })),
}));

export const useModelStore = create<ModelSelection>((set) => ({
  model: "minicpm", // default
  setModel: (model: string) => set(() => ({ model: model })),
}));

// export const useErrorStore = createStore({ error: "" });

export const useErrorStore = create<Error>((set) => ({
  error: "",
  setError: (err: string) => set(() => ({error: err}))
}))