// Základné údaje obce – upravujú sa na jednom mieste a prejavia sa na celom webe.

export const obec = {
  name: 'Most pri Bratislave',
  fullName: 'Obec Most pri Bratislave',
  address: 'Bratislavská 96/98',
  zip: '900 46',
  city: 'Most pri Bratislave',
  phone: '02 / 4595 1215',
  phoneHref: '+421245951215',
  email: 'sekretariat@mostpribratislave.sk',
  emailStarosta: 'starosta@mostpribratislave.sk',
  ico: '00 304 964',
  dic: '2020662204',
  iban: 'SK13 0200 0000 0029 9688 4553',
  bank: 'VÚB, a. s.',
  facebook: 'https://www.facebook.com/obecMostpriBratislave/',
  mapUrl: 'https://www.openstreetmap.org/?mlat=48.1424&mlon=17.2719#map=17/48.1424/17.2719',
  population: '4 517',
  populationNote: 'k 31. 12. 2024',
  firstMention: 1238,
};

// Stránkové hodiny obecného úradu (0 = nedeľa ... 6 = sobota)
// Každý deň: zoznam intervalov [od, do] v tvare "HH:MM". Prázdny zoznam = nestránkový deň.
export const officeHours: Record<number, [string, string][]> = {
  1: [['08:00', '12:00'], ['13:00', '16:30']],
  2: [],
  3: [['08:00', '12:00'], ['13:00', '16:30']],
  4: [],
  5: [['08:00', '12:00']],
  6: [],
  0: [],
};
export const dayNames = ['Nedeľa', 'Pondelok', 'Utorok', 'Streda', 'Štvrtok', 'Piatok', 'Sobota'];
export const officeHoursNote = 'Stavebný úrad má v piatok nestránkový deň.';

// Upozornenie v hornej lište webu – upravuje sa v administrácii (src/data/alerts.json)
import alertsData from './alerts.json';
export const alerts: { text: string; href?: string; until?: string }[] = alertsData;

// Hlavné sekcie webu = hlavné menu
export const sections = [
  {
    id: 'urad',
    title: 'Úrad a služby',
    short: 'Úrad',
    icon: 'landmark',
    description: 'Matrika, trvalý pobyt, dane a poplatky, stavebný úrad, tlačivá a kontakty na referáty.',
  },
  {
    id: 'odpady',
    title: 'Odpady',
    short: 'Odpady',
    icon: 'recycle',
    description: 'Harmonogram vývozu, zber objemného a elektroodpadu, konáre, textil a reklamácie.',
  },
  {
    id: 'samosprava',
    title: 'Samospráva',
    short: 'Samospráva',
    icon: 'users',
    description: 'Starostka, zastupiteľstvo, komisie, uznesenia, VZN, rozpočet a rozvoj obce.',
  },
  {
    id: 'uradna-tabula',
    title: 'Úradná tabuľa',
    short: 'Úradná tabuľa',
    icon: 'file-text',
    description: 'Úradná tabuľa, zmluvy, faktúry, objednávky, verejné obstarávanie, voľby a dokumenty.',
  },
  {
    id: 'aktuality',
    title: 'Aktuality',
    short: 'Aktuality',
    icon: 'newspaper',
    description: 'Novinky z obce, podujatia, projekty a obecný spravodaj.',
  },
  {
    id: 'obec',
    title: 'Život v obci',
    short: 'Obec',
    icon: 'trees',
    description: 'O obci a jej histórii, školy, zdravie, služby, kultúra, kluby a spolky.',
  },
] as const;

export type SectionId = (typeof sections)[number]['id'] | 'kontakt';

// Rýchle odkazy na úvodnej stránke – „Čo potrebujete vybaviť?“
export const quickLinks = [
  { title: 'Vývoz odpadu', text: 'Harmonogram 2026', href: '/odpady/harmonogram/harmonogram-na-rok-2026/', icon: 'trash-2' },
  { title: 'Dane a poplatky', text: 'Daň z nehnuteľností, psy, odpad', href: '/urad/dane-a-poplatky/', icon: 'wallet' },
  { title: 'Trvalý pobyt', text: 'Prihlásenie, odhlásenie, potvrdenie', href: '/urad/evidencia-obyvatelstva/', icon: 'house' },
  { title: 'Matrika', text: 'Narodenie, sobáš, úmrtie, výpisy', href: '/urad/matrika/', icon: 'scroll-text' },
  { title: 'Stavebný úrad', text: 'Tlačivá a elektronické podanie', href: '/urad/stavebny-urad/', icon: 'hard-hat' },
  { title: 'Úradná tabuľa', text: 'Oznámenia a zverejnené dokumenty', href: '/uradna-tabula/uradna-tabula/', icon: 'clipboard-list' },
  { title: 'Kultúrny dom', text: 'Prenájom sály a telocvične', href: '/obec/kulturny-dom/', icon: 'calendar-days' },
  { title: 'Nahlásiť problém', text: 'Podnet pre obec', href: '/nahlasit-problem/', icon: 'message-square-warning' },
];

