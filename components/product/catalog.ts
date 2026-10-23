export type AccessoryId = 'heart' | 'money' | 'gun' | 'pet';
export type PetId = 'dog' | 'dog-white' | 'dog-spotted' | 'cat' | 'cat-black' | 'cat-orange' | 'cat-white';
export interface FigureAccessories { items: AccessoryId[]; pet: PetId }
export type AccessorySelections = Record<string, FigureAccessories>;
export const emptyAccessories: FigureAccessories = { items: [], pet: 'dog' };
export const accessories: { id: AccessoryId; label: string; price: number; image: string }[] = [
  { id: 'heart', label: 'Срце', price: 70, image: '/accessories/heart.png' },
  { id: 'money', label: 'Пари', price: 70, image: '/accessories/money.png' },
  { id: 'gun', label: 'Пиштол', price: 70, image: '/accessories/gun.png' },
  { id: 'pet', label: 'Милениче', price: 150, image: '/accessories/dog-reference.png' },
];
export const pets: { id: PetId; label: string; image: string }[] = [
  { id: 'dog', label: 'Куче', image: '/accessories/dog-reference.png' },
  { id: 'dog-white', label: 'Куче · бело', image: '/accessories/dog-white-reference.png' },
  { id: 'dog-spotted', label: 'Куче · шарено', image: '/accessories/dog-spotted-reference.png' },
  { id: 'cat', label: 'Мачка', image: '/accessories/cat-reference.png' },
  { id: 'cat-black', label: 'Мачка · црна', image: '/accessories/cat-black-reference.png' },
  { id: 'cat-orange', label: 'Мачка · портокалова', image: '/accessories/cat-orange-reference.png' },
  { id: 'cat-white', label: 'Мачка · бела', image: '/accessories/cat-white-reference.png' },
];
export const frameColors = { white: 'Бела', black: 'Црна' } as const;
export type FrameColor = keyof typeof frameColors;

export type FrameFormat = 'standard' | 'a4';

// Exactly four figures use 20 × 25 cm; larger teams use landscape A4.
export const MAX_PREVIEW_FIGURES = 24;
export function frameSize(count: number): string {
  if (count <= 3) return '15 × 20 cm';
  return count === 4 ? '20 × 25 cm' : 'A4';
}
