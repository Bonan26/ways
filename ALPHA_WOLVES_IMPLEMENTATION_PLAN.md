# ALPHA WOLVES - Plan d'Implementation Complet

## Vue d'Ensemble

Recréation complète des math-sdk et web-sdk pour le jeu **Alpha Wolves** basé sur l'architecture Ways SDK.

| Paramètre | Valeur |
|-----------|--------|
| RTP | 96.5% (3 modes: 96.8% / 96.5% / 96.2%) |
| Max Win | 50,000x |
| Grille | 6x5 → 8x8 dynamique |
| Ways | 7,776 → 262,144 |
| Volatilité | Extrême (choix joueur) |

---

## PARTIE 1: MATH-SDK (20 fichiers)

### 1.1 Fichiers Python Principaux (8 fichiers)

#### `alpha-wolves/math-sdk/run.py`
```
- Orchestrateur principal
- 6 modes cibles: lone_wolf, pack, alpha, bonus_pack_hunt, bonus_enhanced, bonus_alpha_domination
- Config: 10 threads, 20 rust_threads, batch 50000
- Simulations: 1M base, 1M bonus, 500k alpha_domination
```

#### `alpha-wolves/math-sdk/game_config.py`
```
- Singleton GameConfig
- game_id: "alpha_wolves"
- wincap: 50000
- Grille dynamique: 6x5 → 8x8
- 12 symboles: BOSS_WOLF, HUSTLER, TECH_BRO, DIAMOND_HANDS, BONE, MEAT, CLAW, FANG, ALPHA_WOLF, HOWLING_WILD, MOON_SCATTER, TERRITORY
- Paytable complet (3-6 symboles)
- 3 modes de volatilité avec RTP distincts
- Seuils d'expansion: 3→6x6, 5→7x6, 7→7x7, 10→8x8
- Caps multiplicateur: base=50, freegame=100, alpha_domination=500
- 6 BetModes
```

#### `alpha-wolves/math-sdk/gamestate.py`
```
- run_spin(): Loop cascade (Hunt Cascade)
  - draw_board()
  - while has_winning_combinations():
    - evaluate_ways_board()
    - apply_hunt_cascade()
    - increment_cascade_multiplier()
    - process_pack_split()
    - draw_cascade_symbols()
  - check_territory_expansion()
  - process_howl_chains()
  - check_fs_condition()
- run_freespin(): Logique bonus avec multiplicateur persistant
```

#### `alpha-wolves/math-sdk/game_executables.py`
```
- evaluate_ways_board(): Calcul ways dynamique
- apply_hunt_cascade(): Suppression symboles gagnants
- process_pack_split(): Alpha Wolf split vers la gauche
- check_territory_expansion(): Expansion grille
- process_howl_chains(): Combinaison multiplicateurs wilds adjacents
```

#### `alpha-wolves/math-sdk/game_override.py`
```
- reset_book(): Reset cascade, territory, grid
- assign_special_sym_function():
  - ALPHA_WOLF → assign_split_property
  - HOWLING_WILD → assign_howl_multiplier (x2-x10)
  - TERRITORY → assign_territory_property
  - MOON_SCATTER → assign_scatter_property
- increment_cascade_multiplier(): +1 par cascade (cap variable)
```

#### `alpha-wolves/math-sdk/game_calculations.py`
```
- calculate_ways_count(grid_size)
- calculate_howl_chain_multiplier(wilds): 2=add, 3+=multiply
- calculate_split_positions(alpha_pos)
- calculate_grid_expansion_ways(current, target)
```

#### `alpha-wolves/math-sdk/game_events.py`
```
Événements custom:
- PackSplitEvent
- TerritoryExpandEvent
- HowlChainEvent
- HuntCascadeEvent
- ModeSwitchEvent
- AlphaDominationTriggerEvent
```

#### `alpha-wolves/math-sdk/game_optimization.py`
```
OptimizationSetup pour 6 modes:
- lone_wolf: RTP 96.8%, HR 3.5
- pack: RTP 96.5%, HR 3.0
- alpha: RTP 96.2%, HR 2.5
- bonus_pack_hunt: 75x cost
- bonus_enhanced: 150x cost
- bonus_alpha_domination: 500x cost
```

### 1.2 Fichiers Reels CSV (12 fichiers)

