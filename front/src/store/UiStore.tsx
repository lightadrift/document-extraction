import { create } from 'zustand'


export const useUiStore = create((set) => ({
  isLoading: false,
  setIsLoading: (isLoading: boolean) => set(() => ({ isLoading: isLoading}))
}))



export const UploadStore = create((set) => ({
  isFrameOpen: false,
  setIsFrameOpen: (isFrameOpen: boolean) => set(() => ({isFrameOpen: isFrameOpen}))
}))