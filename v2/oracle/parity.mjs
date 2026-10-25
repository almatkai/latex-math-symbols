import assert from 'node:assert/strict';
import { readFileSync,writeFileSync,mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { declarations,execute,plain } from './beta-extract.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const require=createRequire(import.meta.url);
const Fuse=require('../libraries/fuse.js/fuse.common.js');
const beta=declarations(`${root}/fixtures/beta/src/main/extension-runner.ts`,[
 'JSX_FRAGMENT','REACT_CONTEXT','RUNTIME_COMPONENT_LIMIT','RUNTIME_RECURSION_LIMIT',
 'hookDepsEqual','flushPendingEffects','createJsxRuntimeShim','createReactShim','makeToken','isToken',
 'normalizeActionTitle','stableActionId','parseShortcut','pushEffect','copyToSystemClipboard','registerAction',
 'isJsxNode','sanitizeValue','walkRuntimeNodes'
],{createHash:(await import('node:crypto')).createHash,
 copyClipboardContent:()=>{throw Error('Real clipboard forbidden');},
 pasteClipboardContent:()=>{throw Error('Real paste forbidden');},shell:new Proxy({}, {get(){throw Error('Real shell forbidden');}})});
const session={hookStates:[],hookIndex:0,pendingEffects:[],effectDeps:new Map(),effectCleanups:new Map(),
 hasStateUpdates:false,currentActions:[],actionHandlers:new Map(),effects:[],effectMode:'record',renderErrors:[],listItemLimit:10000};
const react=beta.createReactShim(session),jsx=beta.createJsxRuntimeShim();
const List=beta.makeToken('List');List.Item=beta.makeToken('List.Item');
const api={List,ActionPanel:beta.makeToken('ActionPanel'),Action:{CopyToClipboard:beta.makeToken('Action.CopyToClipboard')}};
const data=execute(readFileSync(`${root}/fixtures/own/src/commands.ts`,'utf8'),()=>{throw Error('Unexpected import');}).default;
const own=execute(readFileSync(`${root}/fixtures/own/src/index.tsx`,'utf8')+'\nexport {ITEMS,FuseOptions,fuse};',name=>{
 if(name==='react')return react;if(name==='react/jsx-runtime')return jsx;
 if(name==='./commands')return {default:data,__esModule:true};if(name==='@raycast/api')return api;
 if(name==='fuse.js')return Fuse;throw Error(`Unexpected own import ${name}`);
});
assert.deepEqual(plain(data),JSON.parse(readFileSync(`${root}/data/commands.json`)));
assert.equal(data.length,131);
function render(query) {
 if(session.searchTextChangeHandler)session.searchTextChangeHandler(query);
 let rootNode;
 for(let pass=0;pass<5;pass++) {
  session.hookIndex=0;session.currentActions=[];session.actionHandlers.clear();session.hasStateUpdates=false;
  rootNode=beta.walkRuntimeNodes(own.default(),session,0,{remaining:10000})[0];
  beta.flushPendingEffects(session);
  if(!session.hasStateUpdates)return rootNode;
 }
 throw Error('Source did not settle within five passes');
}
render('');
const queries=new Set(['',' ','  ','\t','\n','???','not-a-symbol','😀','日本','İ','K','Α','Σ','𝔸', '\\Delta','\\delta']);
for(const s of data) {
 for(const value of [s.command,s.example,...s.descriptions]) {
  queries.add(value);queries.add(value.toUpperCase());
  queries.add(value.slice(0,Math.min(value.length,4)));
  queries.add(value.slice(1));
  queries.add(value+'x');
  if(value.length>3) queries.add(value.slice(0,2)+'z'+value.slice(3));
 }
}
for(const size of [31,32,33,63,64,65,95,96,97,127,128,129,256,4096]) {
 queries.add('a'.repeat(size));queries.add(('matrix '+ '\\sqrt{} ').repeat(300).slice(0,size));
}
// Deterministic fuzz spanning ordinary ASCII, whitespace, escapes and UTF-16 surrogate pairs.
let seed=6734;const alphabet='abcdeinotmS\\{}^_ ;>=!\t\n😀';
for(let n=0;n<400;n++) {
 let q='';for(let k=0;k<n%40+1;k++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;q+=Array.from(alphabet)[seed%Array.from(alphabet).length];}queries.add(q);
}
const qs=[...queries];
const scores=new Fuse(own.ITEMS,{...own.FuseOptions,includeScore:true});
const input=qs.map(q=>JSON.stringify(q)).join('\n')+'\n';
function run(binary) {
 const r=spawnSync(binary,[],{input,encoding:'utf8',maxBuffer:256*1024*1024});
 assert.equal(r.status,0,r.stderr);return r.stdout.trimEnd().split('\n').map(s=>JSON.parse(s));
}
const rust=run(process.env.LATEX_ENGINE_BIN||`${root}/target/debug/examples/search`);
const views=run(process.env.LATEX_ADAPTER_BIN||`${root}/.work/checks/runner/target/debug/examples/dump`);
assert.equal(rust.length,qs.length);assert.equal(views.length,qs.length);
let rows=0,scoreComparisons=0,nonBitExact=0,maxRelative=0,actionChecks=0;
for(let i=0;i<qs.length;i++) {
 const q=qs[i];const tree=render(q);
 const expected=q.length?scores.search(q).map(r=>({item:r.item,score:r.score})):own.ITEMS.map(item=>({item,score:null}));
 assert.deepEqual(rust[i].map(h=>h.item),plain(expected.map(h=>h.item)),`records/order ${JSON.stringify(q)}`);
 for(let j=0;j<expected.length;j++) {
  const a=rust[i][j].score,b=expected[j].score;
  if(b===null){assert.equal(a,null);continue;}
  const relative=Math.abs(a-b)/Math.max(Math.abs(b),Number.MIN_VALUE);
  maxRelative=Math.max(maxRelative,relative);if(a!==b)nonBitExact++;
  assert.equal(a,b,`exact score ${q}: ${a} != ${b}`);scoreComparisons++;
 }
 const v=views[i];assert.equal(v.ok,true);assert.equal(v.root.type,'List');
 assert.equal(v.root.props.filtering,tree.props.filtering);
 assert.equal(v.root.props.__hasServerSearch,tree.props.__hasServerSearch);
 assert.equal(v.root.props.searchBarPlaceholder,tree.props.searchBarPlaceholder);
 assert.equal(v.root.props.searchText,q);
 assert.deepEqual(v.root.children.map(row=>({title:row.props.title,subtitle:row.props.subtitle,accessories:row.props.accessories})),plain(tree.children.map(row=>({title:row.props.title,subtitle:row.props.subtitle,accessories:row.props.accessories}))),`actual beta reconciliation ${q}`);
 assert.equal(v.actions.length,session.currentActions.length);
 for(let j=0;j<v.actions.length;j++) {
  assert.equal(v.actions[j].title,session.currentActions[j].title);
  assert.equal(v.actions[j].kind,session.currentActions[j].kind);
  assert.deepEqual(v.root.children[j].props.actionIds,[v.actions[j].id]);
 }
 if(q==='')for(let j=0;j<session.currentActions.length;j++) {
  session.effects=[];await session.actionHandlers.get(session.currentActions[j].id)({content:'forged'});
  assert.deepEqual(plain(session.effects),[{kind:'clipboard',value:expected[j].item.title}]);actionChecks++;
 }
 rows+=expected.length;
}
const summary={queries:qs.length,exactRowsAndOrder:rows,scoreComparisons,scoreNonBitExact:nonBitExact,maxRelativeError:maxRelative,scoreRelativeTolerance:0,actualBetaReconciliations:qs.length,actualOwnCopyActions:actionChecks};
mkdirSync(`${root}/.work/oracle`,{recursive:true});writeFileSync(`${root}/.work/oracle/queries.json`,JSON.stringify(qs));
writeFileSync(`${root}/.work/oracle/summary.json`,JSON.stringify(summary,null,2)+'\n');
writeFileSync(`${root}/.work/oracle/initial-view.json`,JSON.stringify(views[0]));
console.log(JSON.stringify(summary,null,2));
