// Runs the unchanged own TS module. This is a validation/build-time tool only.
import commands from '../fixtures/own/src/commands';
import { writeFileSync } from 'node:fs';
writeFileSync(new URL('../data/commands.json', import.meta.url), JSON.stringify(commands, null, 2) + '\n');
console.log(`${commands.length} symbols, ${commands.filter(s => s.variants).length} variant groups`);
