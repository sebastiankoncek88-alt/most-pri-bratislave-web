// Počasie pre Most pri Bratislave – Open-Meteo (bez kľúča, bez cookies, CC BY 4.0)
export const WEATHER_URL =
  'https://api.open-meteo.com/v1/forecast?latitude=48.1424&longitude=17.2719' +
  '&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day' +
  '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max' +
  '&timezone=Europe%2FBratislava&forecast_days=7';

// WMO kódy počasia -> slovenský popis a ikona
export function describe(code: number, isDay = 1): { text: string; icon: string } {
  if (code === 0) return { text: 'Jasno', icon: isDay ? 'sun' : 'moon' };
  if (code === 1) return { text: 'Prevažne jasno', icon: isDay ? 'sun' : 'moon' };
  if (code === 2) return { text: 'Polojasno', icon: isDay ? 'cloud-sun' : 'cloud-moon' };
  if (code === 3) return { text: 'Zamračené', icon: 'cloud' };
  if (code === 45 || code === 48) return { text: 'Hmla', icon: 'cloud-fog' };
  if (code >= 51 && code <= 57) return { text: 'Mrholenie', icon: 'cloud-drizzle' };
  if (code >= 61 && code <= 67) return { text: code >= 65 ? 'Silný dážď' : 'Dážď', icon: 'cloud-rain' };
  if (code >= 71 && code <= 77) return { text: 'Sneženie', icon: 'cloud-snow' };
  if (code >= 80 && code <= 82) return { text: 'Prehánky', icon: 'cloud-sun-rain' };
  if (code === 85 || code === 86) return { text: 'Snehové prehánky', icon: 'cloud-snow' };
  if (code >= 95) return { text: 'Búrka', icon: 'cloud-lightning' };
  return { text: '', icon: 'cloud' };
}
export const WEATHER_ICONS = ['sun', 'moon', 'cloud-sun', 'cloud-moon', 'cloud', 'cloud-fog', 'cloud-drizzle', 'cloud-rain', 'cloud-snow', 'cloud-sun-rain', 'cloud-lightning'];

// Spoločné načítanie s 30-min. vyrovnávacou pamäťou v prehliadači
export async function loadWeather(): Promise<any | null> {
  try {
    const c = sessionStorage.getItem('weather');
    if (c) { const j = JSON.parse(c); if (Date.now() - j.t < 30 * 60 * 1000) return j.d; }
  } catch {}
  try {
    const r = await fetch(WEATHER_URL);
    if (!r.ok) return null;
    const d = await r.json();
    if (d.error || !d.current) return null;
    try { sessionStorage.setItem('weather', JSON.stringify({ t: Date.now(), d })); } catch {}
    return d;
  } catch { return null; }
}
