import { notFound } from 'next/navigation';
import CharacterTestingView from '@/components/characters/CharacterTestingView';
export default function CharacterTestingPage() {
  if (process.env.NODE_ENV !== 'development') notFound();
  return <CharacterTestingView/>;
}