| Fichier | Description | Colonnes |
|---------|-------------|----------|
| `reels/BR_LONE_WOLF.csv` | Base game Lone Wolf | 6 |
| `reels/BR_PACK.csv` | Base game Pack | 6 |
| `reels/BR_ALPHA.csv` | Base game Alpha | 6 |
| `reels/FR_PACK_HUNT.csv` | Free game Pack Hunt | 6 |
| `reels/FR_ENHANCED.csv` | Free game Enhanced | 7 |
| `reels/FR_ALPHA_DOM.csv` | Alpha Domination | 8 |
| `reels/FR_6x6.csv` | Expansion 6x6 | 6 |
| `reels/FR_7x6.csv` | Expansion 7x6 | 7 |
| `reels/FR_7x7.csv` | Expansion 7x7 | 7 |
| `reels/FR_8x8.csv` | Expansion 8x8 | 8 |
| `reels/WINCAP_BASE.csv` | Wincap base | 6 |
| `reels/WINCAP_BONUS.csv` | Wincap bonus | 8 |

---

## PARTIE 2: WEB-SDK (100+ fichiers)

### 2.1 Configuration Game (`src/game/` - 14 fichiers)

| Fichier | Contenu Clé |
|---------|-------------|
| `config.ts` | 12 symboles (4 loups premium, 4 items loup, 4 spéciaux), 6 betModes, grille dynamique |
| `types.ts` | SymbolName, GridSize, CascadeData, TerritoryData, HowlChainData |
| `typesBookEvent.ts` | 6 nouveaux events: packSplit, territoryExpand, howlChain, huntCascade, modeSwitch, updateCascadeMultiplier |
| `typesEmitterEvent.ts` | Emitter events pour nouveaux composants |
| `constants.ts` | getSymbolSize(), SYMBOL_INFO_MAP (12 symboles, états étendus) |
| `stateGame.svelte.ts` | Board dynamique, cascadeData, territoryData, howlChainData, volatilityMode |
| `bookEventHandlerMap.ts` | 6 nouveaux handlers + reveal avec gridSize |
| `actor.ts` | Game actor (similaire Ways) |
| `stateApp.ts` | App state (identique Ways) |
| `stateLayout.ts` | Layout state (identique Ways) |
| `stateXstate.ts` | XState (identique Ways) |
| `eventEmitter.ts` | Event emitter (identique Ways) |
| `utils.ts` | Utilitaires étendus pour grille dynamique |
| `winLevelMap.ts` | Win levels étendus pour 50,000x |
| `sound.ts` | ~60 sons (nouveaux: pack_split, howl_chain, cascade, etc.) |
| `assets.ts` | Assets étendus (22 dossiers Spine, 15 dossiers Sprites) |

### 2.2 Composants Svelte (`src/components/` - 47 fichiers)

#### Composants Core (15 fichiers - similaires Ways)
```
Game.svelte              - Container principal + nouveaux éléments
Board.svelte             - Grille dynamique + cascade
BoardBase.svelte         - Rendu symboles dynamique
BoardContainer.svelte    - Positionnement dynamique
BoardFrame.svelte        - Frame + glow Alpha Domination
BoardMask.svelte         - Masque dynamique
ReelSymbol.svelte        - États étendus (split, howl, territory_glow, cascade_remove)
Symbol.svelte            - 12 symboles
SymbolWrap.svelte        - Wrapper dynamique
SymbolSpine.svelte       - Animations Spine
SymbolSpineMain.svelte   - Setup Spine
SymbolSprite.svelte      - Sprites statiques
Background.svelte        - 4 backgrounds (base, bonus, alpha_dom, transition)
LoadingScreen.svelte     - Branding Alpha Wolves
Sound.svelte             - Gestion sons étendue
```

#### Composants Free Spin (7 fichiers)
```
FreeSpinIntro.svelte          - 3 types bonus (Pack Hunt, Enhanced, Alpha Dom)
FreeSpinOutro.svelte          - Total win + cascade multiplier
FreeSpinCounter.svelte        - Counter + grid size + multiplier
FreeSpinAnimation.svelte      - Animations meute
AlphaDominationIntro.svelte   - Intro 8x8, x5 min multiplier [NOUVEAU]
BonusTypeSelector.svelte      - Sélection 3 bonus (75x, 150x, 500x) [NOUVEAU]
PackHuntMeter.svelte          - Progression territory [NOUVEAU]
```

