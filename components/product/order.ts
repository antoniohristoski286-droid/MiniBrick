import type { FrameConfiguration } from '../config';
import { defaultFigureLayout, defaultTextLayout } from '../config';
import { initialBackgroundSettings } from '../backgrounds/catalog';
import { defaultCalendarDate, normalizeCalendar, calendarLabel } from './calendar';
import { accessories, frameColors, frameSize, pets } from './catalog';
import { calculatePrice, denars } from './pricing';

export interface CustomerDetails { name: string; phone: string; address: string; city: string; note: string }
export const emptyCustomer: CustomerDetails = { name: '', phone: '', address: '', city: '', note: '' };
export function validateCustomer(customer: CustomerDetails): Partial<Record<keyof CustomerDetails, string>> {
  const errors: Partial<Record<keyof CustomerDetails, string>> = {};
  if (customer.name.trim().length < 2) errors.name = 'Внесете име и презиме.';
  const phone = customer.phone.trim();
  const digits = phone.replace(/\D/g, '');
  if (!/^[+\d\s()./\-]+$/.test(phone) || digits.length < 6 || digits.length > 18) errors.phone = 'Внесете важечки телефонски број.';
  if (customer.address.trim().length < 3) errors.address = 'Внесете адреса за достава.';
  if (customer.city.trim().length < 2) errors.city = 'Внесете град.';
  return errors;
}

export function createOrderRequest(config: FrameConfiguration, customer: CustomerDetails) {
  const settings = config.backgroundSettings ?? initialBackgroundSettings;
  const visible = config.characters.slice(0, config.figureCount);
  const photo = settings.mode === 'custom';
  const background = settings.mode === 'calendar'
    ? { mode: 'calendar' as const, calendar: normalizeCalendar(settings.calendar ?? defaultCalendarDate) }
    : photo
      ? { mode: 'custom' as const, photo: settings.photo ? { filename: settings.photo.name, attached: false, requiresSeparateDelivery: true } : null, fit: settings.fit, x: settings.x, y: settings.y, zoom: settings.zoom }
      : { mode: 'catalog' as const, catalogId: settings.catalogId };
  return {
    schemaVersion: 1,
    status: 'prepared-not-submitted' as const,
    product: { figureCount: config.figureCount, frameColor: config.frameColor ?? 'white', frameSize: frameSize(config.figureCount), orientation: config.figureCount>4?'landscape' as const:'portrait' as const, sizeRequiresConfirmation: false, occasion: config.occasion },
    background,
    characters: visible.map((character, index) => {
      const selection = config.accessories?.[character.id];
      return {
        id: character.id, type: character.type, name: (config.names[index] ?? '').trim(), faceId: character.faceId,
        ...(character.type === 'baby' ? { babyBodyColorId: character.babyBodyColorId } : { hairId: character.hairId, torsoColorId: character.torsoColorId, legsColorId: character.legsColorId }),
        accessories: accessories.filter(item => selection?.items.includes(item.id)).map(item => ({ id: item.id, quantity: 1, unitPrice: item.price, ...(item.id === 'pet' ? { variant: selection?.pet ?? 'dog' } : {}), artwork: item.id === 'pet' ? 'approximate-reference-derived-cutout' : 'approximate-generated-illustration' })),
      };
    }),
    personalization: { names: config.names.slice(0, config.figureCount).map(name => name.trim()), message: config.message.trim(), date: config.date.trim() },
    composition: { figures: config.figureLayout ?? defaultFigureLayout, text: config.textLayout ?? defaultTextLayout },
    pricing: calculatePrice(visible.map(character => character.id), config.accessories),
    customer: Object.fromEntries(Object.entries(customer).map(([key, value]) => [key, value.trim()])) as unknown as CustomerDetails,
    estimatedProductionAndDelivery: '2–3 работни дена',
  };
}
export type OrderRequest = ReturnType<typeof createOrderRequest>;
export function formatOrderRequest(order: OrderRequest) {
  const types = { male: 'Машки', female: 'Женски', child: 'Дете', baby: 'Новороденче' };
  const background = order.background.mode === 'calendar' ? `Календар — ${calendarLabel(order.background.calendar)}` : order.background.mode === 'catalog' ? `Позадина ${order.background.catalogId}` : `Своја фотографија: ${order.background.photo?.filename ?? 'не е избрана'} (НЕ е приложена; потребно е одделно доставување)`;
  return [
    'MINIBRICK.MK — ПОДГОТВЕНО БАРАЊЕ', 'Барањето НЕ е испратено до MiniBrick.', '',
    `Фигури: ${order.product.figureCount}`, `Рамка: ${frameColors[order.product.frameColor]}`, `Големина: ${order.product.frameSize}`, `Ориентација: ${order.product.orientation==='landscape'?'Хоризонтална':'Вертикална'}`, `Повод: ${order.product.occasion}`, `Дизајн: ${background}`,
    ...(order.background.mode === 'custom' ? [`Фотографија: ${order.background.fit}; x ${order.background.x}%; y ${order.background.y}%; зголемување ${order.background.zoom}×`] : []), '',
    ...order.characters.map((character, i) => `Фигура ${i + 1} (${character.id}): ${types[character.type]}; ${character.name || 'без име'}; лице ${character.faceId}; ${'babyBodyColorId' in character ? `тело ${character.babyBodyColorId}` : `фризура ${character.hairId}; горен дел ${character.torsoColorId}; долен дел ${character.legsColorId}`}; додатоци: ${character.accessories.map(item => `${accessories.find(option => option.id === item.id)?.label}${item.id === 'pet' ? ` (${pets.find(pet => pet.id === item.variant)?.label})` : ''}`).join(', ') || 'нема'}`), '',
    `Имиња: ${order.personalization.names.filter(Boolean).join(' & ') || '—'}`, `Порака: ${order.personalization.message || '—'}`, `Датум во текстот: ${order.personalization.date || '—'}`,
    `Положба на фигурите: ${order.composition.figures.vertical}%; растојание ${order.composition.figures.spacing}%`, `Положба на текстот: ${order.composition.text.vertical}%; подлога: ${order.composition.text.backplate ? 'да' : 'не'}`, '',
    `Основна цена: ${denars(order.pricing.base)}`,
    ...order.pricing.lines.map(line => `${line.label} × ${line.quantity}: ${denars(line.total)}`),
    `Додатоци вкупно: ${denars(order.pricing.accessorySubtotal)}`, `Достава: ${denars(order.pricing.delivery)}`, `ВКУПНО: ${denars(order.pricing.total)}`, `Проценета изработка и достава: ${order.estimatedProductionAndDelivery}`, '',
    `Име и презиме: ${order.customer.name}`, `Телефон: ${order.customer.phone}`, `Адреса: ${order.customer.address}`, `Град: ${order.customer.city}`, `Забелешка: ${order.customer.note || '—'}`, '',
    'Илустрациите на додатоците се приближни. Конечниот изглед се потврдува при договор за нарачката.',
  ].join('\n');
}
