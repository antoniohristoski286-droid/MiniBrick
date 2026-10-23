import Link from 'next/link';

export default function NotFound() {
  return <main id="main-content" tabIndex={-1} className="privacy-page container">
    <h1>Страницата не е<br/><em>пронајдена.</em></h1>
    <p className="privacy-intro">Адресата можеби е променета. Вратете се на почетната страница или продолжете кон персонализаторот.</p>
    <Link href="/" className="button button-dark">Кон почетната страница</Link>
  </main>;
}
