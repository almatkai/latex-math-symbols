import Ajv2020 from 'ajv/dist/2020.js';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
const load=p=>JSON.parse(readFileSync(new URL(p,import.meta.url)));
const validate=new Ajv2020({allErrors:true,strict:false}).compile(load('../fixtures/beta/schemas/extension-v2.schema.json'));
const manifest=load('../manifest.json');
assert.ok(validate(manifest),JSON.stringify(validate.errors));
const mutations=[
 m=>{delete m.schemaVersion},m=>m.schemaVersion=1,m=>m.id='raycast.latex-math-symbols',m=>m.author='forbidden',
 m=>m.runtime='javascript',m=>m.slug='../escape',m=>m.icon='https://remote/icon.png',m=>m.icon='/extensions/icons/UPPER.png',
 m=>m.replaces=[],m=>m.replaces=['other'],m=>m.replaces.push(m.replaces[0]),
 m=>m.commands=[],m=>m.commands[0].name='',m=>m.commands[0].runtime='js',m=>m.commands[0].platforms=[],
 m=>m.commands[0].platforms=['linux'],m=>m.platforms=['macOS','macOS'],m=>m.preferences={},
 m=>m.verification=[],m=>m.verification[0].state='tested',m=>{delete m.verification[0].platform},m=>m.name=''
];
for(const mutate of mutations){const m=structuredClone(manifest);mutate(m);assert.equal(validate(m),false,JSON.stringify(m));}
assert.deepEqual(manifest.verification.map(v=>v.state),['not-run','not-run']);
assert.deepEqual(manifest.commands.map(c=>c.name),['index']);
console.log(`Pinned full draft 2020-12 schema: 1 positive + ${mutations.length} negative cases passed.`);
