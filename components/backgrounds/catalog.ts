import manifest from '../../data/backgrounds.json';
import { calendarLabel, defaultCalendarDate, type CalendarDate } from '../product/calendar';

export interface CatalogBackground {
  id: string;
  category: string;
  src: string;
  thumbnail: string;
  status: string;
  edited: boolean;
  original_filename: string;
  warnings: string[];
}

// Keep the supplier's IDs, category assignments and review warnings verbatim.
export const catalogBackgrounds = manifest.backgrounds.filter(
  (entry): entry is CatalogBackground => Boolean(entry.src && entry.thumbnail) && entry.status !== 'excluded',
);
export const backgroundCategories = manifest.categories;
export const backgroundById = new Map(catalogBackgrounds.map(entry => [entry.id, entry]));

export interface BackgroundSettings {
  mode: 'catalog' | 'custom' | 'calendar';
  calendar?: CalendarDate;
  catalogId: string;
  photo: { url: string; name: string } | null;
  fit: 'contain' | 'cover';
  x: number;
  y: number;
  zoom: number;
}

export const initialBackgroundSettings: BackgroundSettings = {
  mode: 'catalog', catalogId: 'BG018', photo: null,
  fit: 'cover', x: 50, y: 50, zoom: 1, calendar: defaultCalendarDate,
};

export function backgroundLabel(settings: BackgroundSettings) {
  if (settings.mode === 'calendar') return `Календар — ${calendarLabel(settings.calendar ?? defaultCalendarDate)}`;
  if (settings.mode === 'custom') return settings.photo ? 'Своја фотографија' : 'Нема прикачена фотографија';
  return `Позадина ${settings.catalogId}`;
}
