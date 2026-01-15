# Prompts Initiaux pour les 3 Claude Code

Copiez-collez le prompt correspondant dans chaque instance de Claude Code.

---

## PROMPT 1: MATH-SDK (Python)

```
Tu es le développeur du MATH-SDK pour le jeu de slot "Alpha Wolves".

## Contexte
Alpha Wolves est un slot 6x5 expandable jusqu'à 8x8 avec:
- 3 modes de volatilité (Lone Wolf 96.8%, Pack 96.5%, Alpha 96.2%)
- Max win 50,000x
- Mécaniques: Hunt Cascade (tumble), Pack Split, Territory Expand, Howl Chain

## Fichiers de référence OBLIGATOIRES
Avant de coder, LIS ces fichiers:
1. `INTERFACE_CONTRACT.md` - Contrat d'interface (symboles, events, types)
2. `ALPHA_WOLVES_IMPLEMENTATION_PLAN.md` - Plan détaillé section PARTIE 1
3. `math-sdk/` - Structure existante de Ways SDK à reproduire

## Ta mission
Créer le dossier `alpha-wolves/math-sdk/` avec:

### Fichiers Python (8)
1. `run.py` - Orchestrateur principal
2. `game_config.py` - Configuration singleton (symboles, paytables, grilles, bet modes)
3. `gamestate.py` - Logique de jeu (run_spin, run_freespin avec cascade loop)
4. `game_executables.py` - Calculs ways, cascade, pack split
5. `game_override.py` - Fonctions symboles spéciaux
6. `game_calculations.py` - Math custom (howl chain, grid expansion)
7. `game_events.py` - Événements custom (PackSplit, TerritoryExpand, HowlChain, etc.)
8. `game_optimization.py` - Setup optimisation RTP

### Fichiers Reels CSV (12)
Dans `reels/`: BR_LONE_WOLF, BR_PACK, BR_ALPHA, FR_PACK_HUNT, FR_ENHANCED, FR_ALPHA_DOM, FR_6x6, FR_7x6, FR_7x7, FR_8x8, WINCAP_BASE, WINCAP_BONUS

## Contraintes CRITIQUES
- Les 12 symboles DOIVENT être: BOSS_WOLF, HUSTLER, TECH_BRO, DIAMOND_HANDS, BONE, MEAT, CLAW, FANG, ALPHA_WOLF, HOWLING_WILD, MOON_SCATTER, TERRITORY
- Les paytables DOIVENT correspondre à INTERFACE_CONTRACT.md section 2
- Les BookEvents émis DOIVENT correspondre à INTERFACE_CONTRACT.md section 4
- Base-toi sur la structure de `math-sdk/` existant pour le style de code

## Ordre d'implémentation
1. game_config.py (tout le reste en dépend)
2. game_events.py (définitions événements)
3. game_calculations.py
4. game_executables.py
5. game_override.py
6. gamestate.py
7. game_optimization.py
8. run.py
9. Fichiers CSV reels

Commence par lire les fichiers de référence, puis implémente game_config.py.
```

---

## PROMPT 2: WEB-SDK (Svelte/TypeScript)

```
Tu es le développeur du WEB-SDK pour le jeu de slot "Alpha Wolves".

## Contexte
Alpha Wolves est un slot 6x5 expandable jusqu'à 8x8 avec:
- Grille dynamique (7,776 → 262,144 ways)
- Mécaniques visuelles: Hunt Cascade (tumble), Pack Split, Territory Expand, Howl Chain
- Style artistique: "Grungy Cartoon" (Ren & Stimpy)

## Fichiers de référence OBLIGATOIRES
Avant de coder, LIS ces fichiers:
1. `INTERFACE_CONTRACT.md` - Contrat d'interface (types, events, nomenclature assets)
2. `ALPHA_WOLVES_IMPLEMENTATION_PLAN.md` - Plan détaillé section PARTIE 2
3. `web-sdk/` - Structure existante de Ways SDK à reproduire

## Ta mission
Créer le dossier `alpha-wolves/web-sdk/` avec:

### Configuration Game (`src/game/` - 14 fichiers)
- `config.ts` - Configuration jeu
- `types.ts` - Types (copie depuis INTERFACE_CONTRACT.md section 5)
- `typesBookEvent.ts` - Types événements (copie depuis INTERFACE_CONTRACT.md section 4)
- `typesEmitterEvent.ts` - Types emitter
- `constants.ts` - Constantes, SYMBOL_INFO_MAP pour 12 symboles
- `stateGame.svelte.ts` - État réactif avec grille dynamique
- `bookEventHandlerMap.ts` - Handlers pour TOUS les événements
- `actor.ts`, `stateApp.ts`, `stateLayout.ts`, `stateXstate.ts`, `eventEmitter.ts`, `utils.ts`
- `winLevelMap.ts` - Win levels 1-10 (jusqu'à 50,000x)
- `sound.ts`, `assets.ts`

### Composants Svelte (`src/components/` - 47 fichiers)
Voir IMPLEMENTATION_PLAN section 2.2 pour la liste complète.
Priorité:
1. Composants Core (Game, Board, Symbol, etc.)
2. Composants Alpha Wolves (PackSplitAnimation, HowlChainAnimation, etc.)
3. Composants Free Spin
4. Composants Win

## Contraintes CRITIQUES
- Les types DOIVENT correspondre EXACTEMENT à INTERFACE_CONTRACT.md
- Les noms d'assets dans constants.ts DOIVENT correspondre à la nomenclature section 6
- Utilise des PLACEHOLDERS pour les assets (l'équipe Assets les fournira)
- La grille DOIT être dynamique (6x5 → 8x8)
- Base-toi sur `web-sdk/` existant pour le style de code Svelte

## Ordre d'implémentation
1. `src/game/types.ts` et `typesBookEvent.ts` (copie du contrat)
2. `src/game/config.ts` et `constants.ts`
3. `src/game/stateGame.svelte.ts` (grille dynamique)
4. `src/game/bookEventHandlerMap.ts` (tous les handlers)
5. Composants de base (Game, Board, Symbol)
6. Composants features (PackSplit, HowlChain, etc.)

Commence par lire les fichiers de référence, puis crée les types.
```

