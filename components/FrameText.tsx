'use client';
import { useLayoutEffect, useRef } from 'react';
import type { TextLayout } from './config';

/** Keep text layout out of the figure scene, while retaining its existing reserved space. */
export function FrameText({ names, message, date, layout }: { names: string; message: string; date: string; layout: TextLayout }) {
  const slot = useRef<HTMLDivElement>(null);
  const content = useRef<HTMLDivElement>(null);
  const offset = useRef(0);
  const backing = useRef<HTMLDivElement>(null);
  const hasText = Boolean(names || message || date);

  useLayoutEffect(() => {
    const element = slot.current;
    const text = content.current;
    const frame = element?.closest<HTMLElement>('.frame-art');
    if (!element || !text || !frame) return;
    function position() {
      if (!element || !text || !frame) return;
      const frameBox = frame.getBoundingClientRect();
      const slotBox = element.getBoundingClientRect();
      const textHeight = text.getBoundingClientRect().height;
      const baseBottom = slotBox.bottom - frameBox.top - offset.current;
      const safeInset = 6;
      const minimum = safeInset - (baseBottom - textHeight);
      const maximum = frameBox.height - safeInset - baseBottom;
      const frameStyle = getComputedStyle(frame);
      const sceneHeight = frameBox.height - parseFloat(frameStyle.paddingTop) - parseFloat(frameStyle.paddingBottom);
      const requested = layout.vertical / 100 * sceneHeight;
      const next = Math.max(minimum, Math.min(maximum, requested));
      // Pixel offsets are recomputed from the same frame-relative geometry at every size.
      if (Math.abs(next - offset.current) > .01) {
        offset.current = next;
        element.style.transform = `translateY(${next}px)`;
      }
      if (backing.current) {
        const box = text.getBoundingClientRect();
        Object.assign(backing.current.style, { left: `${box.left-frameBox.left}px`, top: `${box.top-frameBox.top}px`, width: `${box.width}px`, height: `${box.height}px` });
      }
    }
    position();
    const observer = new ResizeObserver(position);
    observer.observe(frame);
    observer.observe(element);
    observer.observe(text);
    return () => observer.disconnect();
  }, [layout.vertical, layout.backplate, names, message, date]);

  return <>
    {layout.backplate && hasText && <div ref={backing} className="frame-text-backplate" aria-hidden="true"/>}
    <div ref={slot} className="art-copy configurable-copy" data-text-vertical={layout.vertical}>
    <div ref={content} className={`art-copy-content ${layout.backplate && hasText ? 'art-copy-readable' : ''} ${names.length>48?'art-copy-dense':''}`}>
      <div className="art-names">{names}</div>
      <div className="art-message">{message}</div>
      <div className="art-date">{date}</div>
    </div>
  </div></>;
}
