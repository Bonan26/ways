# ALPHA WOLVES - CONTRAT D'INTERFACE

## Document de Référence pour les 3 Équipes

Ce document définit les interfaces entre Math-SDK, Web-SDK et Assets.
**TOUTE MODIFICATION doit être validée par les 3 équipes.**

---

## 1. DIRECTION ARTISTIQUE

### Style: "Grungy Cartoon"

**Références visuelles:**
- Ren & Stimpy
- Courage le Chien Froussard
- Cartoons underground 90s/2000s
- Esthétique Streetwear/NFT moderne

**Caractéristiques du trait:**
| Élément | Description |
|---------|-------------|
| Line Art | Trait noir, net mais organique, variations d'épaisseur |
| Colorimétrie | Aplats de couleurs vibrantes sur fonds neutres/désaturés |
| Ombres | Quasi inexistantes - look 2D traditionnel |
| Expressions | Grotesques et décalées (yeux injectés de sang, grimaces) |
| Contraste | Mélange "mignon" (couleurs) vs "agressif" (expressions) |

**Palette de couleurs suggérée:**
```
Rose chair loup:  #E8A0B0
Fond désaturé:    #2D2A3A
Noir trait:       #1A1A1A
Accent néon:      #00FF88 (pour les wins)
Rouge sang:       #CC2233 (yeux, effets)
```

---

## 2. SYMBOLES - DÉFINITIONS EXACTES

### 2.1 Symboles Premium (4) - Personnages Loups

| ID | Nom Affichage | Description Visuelle | Paytable 6x/5x/4x/3x |
|----|---------------|---------------------|----------------------|
| `BOSS_WOLF` | Boss Wolf | Loup en costume 3 pièces, cigare, lunettes noires, expression menaçante, yeux injectés de sang | 100 / 50 / 20 / 5 |
| `HUSTLER` | Hustler | Loup streetwear, casquette à l'envers, chaîne en or, sourire rusé/malsain | 50 / 25 / 10 / 3 |
| `TECH_BRO` | Tech Bro | Loup avec lunettes cassées, t-shirt taché, expression maniaque/obsédée | 30 / 15 / 6 / 2 |
| `DIAMOND_HANDS` | Diamond Hands | Loup aux pattes couvertes de bagues, expression déterminée/folle | 20 / 10 / 4 / 1.5 |

### 2.2 Symboles Low (4) - Items de Meute

| ID | Nom Affichage | Description Visuelle | Paytable 6x/5x/4x/3x |
|----|---------------|---------------------|----------------------|
| `BONE` | Os | Os rongé, traces de morsures, style cartoon dégoûtant | 12 / 6 / 2 / 0.8 |
| `MEAT` | Viande | Morceau de viande crue dégoulinante, style exagéré | 10 / 5 / 1.5 / 0.6 |
| `CLAW` | Griffe | Griffe acérée avec traces de sang, look menaçant | 8 / 4 / 1.2 / 0.4 |
| `FANG` | Croc | Croc de loup isolé, jauni, style grotesque | 6 / 3 / 1 / 0.3 |

### 2.3 Symboles Spéciaux (4)

| ID | Nom Affichage | Type | Description Visuelle |
|----|---------------|------|---------------------|
| `ALPHA_WOLF` | Alpha Wolf | Wild + Split | Loup alpha massif, yeux brillants rouges, aura de pouvoir, expression dominante |
| `HOWLING_WILD` | Howling Wild | Wild + Multiplier (x2-x10) | Loup hurlant à la lune, ondes sonores visibles, affichage multiplicateur |
| `MOON_SCATTER` | Moon | Scatter | Lune sanglante/rouge avec silhouette de loup hurlant |
| `TERRITORY` | Territory | Expand | Drapeau déchiré avec empreinte de patte, style graffiti |

---

## 3. ÉTATS DES SYMBOLES (pour Assets & Web)

Chaque symbole doit avoir ces états/animations:

| État | Nom Fichier Suffix | Description | Durée |
|------|-------------------|-------------|-------|
| `static` | `_static` | Image fixe, état par défaut | - |
| `spin` | `_spin` | Animation pendant rotation reels | loop |
| `land` | `_land` | Animation à l'atterrissage | 0.5s |
| `win` | `_win` | Animation de victoire | 1.5s |
| `postWinStatic` | `_post_win` | État après win, avant reset | - |
| `explosion` | `_explosion` | Disparition (cascade) | 0.3s |

