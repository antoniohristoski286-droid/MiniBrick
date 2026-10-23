'use client';
import { useEffect, useRef, useState } from 'react';

const supportedTypes = ['image/jpeg', 'image/png', 'image/webp'];

/** Owned by the configurator, so changing steps keeps the photo alive. */
export function usePhotoUpload(url: string | undefined, onPhoto: (photo: { url: string; name: string }) => void) {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const request = useRef(0);
  const pending = useRef<string | null>(null);

  useEffect(() => () => { if (url) URL.revokeObjectURL(url); }, [url]);
  useEffect(() => () => {
    request.current += 1;
    if (pending.current) URL.revokeObjectURL(pending.current);
  }, []);

  function cancel() {
    request.current += 1;
    if (pending.current) URL.revokeObjectURL(pending.current);
    pending.current = null;
    setLoading(false);
    setError('');
  }

  async function upload(file: File) {
    cancel();
    if (!supportedTypes.includes(file.type)) {
      setError('Изберете JPG, PNG или WebP фотографија.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Фотографијата мора да биде помала од 10 MB.');
      return;
    }
    if (!file.size) {
      setError('Датотеката е празна. Изберете друга фотографија.');
      return;
    }
    const token = request.current;
    const nextUrl = URL.createObjectURL(file);
    pending.current = nextUrl;
    setLoading(true);
    try {
      const image = new Image();
      image.src = nextUrl;
      await image.decode();
      if (request.current !== token) return;
      pending.current = null;
      onPhoto({ url: nextUrl, name: file.name });
    } catch {
      if (request.current === token) setError('Фотографијата не може да се отвори. Изберете друга датотека.');
      URL.revokeObjectURL(nextUrl);
    } finally {
      if (request.current === token) {
        pending.current = null;
        setLoading(false);
      }
    }
  }

  return { upload, cancel, error, loading };
}