// Pomocná funkcia: odkaz s ohľadom na base path (GitHub Pages)
export function url(path: string) {
  if (/^(https?:|mailto:|tel:|#)/.test(path)) return path;
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return base + (path.startsWith('/') ? path : '/' + path);
}

// Kontakty na referáty obecného úradu (zdroj: pôvodný web obce)
export const contacts = [
  { title: 'Starostka obce', people: 'Mgr. Katarína Rentková, PhD.', email: 'starosta@mostpribratislave.sk', phone: '0911 714 647', href: '/samosprava/starosta/' },
  { title: 'Podateľňa a sekretariát', people: 'Gabriela Vallová (zastupuje Mgr. Renáta Jurašková)', email: 'sekretariat@mostpribratislave.sk', href: '/urad/podatelna/' },
  { title: 'Matrika a evidencia obyvateľov', people: 'Katarína Dimoulatos', email: 'matrika@mostpribratislave.sk', href: '/urad/matrika/' },
  { title: 'Dane a poplatky', people: 'Mariana Kochrdová', email: 'dane@mostpribratislave.sk', href: '/urad/dane-a-poplatky/' },
  { title: 'Odpady a životné prostredie', people: 'Mgr. Veronika Veselá', email: 'odpady@mostpribratislave.sk', phone: '02 / 4595 1215, kl. 3', href: '/odpady/referat-odpadov/' },
  { title: 'Stavebný úrad', people: 'RNDr. Róbert Mikóci', email: 'stavebnyurad@mostpribratislave.sk', phone: '+421 910 225 893', href: '/urad/stavebny-urad/' },
  { title: 'Stavebný úrad', people: 'Ing. Mária Zárubová', email: 'zarubova@mostpribratislave.sk', phone: '+421 903 232 911', href: '/urad/stavebny-urad/' },
  { title: 'Územné plánovanie', people: 'Ing. Lýdia Tučániová', email: 'uzemneplanovanie@mostpribratislave.sk', href: '/urad/uzemny-rozvoj/' },
  { title: 'Ekonomický referát', people: 'Jana Cingelová', email: 'ekonom@mostpribratislave.sk', href: '/urad/socialne-veci/' },
  { title: 'Sociálne veci', people: 'Mgr. Iveta Sarangová', email: 'socialne@mostpribratislave.sk', href: '/urad/socialne-veci/' },
  { title: 'Priestupky', people: 'JUDr. Dominika Bela', email: 'priestupky@mostpribratislave.sk', href: '/urad/priestupky/' },
  { title: 'Personalistika a mzdy', people: 'Iveta Kvasnicová', email: 'kvasnicova@mostpribratislave.sk', href: '/urad/personalny-a-mzdovy/' },
  { title: 'Verejné obstarávanie', people: '', email: 'obstaravanie@mostpribratislave.sk', href: '/urad/projekty-a-obstaravanie/' },
  { title: 'Projekty', people: '', email: 'projekty@mostpribratislave.sk', href: '/urad/projekty-a-obstaravanie/' },
  { title: 'Obecný spravodaj', people: 'Príspevky do obecných novín', email: 'spravodaj@mostpribratislave.sk', href: '/aktuality/obecny-spravodaj/' },
  { title: 'Obecná polícia', people: 'Spoločná obecná polícia (Malinovo)', email: 'obecna.policia@malinovo.sk', phone: '0914 557 722', href: '/urad/obecna-policia/' },
];

// Špeciálne stránky, ktoré nie sú z importu – zobrazia sa v navigácii sekcie
export const extraLinks: Record<string, { title: string; href: string; group: string; order: number }[]> = {
  obec: [{ title: 'Fotogaléria', href: '/obec/fotogaleria/', group: 'O obci', order: 3 }],
  aktuality: [
    { title: 'Všetky aktuality', href: '/aktuality/', group: 'Z obce', order: 1 },
    { title: 'Na čo si dať pozor', href: '/aktuality/upozornenia/', group: 'Z obce', order: 2 },
    { title: 'Kalendár podujatí', href: '/aktuality/podujatia/', group: 'Podujatia', order: 19 },
  ],
  'uradna-tabula': [{ title: 'Voľby a referendá – prehľad', href: '/volby/', group: 'Voľby a referendá', order: 19 }],
  kontakt: [
    { title: 'Kontakty a úradné hodiny', href: '/kontakt/', group: 'Kontakty', order: 0 },
    { title: 'Nahlásiť problém', href: '/nahlasit-problem/', group: 'Kontakty', order: 2 },
    { title: 'Odpovede na podnety občanov', href: '/kontakt/podnety/', group: 'Kontakty', order: 3 },
  ],
};
