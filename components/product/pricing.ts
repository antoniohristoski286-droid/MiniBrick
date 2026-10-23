import { accessories, type AccessorySelections } from './catalog';
export const DELIVERY_PRICE = 170;
export function basePrice(count: number) {
  if (!Number.isInteger(count) || count < 1) throw new RangeError('Invalid figure count');
  return count <= 4 ? [1290, 1690, 2090, 2490][count - 1] : 2490 + (count - 4) * 350;
}
export function calculatePrice(figureIds: string[], selections: AccessorySelections = {}) {
  const lines = accessories.map(accessory => {
    const quantity = figureIds.reduce((sum, id) => sum + (selections[id]?.items.includes(accessory.id) ? 1 : 0), 0);
    return { id: accessory.id, label: accessory.label, unitPrice: accessory.price, quantity, total: quantity * accessory.price };
  }).filter(line => line.quantity > 0);
  const base = basePrice(figureIds.length);
  const accessorySubtotal = lines.reduce((sum, line) => sum + line.total, 0);
  return { currency: 'MKD' as const, base, lines, accessorySubtotal, delivery: DELIVERY_PRICE, total: base + accessorySubtotal + DELIVERY_PRICE };
}
// Deterministic grouping avoids server/browser ICU locale differences during hydration.
export function denars(value: number) { return `${String(value).replace(/\B(?=(\d{3})+(?!\d))/g, '.')} ден.`; }
