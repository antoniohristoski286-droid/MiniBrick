export interface CalendarDate { year: number; month: number; day: number }
export const defaultCalendarDate: CalendarDate = { year: 2026, month: 10, day: 26 };
export const months = ['Јануари', 'Февруари', 'Март', 'Април', 'Мај', 'Јуни', 'Јули', 'Август', 'Септември', 'Октомври', 'Ноември', 'Декември'];
export const weekdays = ['П', 'В', 'С', 'Ч', 'П', 'С', 'Н'];
export const MIN_YEAR = 1900;
export const MAX_YEAR = 2100;
export function daysInMonth(year: number, month: number) {
  return new Date(Date.UTC(year, month, 0)).getUTCDate();
}
export function normalizeCalendar(value: CalendarDate): CalendarDate {
  const year = Math.max(MIN_YEAR, Math.min(MAX_YEAR, Math.trunc(value.year) || defaultCalendarDate.year));
  const month = Math.max(1, Math.min(12, Math.trunc(value.month) || 1));
  const day = Math.max(1, Math.min(daysInMonth(year, month), Math.trunc(value.day) || 1));
  return { year, month, day };
}
export function calendarCells(value: CalendarDate): (number | null)[] {
  const { year, month } = normalizeCalendar(value);
  const offset = (new Date(Date.UTC(year, month - 1, 1)).getUTCDay() + 6) % 7;
  return Array.from({ length: 42 }, (_, index) => index < offset || index >= offset + daysInMonth(year, month) ? null : index - offset + 1);
}
export function calendarLabel(value: CalendarDate) {
  const date = normalizeCalendar(value);
  return `${date.day} ${months[date.month - 1].toLowerCase()} ${date.year}`;
}