---

## PROMPT 3: ASSETS (Art/Audio)

```
Tu es le développeur des ASSETS STATIQUES pour le jeu de slot "Alpha Wolves".

## Contexte
Alpha Wolves est un slot avec un style artistique "Grungy Cartoon":
- Inspiration: Ren & Stimpy, Courage le Chien Froussard
- Trait noir organique avec variations d'épaisseur
- Aplats de couleurs vibrantes sur fonds désaturés
- Expressions grotesques/décalées
- Ombres quasi inexistantes (look 2D traditionnel)

## Fichiers de référence OBLIGATOIRES
Avant de créer, LIS ces fichiers:
1. `INTERFACE_CONTRACT.md` - Direction artistique section 1, Symboles section 2, Nomenclature section 6
2. `ALPHA_WOLVES_IMPLEMENTATION_PLAN.md` - Plan détaillé section PARTIE 3
3. `web-sdk/static/assets/` - Structure existante de Ways SDK

## Ta mission
Créer la structure `alpha-wolves/web-sdk/static/assets/` avec:

### Spine Animations (`spines/` - 22 dossiers)
Structure EXACTE depuis INTERFACE_CONTRACT.md section 6.1

### Sprites Statiques (`sprites/`)
Structure EXACTE depuis INTERFACE_CONTRACT.md section 6.2

### Fonts (`fonts/` - 5 dossiers)
goldFont, goldBlur, silverFont, alphaFont, cryptoFont

### Audio (`audio/`)
sounds.json + fichiers audio sprite (mp3, ogg, m4a, ac3)
Liste des sons dans INTERFACE_CONTRACT.md section 6.3

## Les 12 Symboles à créer

### Premium (Loups personnages)
| ID | Description |
|----|-------------|
| BOSS_WOLF | Loup costume 3 pièces, cigare, lunettes, yeux injectés sang |
| HUSTLER | Loup streetwear, casquette, chaîne or, sourire malsain |
| TECH_BRO | Loup lunettes cassées, t-shirt taché, expression maniaque |
| DIAMOND_HANDS | Loup pattes avec bagues, expression folle/déterminée |

### Low (Items de meute)
| ID | Description |
|----|-------------|
| BONE | Os rongé, traces morsures, style cartoon dégoûtant |
| MEAT | Viande crue dégoulinante, exagéré |
| CLAW | Griffe acérée avec traces sang |
| FANG | Croc jauni, style grotesque |

### Spéciaux
| ID | Description |
|----|-------------|
| ALPHA_WOLF | Loup alpha massif, yeux rouges brillants, aura pouvoir |
| HOWLING_WILD | Loup hurlant, ondes sonores visibles |
| MOON_SCATTER | Lune sanglante avec silhouette loup |
| TERRITORY | Drapeau déchiré avec empreinte patte |

## États par symbole
Chaque symbole doit avoir: static, spin, land, win, postWinStatic, explosion
Les spéciaux ont en plus: split (ALPHA_WOLF), howl (HOWLING_WILD), territory_glow (TERRITORY)

## Contraintes CRITIQUES
- Les NOMS de fichiers DOIVENT correspondre EXACTEMENT à INTERFACE_CONTRACT.md section 6
- La STRUCTURE des dossiers DOIT être EXACTE
- Palette suggérée: Rose chair #E8A0B0, Fond #2D2A3A, Noir #1A1A1A, Accent #00FF88, Rouge sang #CC2233

## Ordre de création
1. Créer la structure de dossiers complète
2. Sprites statiques des 12 symboles (pour que Web puisse tester)
3. Animations Spine des symboles
4. Effets (pack_split, howl_chain, cascade, etc.)
5. Backgrounds (3 modes)
6. UI elements
7. Audio

Commence par lire INTERFACE_CONTRACT.md section 1 (Direction Artistique), puis crée la structure de dossiers.
```

---

## Notes d'utilisation

1. Chaque Claude Code travaille dans le même repo mais dans des dossiers différents
2. Chacun doit LIRE le contrat avant de coder
3. En cas de conflit/question → modifier INTERFACE_CONTRACT.md et prévenir les autres
4. L'équipe Web peut utiliser des placeholders en attendant les assets réels
