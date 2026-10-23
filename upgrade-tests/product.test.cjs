/* eslint-disable @typescript-eslint/no-require-imports -- This CommonJS test loader runs TS helpers with the installed compiler. */
/* Use the project's TypeScript compiler for a dependency-free Node test loader. */
const ts = require('typescript');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const originalResolve = Module._resolveFilename;
Module._resolveFilename = function (request, parent, ...args) {
  return originalResolve.call(this, request.startsWith('@/') ? path.join(root, request.slice(2)) : request, parent, ...args);
};
require.extensions['.ts'] = (module, filename) => module._compile(ts.transpileModule(fs.readFileSync(filename, 'utf8'), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true } }).outputText, filename);
const { basePrice, calculatePrice } = require('../components/product/pricing.ts');
const { calendarCells, normalizeCalendar, daysInMonth } = require('../components/product/calendar.ts');
const { pets, frameSize } = require('../components/product/catalog.ts');
const { createOrderRequest, formatOrderRequest, validateCustomer } = require('../components/product/order.ts');
const { initialConfig } = require('../components/config.ts');
const { initialBackgroundSettings } = require('../components/backgrounds/catalog.ts');
const { ensureCharacterCount } = require('../components/characters/state.ts');
const ids = n => Array.from({ length: n }, (_, i) => `figure-${i + 1}`);
let cases = 0;
const check = (value, expected) => { assert.deepEqual(value, expected); cases++; };
const bases = [1290, 1690, 2090, 2490, 2840, 3190, 3540, 3890];
for (let count = 1; count <= 8; count++) { check(basePrice(count), bases[count - 1]); check(calculatePrice(ids(count)).total, bases[count - 1] + 170); check(calculatePrice(ids(count)).accessorySubtotal, 0); }
assert.throws(() => basePrice(0), RangeError); assert.throws(() => basePrice(1.5), RangeError);
for (let mask = 0; mask < 16; mask++) {
  const all = ['heart', 'money', 'gun', 'pet']; const items = all.filter((_, i) => mask & (1 << i));
  const subtotal = items.reduce((sum, id) => sum + (id === 'pet' ? 150 : 70), 0);
  const selections = { 'figure-1': { items, pet: 'cat' }, 'figure-2': { items: ['heart'], pet: 'dog' }, 'figure-8': { items: ['pet'], pet: 'dog' } };
  const result = calculatePrice(ids(2), selections);
  check(result.accessorySubtotal, subtotal + 70); check(result.total, 1690 + subtotal + 70 + 170);
  check(calculatePrice(ids(1), selections).accessorySubtotal, subtotal);
}
check(calculatePrice(ids(2), { 'figure-1': { items: ['heart', 'pet'], pet: 'cat' } }).total, 2080);
check(calculatePrice(ids(1), { 'figure-1': { items: ['heart', 'heart'], pet: 'dog' } }).accessorySubtotal, 70);
for (let count = 1; count <= 8; count++) {
  check(frameSize(count), count <= 3 ? '15 × 20 cm' : count === 4 ? '20 × 25 cm' : 'A4');
  for (const format of ['standard', 'a4']) {
    const expected = count <= 3 ? '15 × 20 cm' : count === 4 ? '20 × 25 cm' : 'A4';
    check(frameSize(count, format), expected);
    const request = createOrderRequest({ ...initialConfig, figureCount: count, characters: ensureCharacterCount(initialConfig.characters, count), frameFormat: format }, { name: '', phone: '', address: '', city: '', note: '' });
    check(request.product.frameSize, expected); check(request.product.orientation, count>4?'landscape':'portrait'); check(request.product.sizeRequiresConfirmation, false);
    check(formatOrderRequest(request).includes(`Големина: ${expected}`), true);
  }
}
for (const count of [9,12,24]) {
  const request = createOrderRequest({ ...initialConfig, figureCount: count, characters: ensureCharacterCount(initialConfig.characters, count) }, { name:'',phone:'',address:'',city:'',note:'' });
  check(request.characters.length,count); check(request.product.frameSize,'A4'); check(request.product.orientation,'landscape'); check(request.pricing.total,2490+(count-4)*350+170);
}
check(daysInMonth(2024, 2), 29); check(daysInMonth(2100, 2), 28); check(daysInMonth(2000, 2), 29);
check(normalizeCalendar({ year: 2024, month: 2, day: 31 }), { year: 2024, month: 2, day: 29 });
check(normalizeCalendar({ year: 2025, month: 2, day: 29 }), { year: 2025, month: 2, day: 28 });
// Reference October 2026 begins on Thursday: Monday-first offset is three.
check(calendarCells({ year: 2026, month: 10, day: 26 }).indexOf(1), 3);
for (let year = 1900; year <= 2100; year++) for (let month = 1; month <= 12; month++) {
  const cells = calendarCells({ year, month, day: 1 });
  check(cells.filter(Boolean).length, daysInMonth(year, month));
  check(cells.indexOf(1), (new Date(Date.UTC(year, month - 1, 1)).getUTCDay() + 6) % 7);
  check(cells.length, 42);
}
const customer = { name: 'Тест Корисник', phone: '+389 (70) 123-456', address: 'Тест адреса 12', city: 'Скопје', note: '' };
check(validateCustomer(customer), {}); check(validateCustomer({ ...customer, phone: '070/123-456' }), {});
check(Object.keys(validateCustomer({ name: '', phone: 'abc', address: '', city: '', note: '' })).length, 4);
const config = { ...initialConfig, frameColor: 'black', backgroundSettings: { ...initialBackgroundSettings, mode: 'custom', photo: { url: 'blob:private-photo', name: 'personal.png' }, x: 23, y: 77, zoom: 1.6, fit: 'cover' }, figureLayout: { vertical: -12, spacing: 45 }, textLayout: { vertical: -30, backplate: true }, accessories: { 'figure-1': { items: ['heart', 'pet'], pet: 'cat' } } };
const order = createOrderRequest(config, customer);
check(order.pricing.total, 2080); check(order.background.photo.attached, false); check(order.product.frameColor, 'black');
check(JSON.stringify(order).includes('blob:'), false); check(formatOrderRequest(order).includes('blob:'), false);
check(order.composition.figures, config.figureLayout); check(order.customer.name, customer.name);
check(formatOrderRequest(order).includes('НЕ е приложена'), true); check(order.status, 'prepared-not-submitted');
const characters = ensureCharacterCount(config.characters, 8); characters[1] = { ...characters[1], type: 'baby', faceId: 'B02' };
const baby = createOrderRequest({ ...config, characters, figureCount: 8 }, customer).characters[1];
check('hairId' in baby, false); check('torsoColorId' in baby, false); check('legsColorId' in baby, false); check('babyBodyColorId' in baby, true);
const calendarOrder = createOrderRequest({ ...config, backgroundSettings: { ...initialBackgroundSettings, mode: 'calendar', calendar: { year: 2024, month: 2, day: 29 } } }, customer);
check(calendarOrder.background.calendar, { year: 2024, month: 2, day: 29 }); check(formatOrderRequest(calendarOrder).includes('29 февруари 2024'), true);
for (const pet of pets) {
  const selections = { 'figure-1': { items: ['pet'], pet: pet.id } };
  check(calculatePrice(ids(2), selections).total, 2010);
  check(createOrderRequest({ ...config, accessories: selections }, customer).characters[0].accessories[0].variant, pet.id);
}
const report = { petVariants: pets.length, checks: cases, basePrices: bases, calendarMonths: 201 * 12, accessoryCombinations: 16, exampleTotal: 2080, orderSanitization: 'passed', newbornFields: 'passed' };
fs.writeFileSync(path.join(root, 'artifacts/upgrade/unit-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report));