#### Composants Alpha Wolves Spécifiques (15 fichiers) [NOUVEAUX]
```
PackSplitAnimation.svelte         - Animation split Alpha Wolf
TerritoryExpandAnimation.svelte   - Animation expansion grille
HowlChainAnimation.svelte         - Animation chaîne hurlements
HuntCascadeAnimation.svelte       - Animation tumble/cascade
CascadeMultiplierDisplay.svelte   - Affichage multiplicateur (1x-500x)
TerritoryMeter.svelte             - Compteur territories collectés
VolatilityModeSelector.svelte     - Sélection Lone Wolf/Pack/Alpha
AlphaWolfSymbol.svelte            - Symbole Alpha Wolf spécialisé
HowlingWildSymbol.svelte          - Symbole Howling Wild + multiplicateur
MoonScatterSymbol.svelte          - Symbole Moon Scatter
TerritorySymbol.svelte            - Symbole Territory
GridExpansionOverlay.svelte       - Overlay expansion grille
WaysCounter.svelte                - Affichage ways dynamique
MultiplierChainEffect.svelte      - Effet particules chaîne
CryptoSymbolEffects.svelte        - Effets symboles crypto
```

#### Composants Win (5 fichiers)
```
Win.svelte                    - Win display 50,000x + cascade multi
WinAnimation.svelte           - Animations victoire loup
WinCoins.svelte               - Particules crypto
MaxWinAnimation.svelte        - Animation max win 50,000x [NOUVEAU]
CascadeWinAccumulator.svelte  - Total running cascades [NOUVEAU]
```

#### Composants Anticipation (2 fichiers)
```
Anticipations.svelte    - Container anticipations
Anticipation.svelte     - Effet anticipation Moon Scatter
```

#### Composants UI (5 fichiers) [NOUVEAUX]
```
AlphaWolvesLogo.svelte   - Logo animé
InfoPanel.svelte         - Paytable, règles, features
FeatureBuyPanel.svelte   - 3 options achat bonus
SettingsPanel.svelte     - Sélection mode volatilité
MobileDrawer.svelte      - UI mobile compacte
```

### 2.3 Routes (`src/routes/` - 3 fichiers)
```
+layout.svelte    - Layout racine (identique Ways)
+layout.ts        - Load function (identique Ways)
+page.svelte      - Page principale (identique Ways)
```

### 2.4 Stories Storybook (`src/stories/` - 15 fichiers)

| Fichier | Description |
|---------|-------------|
| `ComponentsGame.stories.svelte` | Game complet |
| `ComponentsSymbol.stories.svelte` | 12 symboles, tous états |
| `ComponentsPackSplit.stories.svelte` | Tests Pack Split |
| `ComponentsTerritoryExpand.stories.svelte` | Tests Territory |
| `ComponentsHowlChain.stories.svelte` | Tests Howl Chain |
| `ComponentsHuntCascade.stories.svelte` | Tests Cascade |
| `ModeBaseBook.stories.svelte` | Livres base game |
| `ModeBaseBookEvent.stories.svelte` | Events base |
| `ModeBonusBook.stories.svelte` | Livres bonus |
| `ModeBonusBookEvent.stories.svelte` | Events bonus |
| `ModeAlphaDomination.stories.svelte` | Tests Alpha Dom |
| `data/base_books.ts` | Données test base |
| `data/bonus_books.ts` | Données test bonus |
| `data/alpha_domination_books.ts` | Données test Alpha Dom |
| `data/base_events.ts` | Events individuels |

### 2.5 Internationalisation (`src/i18n/` - 10 fichiers)
```
i18nDerived.ts
messagesMap/index.ts
messagesMap/en.ts    - Anglais
messagesMap/zh.ts    - Chinois
messagesMap/es.ts    - Espagnol
messagesMap/pt.ts    - Portugais
messagesMap/de.ts    - Allemand
messagesMap/fr.ts    - Français
messagesMap/ja.ts    - Japonais
messagesMap/ko.ts    - Coréen
```

**Traductions requises:**
- Noms symboles (BOSS_WOLF, HUSTLER, etc.)
- Features (Pack Hunt, Alpha Domination, etc.)
- Modes (Lone Wolf, Pack, Alpha)
- Mécaniques (Hunt Cascade, Pack Split, Howl Chain, Territory Expand)
- UI (Ways count, multiplicateurs, free spins)

---