### États Spéciaux (symboles spéciaux uniquement)

| État | Applicable à | Description |
|------|--------------|-------------|
| `split` | ALPHA_WOLF | Animation de split vers la gauche |
| `howl` | HOWLING_WILD | Animation de hurlement + chaîne |
| `territory_glow` | TERRITORY | Glow avant collection |
| `cascade_remove` | Tous | Animation de "chasse" (loup attrape symbole) |

---

## 4. BOOK EVENTS (Math → Web)

### 4.1 Événements Standard

```typescript
// Révélation du board après spin
type BookEventReveal = {
  index: number;
  type: 'reveal';
  board: RawSymbol[][];           // Grille de symboles
  paddingPositions: number[];
  anticipation: number[];         // Reels avec anticipation
  gameType: 'basegame' | 'freegame' | 'alpha_domination';
  gridSize: { reels: number; rows: number };
};

// Information sur un win
type BookEventWinInfo = {
  index: number;
  type: 'winInfo';
  totalWin: number;
  wins: Array<{
    symbol: SymbolName;
    count: number;
    positions: Position[];
    payout: number;
  }>;
  cascadeMultiplier: number;
};

// Mise à jour du total win
type BookEventSetTotalWin = {
  index: number;
  type: 'setTotalWin';
  amount: number;
};

// Trigger des free spins
type BookEventFreeSpinTrigger = {
  index: number;
  type: 'freeSpinTrigger';
  totalFs: number;
  positions: Position[];          // Positions des scatters
  bonusType: 'pack_hunt' | 'enhanced' | 'alpha_domination';
  startingGrid: { reels: number; rows: number };
  startingMultiplier: number;     // x1 pour pack_hunt, x5 pour alpha_dom
};

// Update compteur FS
type BookEventUpdateFreeSpin = {
  index: number;
  type: 'updateFreeSpin';
  current: number;
  total: number;
};

// Fin des free spins
type BookEventFreeSpinEnd = {
  index: number;
  type: 'freeSpinEnd';
  amount: number;
  winLevel: number;               // 1-10
};

// Affichage win
type BookEventSetWin = {
  index: number;
  type: 'setWin';
  amount: number;
  winLevel: number;
};

// Win final du round
type BookEventFinalWin = {
  index: number;
  type: 'finalWin';
  amount: number;
};
```

### 4.2 Événements Alpha Wolves (Custom)

```typescript
// Pack Split - Alpha Wolf duplique symboles à gauche
type BookEventPackSplit = {
  index: number;
  type: 'packSplit';
  alphaPosition: Position;        // Position de l'Alpha Wolf
  affectedPositions: Position[];  // Positions dupliquées
  splitMultipliers: number[];     // Multiplicateurs si split multiple
  newBoard: RawSymbol[][];        // Board après split
};

// Territory Expand - Agrandissement de la grille
type BookEventTerritoryExpand = {
  index: number;
  type: 'territoryExpand';
  oldGrid: { reels: number; rows: number };
  newGrid: { reels: number; rows: number };
  territoryCount: number;
  newBoard: RawSymbol[][];
};

// Howl Chain - Wilds adjacents combinent multiplicateurs
type BookEventHowlChain = {
  index: number;
  type: 'howlChain';
  chains: Array<{
    positions: Position[];
    multipliers: number[];
    combinedMultiplier: number;
    combinationType: 'add' | 'multiply';  // 2 wilds = add, 3+ = multiply
  }>;
  totalMultiplier: number;
};

// Hunt Cascade - Tumble/Cascade
type BookEventHuntCascade = {
  index: number;
  type: 'huntCascade';
  cascadeNumber: number;          // 1, 2, 3...
  removedPositions: Position[];
  currentMultiplier: number;
  multiplierCap: number;
  newBoard: RawSymbol[][];
};

// Mode Switch - Changement de volatilité
type BookEventModeSwitch = {
  index: number;
  type: 'modeSwitch';
  fromMode: 'lone_wolf' | 'pack' | 'alpha';
  toMode: 'lone_wolf' | 'pack' | 'alpha';
};

// Update multiplicateur cascade
type BookEventUpdateCascadeMultiplier = {
  index: number;
  type: 'updateCascadeMultiplier';
  multiplier: number;
  cap: number;
};
```

