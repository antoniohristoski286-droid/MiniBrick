'use client';
import { calendarCells, calendarLabel, daysInMonth, MAX_YEAR, MIN_YEAR, months, normalizeCalendar, weekdays, type CalendarDate } from './calendar';
import styles from './product.module.css';

export function CalendarControls({ value, onChange }: { value: CalendarDate; onChange: (date: CalendarDate) => void }) {
  const update = (patch: Partial<CalendarDate>) => onChange(normalizeCalendar({ ...value, ...patch }));
  return <fieldset className={styles.panel}><legend>Вашиот посебен датум</legend>
    <div className={styles.dateFields}>
      <label>Месец<select aria-label="Месец" value={value.month} onChange={e => update({ month: Number(e.target.value) })}>{months.map((name, i) => <option key={name} value={i + 1}>{name}</option>)}</select></label>
      <label>Година<select aria-label="Година" value={value.year} onChange={e => update({ year: Number(e.target.value) })}>{Array.from({ length: MAX_YEAR - MIN_YEAR + 1 }, (_, i) => MIN_YEAR + i).map(year => <option key={year}>{year}</option>)}</select></label>
      <label>Ден<select aria-label="Ден" value={value.day} onChange={e => update({ day: Number(e.target.value) })}>{Array.from({ length: daysInMonth(value.year, value.month) }, (_, i) => i + 1).map(day => <option key={day}>{day}</option>)}</select></label>
    </div>
    <p className={styles.note}>Избрано: {calendarLabel(value)}. Црвениот круг го означува само вашиот датум. При промена на месецот, денот се приспособува ако е потребно.</p>
  </fieldset>;
}

/** No baked-in month or circle: every cell and the highlight come from the saved date. */
export function CalendarDesign({ value }: { value: CalendarDate }) {
  const date = normalizeCalendar(value);
  return <svg className="calendar-design" viewBox="0 0 700 510" role="img" aria-label={`Календар — ${calendarLabel(date)}`} data-background-id="calendar" data-calendar-date={`${date.year}-${date.month}-${date.day}`}>
    <rect x="12" y="12" width="676" height="486" fill="white" stroke="#27231f" strokeWidth="1"/>
    <text x="350" y="73" textAnchor="middle" fontFamily="Georgia, serif" fontSize="34" fill="#201a17">{months[date.month - 1].toUpperCase()} {date.year}</text>
    <path d="M64 99H636" stroke="#27231f"/>
    {weekdays.map((label, index) => <text key={index} x={88 + index * 87} y="140" textAnchor="middle" fontFamily="Georgia, serif" fontSize="20" fill="#706964">{label}</text>)}
    {calendarCells(date).map((day, index) => day === null ? null : <g key={index} data-calendar-day={day} data-selected={day === date.day}>
      {day === date.day && <circle cx={88 + index % 7 * 87} cy={182 + Math.floor(index / 7) * 55} r="23" fill="none" stroke="#b92320" strokeWidth="2.5"/>}
      <text x={88 + index % 7 * 87} y={190 + Math.floor(index / 7) * 55} textAnchor="middle" fontFamily="Georgia, serif" fontSize="25" fill="#201a17">{day}</text>
    </g>)}
  </svg>;
}