## PARTIE 3: ASSETS STATIQUES (`static/assets/`)

### 3.1 Animations Spine (`spines/` - 22 dossiers)

| Dossier | Contenu |
|---------|---------|
| `symbols_premium/` | BOSS_WOLF, HUSTLER, TECH_BRO, DIAMOND_HANDS (.json + .atlas) |
| `symbols_low/` | BONE, MEAT, CLAW, FANG (.json + .atlas) |
| `symbols_special/` | ALPHA_WOLF, HOWLING_WILD, MOON_SCATTER, TERRITORY |
| `backgrounds/` | base_bg, freegame_bg, alpha_domination_bg |
| `effects/` | pack_split, territory_expand, howl_chain, cascade |
| `ui/` | cascade_multiplier, territory_meter, ways_counter |
| `bigwin/` | big_win, super_win, mega_win, epic_win, max_win |
| `loader/` | loader |
| `anticipation/` | anticipation |
| `transition/` | transition (wolf howl) |
| `fsIntro/` | pack_hunt_intro, enhanced_intro, alpha_domination_intro |
| `reelhouse/` | reelhouse_glow, reelhouse_expand |

### 3.2 Sprite Sheets (`sprites/` - 15 dossiers)

| Dossier | Contenu |
|---------|---------|
| `symbolsStatic/` | 12 symboles statiques .webp + atlas |
| `reelsFrame/` | Frames pour toutes tailles grille |
| `progressBar/` | Barre progression loading |
| `freeSpins/` | Sprites compteur FS |
| `winSmall/` | Petites victoires localisées |
| `pressToContinue/` | Sprites "press to continue" |
| `volatilityModes/` | Boutons sélection mode |
| `buyBonus/` | Boutons achat bonus |
| `cascadeMultiplier/` | Frame multiplicateur |
| `territoryMeter/` | Sprites territory meter |
| `waysCounter/` | Affichage ways |
| `crypto/` | Particules crypto coins |
| `coin/` | Particules pièces |
| `payFrame/` | Bordure win frame |
| `uiElements/` | Éléments UI divers |

### 3.3 Polices (`fonts/` - 5 dossiers)
```
goldFont/      - Police or (victoires)
goldBlur/      - Police or blur (effets)
silverFont/    - Police argent (secondaire)
alphaFont/     - Police custom Alpha Wolves
cryptoFont/    - Police symboles crypto
```

### 3.4 Audio (`audio/` - 5 fichiers)
```
sounds.json    - Définitions audio sprites
sounds.mp3     - Sprite MP3
sounds.ogg     - Sprite OGG
sounds.m4a     - Sprite M4A
sounds.ac3     - Sprite AC3
```

**Sons requis (~60):**

| Catégorie | Sons |
|-----------|------|
| BGM | bgm_main, bgm_freespin, bgm_alpha_domination, bgm_winlevel_big/super/mega/epic/max |
| Symboles | sfx_boss_wolf_land, sfx_alpha_wolf_land, sfx_howling_wild_land, sfx_moon_scatter_1-5, sfx_territory_land, sfx_bone_land, sfx_meat_land |
| Mécaniques | sfx_pack_split, sfx_territory_expand, sfx_howl_chain, sfx_cascade_1-5+, sfx_mode_switch |
| UI | sfx_btn_general, sfx_btn_spin, sfx_reel_stop_1-6, sfx_anticipation |
| Victoires | sfx_winlevel_small-max, sfx_bigwin_coinloop |

---

## PARTIE 4: FICHIERS CONFIGURATION (8 fichiers)

```
package.json        - Dépendances, scripts
.eslintrc.cjs       - Config ESLint
lingui.config.ts    - Config Lingui i18n
.storybook/main.ts  - Config Storybook
.storybook/preview.ts - Preview Storybook
svelte.config.js    - Config Svelte
vite.config.ts      - Config Vite
tsconfig.json       - Config TypeScript
```

---

## PARTIE 5: RÉSUMÉ QUANTITATIF