---

## 5. TYPES PARTAGÉS

```typescript
// Nom des symboles
type SymbolName =
  | 'BOSS_WOLF' | 'HUSTLER' | 'TECH_BRO' | 'DIAMOND_HANDS'
  | 'BONE' | 'MEAT' | 'CLAW' | 'FANG'
  | 'ALPHA_WOLF' | 'HOWLING_WILD' | 'MOON_SCATTER' | 'TERRITORY';

// Symbole brut (du backend)
type RawSymbol = {
  name: SymbolName;
  multiplier?: number;      // Pour HOWLING_WILD (2-10)
  wild?: boolean;
  scatter?: boolean;
  split?: boolean;
  territory?: boolean;
};

// Position sur la grille
type Position = {
  reel: number;             // 0-7
  row: number;              // 0-7
};

// Taille de grille
type GridSize = {
  reels: number;            // 6-8
  rows: number;             // 5-8
};

// Type de jeu
type GameType = 'basegame' | 'freegame' | 'alpha_domination';

// Mode de volatilité
type VolatilityMode = 'lone_wolf' | 'pack' | 'alpha';

// Mode de pari
type BetMode =
  | 'lone_wolf' | 'pack' | 'alpha'
  | 'bonus_pack_hunt' | 'bonus_enhanced' | 'bonus_alpha_domination';
```

---

## 6. NOMENCLATURE DES ASSETS

### 6.1 Spine Animations

```
static/assets/spines/
├── symbols_premium/
│   ├── boss_wolf.json + boss_wolf.atlas
│   ├── hustler.json + hustler.atlas
│   ├── tech_bro.json + tech_bro.atlas
│   └── diamond_hands.json + diamond_hands.atlas
├── symbols_low/
│   ├── bone.json + bone.atlas
│   ├── meat.json + meat.atlas
│   ├── claw.json + claw.atlas
│   └── fang.json + fang.atlas
├── symbols_special/
│   ├── alpha_wolf.json + alpha_wolf.atlas
│   ├── howling_wild.json + howling_wild.atlas
│   ├── moon_scatter.json + moon_scatter.atlas
│   └── territory.json + territory.atlas
├── effects/
│   ├── pack_split.json
│   ├── territory_expand.json
│   ├── howl_chain.json
│   ├── cascade_hunt.json
│   └── explosion.json
├── backgrounds/
│   ├── bg_basegame.json
│   ├── bg_freegame.json
│   └── bg_alpha_domination.json
├── ui/
│   ├── cascade_multiplier.json
│   ├── territory_meter.json
│   └── ways_counter.json
├── bigwin/
│   ├── win_big.json
│   ├── win_super.json
│   ├── win_mega.json
│   ├── win_epic.json
│   └── win_max.json
├── transitions/
│   ├── transition_to_bonus.json
│   └── transition_wolf_howl.json
└── loader/
    └── loader.json
```

### 6.2 Sprites Statiques

```
static/assets/sprites/
├── symbols_static/
│   ├── boss_wolf.webp
│   ├── hustler.webp
│   ├── tech_bro.webp
│   ├── diamond_hands.webp
│   ├── bone.webp
│   ├── meat.webp
│   ├── claw.webp
│   ├── fang.webp
│   ├── alpha_wolf.webp
│   ├── howling_wild.webp
│   ├── moon_scatter.webp
│   └── territory.webp
├── ui/
│   ├── btn_spin.webp
│   ├── btn_turbo.webp
│   ├── btn_autoplay.webp
│   ├── mode_lone_wolf.webp
│   ├── mode_pack.webp
│   ├── mode_alpha.webp
│   ├── buy_pack_hunt.webp
│   ├── buy_enhanced.webp
│   └── buy_alpha_domination.webp
├── frames/
│   ├── reels_frame_6x5.webp
│   ├── reels_frame_6x6.webp
│   ├── reels_frame_7x6.webp
│   ├── reels_frame_7x7.webp
│   └── reels_frame_8x8.webp
└── particles/
    ├── blood_drop.webp
    ├── fur_particle.webp
    └── glow_particle.webp
```

### 6.3 Audio

