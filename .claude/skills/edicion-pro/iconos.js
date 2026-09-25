/* iconos.js — iconos de LÍNEA (trazo blanco, sin relleno) para el estilo dinámico.
   Se ven como en la referencia: blancos con brillo (clase .neon) y se pueden «dibujar» con M.dibuja.
   Uso: el.innerHTML = ICONO('reloj', 220)                                                    */
const ICONOS = {
  persona: '<circle cx="50" cy="32" r="14"/><path d="M22 86v-8a20 20 0 0 1 20-20h16a20 20 0 0 1 20 20v8"/>',
  reloj: '<circle cx="50" cy="50" r="36"/><path d="M50 28v22l14 10"/>',
  sobre: '<rect x="14" y="26" width="72" height="50" rx="4"/><path d="M14 30l36 26 36-26"/>',
  movil: '<rect x="32" y="12" width="36" height="76" rx="7"/><path d="M44 80h12"/>',
  nfc: '<rect x="18" y="16" width="34" height="64" rx="7"/><path d="M30 72h10"/><path d="M62 36a14 14 0 0 1 0 22"/><path d="M70 28a26 26 0 0 1 0 38"/><path d="M78 20a38 38 0 0 1 0 54"/>',
  estrella: '<path d="M50 12l11 24 26 3-19 18 5 26-23-13-23 13 5-26-19-18 26-3z"/>',
  mesa: '<path d="M12 40h76"/><path d="M22 40l-6 44"/><path d="M78 40l6 44"/><path d="M30 40V26h14v14"/>',
  bocadillo: '<path d="M16 22h68v42H44L28 80V64H16z"/>',
  lupa: '<circle cx="42" cy="42" r="24"/><path d="M60 60l24 24"/>',
  check: '<circle cx="50" cy="50" r="36"/><path d="M34 51l11 11 21-24"/>',
  cruz: '<circle cx="50" cy="50" r="36"/><path d="M37 37l26 26M63 37L37 63"/>',
  grafica: '<path d="M14 86h72"/><path d="M18 70l20-20 14 12 30-34"/><path d="M68 28h14v14"/>',
  calendario: '<rect x="14" y="20" width="72" height="64" rx="6"/><path d="M14 38h72M32 12v16M68 12v16"/>',
  euro: '<path d="M72 26a30 30 0 1 0 0 48"/><path d="M18 44h40M18 58h40"/>',
  qr: '<rect x="14" y="14" width="28" height="28"/><rect x="58" y="14" width="28" height="28"/><rect x="14" y="58" width="28" height="28"/><path d="M58 58h10v10M76 58h10M58 78h8M76 72v14h10"/>',
  placa: '<rect x="22" y="10" width="56" height="70" rx="6"/><path d="M22 26h56"/><path d="M50 80v10M34 90h32"/><circle cx="50" cy="52" r="10"/>',
  pulgar: '<path d="M30 46h-14v38h14zM30 48l16-30c8 0 10 6 8 14l-3 12h22c6 0 9 5 8 10l-6 22c-1 5-5 8-10 8H30"/>',
  rayo: '<path d="M56 10L22 56h26l-6 34 36-48H52z"/>',
  flecha: '<path d="M16 50h64M60 30l20 20-20 20"/>',
};
const ICONO = (n, px = 200, sw = 3.2) =>
  `<svg viewBox="0 0 100 100" width="${px}" height="${px}" fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONOS[n]}</svg>`;
