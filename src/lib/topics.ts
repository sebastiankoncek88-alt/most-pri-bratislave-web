// Téma podnetu podľa slov v názve -> ikona a farba obrázka na karte
const TOPICS: { re: RegExp; label: string; icon: string; tone: string }[] = [
  { re: /odpad|smeti|kontajner|zber|šrot|srot|nádob|nadob|bioodpad|komunál/i, label: 'Odpady', icon: 'recycle', tone: 'waste' },
  { re: /osvetlen|lamp|svetl/i, label: 'Osvetlenie', icon: 'lightbulb', tone: 'warn' },
  { re: /kanaliz|vod|žump|zump|dážď|dazd|kaluž/i, label: 'Voda a kanalizácia', icon: 'droplets', tone: 'traffic' },
  { re: /dron/i, label: 'Drony', icon: 'plane', tone: 'civic' },
  { re: /cest|ulic|jednosmer|parkov|chodník|chodnik|výtl|vytl|burin|prechod|dopra|autobus|zastávk/i, label: 'Cesty a doprava', icon: 'construction', tone: 'traffic' },
  { re: /strom|zeleň|zelen|kosen|tráv|trav|park|konár|konar/i, label: 'Zeleň', icon: 'trees', tone: 'waste' },
  { re: /hluk|rušen|rusen|hudb|noc/i, label: 'Hluk a poriadok', icon: 'volume-2', tone: 'civic' },
  { re: /pes|psy|psov|zviera|mačk|mack/i, label: 'Zvieratá', icon: 'dog', tone: 'culture' },
  { re: /škol|skol|škôlk|skolk|deti|ihrisk/i, label: 'Deti a škola', icon: 'school', tone: 'culture' },
];
export function podnetTopic(title: string) {
  return TOPICS.find((t) => t.re.test(title)) ?? { label: 'Podnet', icon: 'message-square', tone: 'default' };
}
