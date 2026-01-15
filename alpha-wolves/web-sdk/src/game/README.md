# Game Config (14+ fichiers)

## Fichiers à créer

| Fichier | Description |
|---------|-------------|
| `config.ts` | Configuration jeu (symboles, betModes, grille) |
| `types.ts` | Types partagés (copier depuis INTERFACE_CONTRACT.md section 5) |
| `typesBookEvent.ts` | Types événements (copier depuis INTERFACE_CONTRACT.md section 4) |
| `typesEmitterEvent.ts` | Types emitter events |
| `constants.ts` | Constantes, SYMBOL_INFO_MAP |
| `stateGame.svelte.ts` | État réactif Svelte 5 |
| `stateApp.ts` | État app PixiJS |
| `stateLayout.ts` | État layout responsive |
| `stateXstate.ts` | État machine XState |
| `eventEmitter.ts` | Event emitter |
| `bookEventHandlerMap.ts` | Handlers tous événements |
| `actor.ts` | Game actor |
| `utils.ts` | Utilitaires |
| `winLevelMap.ts` | Mapping win levels (1-10) |
| `sound.ts` | Définitions sons |
| `assets.ts` | Définitions assets |
| `context.ts` | Context Svelte |

## Ordre d'implémentation
1. types.ts + typesBookEvent.ts
2. config.ts + constants.ts
3. stateGame.svelte.ts
4. bookEventHandlerMap.ts
5. Le reste