| Catégorie | Ways SDK | Alpha Wolves | Delta |
|-----------|----------|--------------|-------|
| **Math SDK** | | | |
| Fichiers Python | 7 | 8 | +1 |
| Fichiers Reels CSV | 3 | 12 | +9 |
| **Web SDK** | | | |
| Game Config/Types | 12 | 14 | +2 |
| Composants Core | 15 | 15 | 0 |
| Composants Feature | 7 | 22 | +15 |
| Composants Win | 3 | 5 | +2 |
| Composants UI | 0 | 5 | +5 |
| Stories | 8 | 15 | +7 |
| i18n | 3 | 10 | +7 |
| **Assets** | | | |
| Dossiers Spine | 15 | 22 | +7 |
| Dossiers Sprites | 10 | 15 | +5 |
| Fichiers Audio | 5 | 5 | 0 |
| Dossiers Fonts | 4 | 5 | +1 |
| Config Files | 8 | 8 | 0 |
| **TOTAL** | ~100 | ~161 | +61 |

---

## PARTIE 6: DÉFIS TECHNIQUES

1. **Système de Grille Dynamique** - Board doit resize de 6x5 à 8x8 fluidement
2. **Animation Cascade** - Mécanique tumble avec accumulation multiplicateur
3. **Logique Pack Split** - Duplication symboles sur plusieurs reels
4. **Math Howl Chain** - Règles combinaison multiplicateurs wilds adjacents (2=add, 3+=multiply)
5. **Tracking Territory** - Persistence collection à travers cascades
6. **Max Win 50,000x** - Optimisation RTP pour haute variance
7. **3 Modes Volatilité** - Modèles math séparés avec switching

---

## PARTIE 7: FICHIERS CRITIQUES

Les 5 fichiers les plus importants à implémenter en premier:

1. **`/alpha-wolves/math-sdk/game_config.py`** - Tous paramètres, paytables, configurations grille, modes volatilité, bet modes
2. **`/alpha-wolves/math-sdk/gamestate.py`** - Loop jeu principal avec Hunt Cascade, Pack Split, Territory Expansion, Howl Chain
3. **`/alpha-wolves/web-sdk/src/game/stateGame.svelte.ts`** - Gestion état board dynamique pour expansion grille et tracking cascade
4. **`/alpha-wolves/web-sdk/src/game/bookEventHandlerMap.ts`** - Handlers pour les 6 nouveaux événements Alpha Wolves
5. **`/alpha-wolves/web-sdk/src/components/Board.svelte`** - Rendu grille dynamique avec support cascade et expansion

---

## PARTIE 8: SÉQUENCE D'IMPLÉMENTATION

### Phase 1: Math Engine Core
1. game_config.py - Toutes configurations
2. gamestate.py - Loop jeu principal
3. game_executables.py - Évaluation ways
4. game_override.py - Symboles spéciaux
5. Fichiers CSV reels (12 fichiers)

### Phase 2: Math Mechanics
1. Hunt Cascade logic
2. Pack Split logic
3. Territory Expansion logic
4. Howl Chain logic
5. game_events.py - Événements custom
6. game_optimization.py - Cibles RTP

### Phase 3: Web Core
1. config.ts, types.ts, constants.ts
2. stateGame.svelte.ts (grille dynamique)
3. typesBookEvent.ts, typesEmitterEvent.ts
4. bookEventHandlerMap.ts

### Phase 4: Composants Core
1. Game.svelte, Board.svelte
2. Tous composants symboles (12)
3. BoardBase, BoardContainer, BoardFrame
4. Background.svelte (4 modes)

### Phase 5: Composants Features
1. PackSplitAnimation.svelte
2. TerritoryExpandAnimation.svelte
3. HowlChainAnimation.svelte
4. HuntCascadeAnimation.svelte
5. CascadeMultiplierDisplay.svelte
6. TerritoryMeter.svelte

### Phase 6: Composants Bonus
1. FreeSpinIntro.svelte (3 types)
2. FreeSpinOutro.svelte
3. AlphaDominationIntro.svelte
4. BonusTypeSelector.svelte
5. Composants Win

### Phase 7: Assets (Parallèle)
1. Animations Spine
2. Sprite sheets
3. Fichiers audio
4. Polices

### Phase 8: Testing & Polish
1. Stories Storybook
2. Traductions i18n
3. Vérification RTP
4. Optimisation performance

---

## Vérification

Pour tester l'implémentation:

1. **Math SDK**:
   - Exécuter `python run.py` avec simulations
   - Vérifier RTP atteint pour chaque mode
   - Valider distribution wins

2. **Web SDK**:
   - `npm run storybook` pour tester composants isolés
   - `npm run dev` pour tester jeu complet
   - Vérifier toutes animations et transitions
   - Tester sur mobile et desktop
