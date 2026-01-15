# Alpha Wolves - Math SDK

## Fichiers à créer ici

```
math-sdk/
├── run.py                 # Orchestrateur principal
├── game_config.py         # Configuration singleton
├── gamestate.py           # Logique de jeu
├── game_executables.py    # Calculs ways, cascade
├── game_override.py       # Fonctions symboles spéciaux
├── game_calculations.py   # Math custom
├── game_events.py         # Événements custom
├── game_optimization.py   # Setup optimisation RTP
└── reels/
    ├── BR_LONE_WOLF.csv
    ├── BR_PACK.csv
    ├── BR_ALPHA.csv
    ├── FR_PACK_HUNT.csv
    ├── FR_ENHANCED.csv
    ├── FR_ALPHA_DOM.csv
    ├── FR_6x6.csv
    ├── FR_7x6.csv
    ├── FR_7x7.csv
    ├── FR_8x8.csv
    ├── WINCAP_BASE.csv
    └── WINCAP_BONUS.csv
```

## Référence
- Voir `INTERFACE_CONTRACT.md` pour les symboles et événements
- Voir `ALPHA_WOLVES_IMPLEMENTATION_PLAN.md` PARTIE 1
- S'inspirer de `../math-sdk/` (Ways SDK original)