```
static/assets/audio/
├── sounds.json           # Manifest audio sprite
├── sounds.mp3
├── sounds.ogg
├── sounds.m4a
└── sounds.ac3
```

**Sons requis dans sounds.json:**

| Catégorie | Noms des sons |
|-----------|---------------|
| **BGM** | `bgm_main`, `bgm_freegame`, `bgm_alpha_domination`, `bgm_win_big`, `bgm_win_super`, `bgm_win_mega`, `bgm_win_epic`, `bgm_win_max` |
| **Reels** | `sfx_reel_stop_1` à `sfx_reel_stop_6`, `sfx_anticipation`, `sfx_spin_start` |
| **Symbols Land** | `sfx_premium_land`, `sfx_low_land`, `sfx_wild_land`, `sfx_scatter_land_1` à `sfx_scatter_land_5` |
| **Mécaniques** | `sfx_pack_split`, `sfx_territory_expand`, `sfx_howl_chain`, `sfx_cascade_1` à `sfx_cascade_5`, `sfx_multiplier_up` |
| **Wins** | `sfx_win_small`, `sfx_win_medium`, `sfx_win_big`, `sfx_win_super`, `sfx_win_mega`, `sfx_win_epic`, `sfx_win_max`, `sfx_coin_loop` |
| **UI** | `sfx_btn_click`, `sfx_mode_switch`, `sfx_bonus_buy` |
| **Ambiance** | `sfx_wolf_growl`, `sfx_wolf_howl`, `sfx_wolf_snarl` |

---

## 7. GRILLES ET WAYS

| Configuration | Reels | Rows | Ways | Trigger |
|---------------|-------|------|------|---------|
| Base | 6 | 5 | 7,776 | Défaut |
| Expand 1 | 6 | 6 | 46,656 | 3 Territory |
| Expand 2 | 7 | 6 | 117,649 | 5 Territory |
| Expand 3 | 7 | 7 | 823,543 | 7 Territory |
| Max (Alpha Dom) | 8 | 8 | 16,777,216 | 10 Territory / 5 Scatters |

---

## 8. WIN LEVELS

| Level | Alias | Seuil (x bet) | Animation | Durée |
|-------|-------|---------------|-----------|-------|
| 1 | zero | 0 | Aucune | 0s |
| 2 | small | 0-2x | Basique | 0.5s |
| 3 | medium | 2-5x | Normale | 1s |
| 4 | nice | 5-10x | Bonne | 1.5s |
| 5 | substantial | 10-25x | Grande | 2s |
| 6 | big | 25-100x | Big Win | 4s |
| 7 | super | 100-500x | Super Win | 6s |
| 8 | mega | 500-2000x | Mega Win | 8s |
| 9 | epic | 2000-10000x | Epic Win | 12s |
| 10 | max | 10000-50000x | MAX WIN | 20s |

---

## 9. CHECKLIST PAR ÉQUIPE

### MATH (Dev 1)
- [ ] Implémenter les 12 symboles avec paytables
- [ ] Créer les 12 fichiers CSV de reels
- [ ] Implémenter Hunt Cascade
- [ ] Implémenter Pack Split
- [ ] Implémenter Territory Expand
- [ ] Implémenter Howl Chain
- [ ] Émettre les BookEvents selon ce contrat
- [ ] Valider RTP pour les 3 modes

### WEB (Dev 2)
- [ ] Implémenter les handlers pour tous les BookEvents
- [ ] Créer les composants pour les 12 symboles
- [ ] Gérer la grille dynamique (6x5 → 8x8)
- [ ] Animations cascade/tumble
- [ ] UI multiplicateur, territory meter, ways counter
- [ ] Intégration audio selon nomenclature

### ASSETS (Dev 3)
- [ ] Créer les 12 symboles (style Grungy Cartoon)
- [ ] Tous les états par symbole (static, spin, land, win, explosion)
- [ ] Animations spéciales (split, howl, territory_glow)
- [ ] Backgrounds (3 modes)
- [ ] Effects (pack_split, cascade, howl_chain, etc.)
- [ ] UI elements
- [ ] Audio complet

---

## 10. CONTACT & VALIDATION

Toute modification de ce contrat nécessite:
1. Discussion entre les 3 équipes
2. Mise à jour de ce document
3. Notification à tous

**Version:** 1.0
**Date:** Janvier 2026
