// Execute exact AST declarations from a pinned fixture. No algorithm replacements.
import vm from 'node:vm';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require=createRequire(new URL('../.work/v1/package.json',import.meta.url));
export const ts=require('typescript');
export function declarations(path,names,globals={}) {
  const source=readFileSync(path,'utf8');
  const tree=ts.createSourceFile(String(path),source,ts.ScriptTarget.Latest,true,String(path).endsWith('.tsx')?ts.ScriptKind.TSX:ts.ScriptKind.TS);
  const found=new Map();
  for(const node of tree.statements) {
    if(ts.isFunctionDeclaration(node)&&node.name) found.set(node.name.text,node.getFullText(tree));
    if(ts.isVariableStatement(node)) for(const d of node.declarationList.declarations) {
      if(ts.isIdentifier(d.name)) found.set(d.name.text,`const ${d.getText(tree)};`);
    }
  }
  const text=names.map(n=>{ if(!found.has(n))throw Error(`Missing beta declaration ${n}`);return found.get(n); }).join('\n');
  const compiled=ts.transpileModule(text, {fileName:String(path),compilerOptions:{target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.React,module:ts.ModuleKind.CommonJS}}).outputText;
  const context={console,...globals,result:null};
  vm.runInNewContext(compiled+`\nresult={${names.join(',')}};`,context,{timeout:10000});
  return context.result;
}
export function execute(source,requireFn) {
  const exports={};const module={exports};
  vm.runInNewContext(ts.transpile(source,{target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,module:ts.ModuleKind.CommonJS,esModuleInterop:true}),{exports,module,require:requireFn,console},{timeout:10000});
  return module.exports;
}
export const plain=x=>JSON.parse(JSON.stringify(x));
