const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, convertInchesToTwip
} = require('docx');

const INK="20262B", BODY="3C454C", MUTED="7A848C", RULE="D8DCDF";
const ACCENT="0F6E77", TINT="EEF1F2", TINT2="F5F7F7", ACCENTBG="E4EDED", WARN="9A5B2C";
const F="Times New Roman", MONO="Times New Roman";
const NB={top:{style:BorderStyle.NONE},bottom:{style:BorderStyle.NONE},left:{style:BorderStyle.NONE},
  right:{style:BorderStyle.NONE},insideHorizontal:{style:BorderStyle.NONE},insideVertical:{style:BorderStyle.NONE}};

function t(x,o={}){return new TextRun({text:x,font:o.mono?MONO:F,size:o.size||19,bold:!!o.bold,
  italics:!!o.italics,color:o.color||BODY,allCaps:!!o.caps,characterSpacing:o.spacing||0});}
function P(runs,o={}){return new Paragraph({children:Array.isArray(runs)?runs:[runs],
  alignment:o.align||AlignmentType.LEFT,
  spacing:{before:o.before||0,after:o.after!==undefined?o.after:60,line:o.line||256},
  ...(o.shading?{shading:{type:ShadingType.CLEAR,fill:o.shading}}:{}),
  ...(o.border?{border:o.border}:{}),...(o.indent?{indent:o.indent}:{}),
  ...(o.bullet?{bullet:{level:0}}:{})});}
function C(children,o={}){return new TableCell({children,width:{size:o.w,type:WidthType.DXA},
  shading:o.fill?{type:ShadingType.CLEAR,fill:o.fill}:undefined,
  margins:{top:o.mt||70,bottom:o.mb||70,left:o.ml||130,right:o.mr||130},
  verticalAlign:o.valign||"top",borders:o.borders||NB});}
function H(num,txt){return P([t(num+"   ",{bold:true,size:20,color:ACCENT}),
  t(txt,{bold:true,size:20,color:INK,spacing:2})],
  {before:170,after:55,border:{bottom:{style:BorderStyle.SINGLE,size:6,color:RULE,space:6}}});}
function sub(txt){return P([t(txt,{size:16,color:MUTED,italics:true})],{after:80});}

const PAGE_W=12240, MARGIN=convertInchesToTwip(0.75), CONTENT=PAGE_W-2*MARGIN;

const title=[
  P([t("Research Data Management",{bold:true,size:34,color:INK,spacing:2})],{after:20}),
  P([t("How our group structures, documents and shares research data across its lifecycle.",
      {size:18,color:MUTED,italics:true})],{after:60,
      border:{bottom:{style:BorderStyle.SINGLE,size:20,color:ACCENT,space:12}}}),
  P([t("DRAFT FOR DISCUSSION",{bold:true,size:13,color:WARN,caps:true,spacing:10}),
     t("     Johannes' suggestions — Katharina & Joachim, please comment; existing lab rules take precedence.",
      {size:14,color:MUTED,italics:true})],{after:40,before:40}),
];

const cwF=Math.floor((CONTENT-3*90)/4);
function fairCard(letter,word,line){return C([
  P([t(letter,{bold:true,size:30,color:ACCENT})],{after:20}),
  P([t(word,{bold:true,size:16,color:INK,caps:true,spacing:6})],{after:26}),
  P([t(line,{size:13,color:BODY})],{line:214})],
  {w:cwF,fill:TINT2,mt:120,mb:120,ml:120,mr:120,borders:{...NB,bottom:{style:BorderStyle.SINGLE,size:16,color:ACCENT}}});}
const gap=()=>C([],{w:90});
const fairRow=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[cwF,90,cwF,90,cwF,90,cwF],borders:NB,
  rows:[new TableRow({children:[
    fairCard("F","Findable","Persistent IDs and rich metadata, so data can be located."),gap(),
    fairCard("A","Accessible","A clear licence and defined access conditions."),gap(),
    fairCard("I","Interoperable","Open formats and controlled vocabularies."),gap(),
    fairCard("R","Reusable","Provenance and documentation, for you and others."),
  ]})]});

const cwL=Math.floor((CONTENT-3*110)/4);
function lc(num,ttl,lines){return C([P([t(num,{bold:true,size:22,color:ACCENT})],{after:16}),
  P([t(ttl,{bold:true,size:16,color:INK,caps:true,spacing:4})],{after:34})]
  .concat(lines.map(l=>P([t(l,{size:13,color:BODY})],{after:14,line:212}))),
  {w:cwL,fill:TINT,mt:110,mb:110,ml:130,mr:130});}
function arr(){return C([P([t("\u2192",{size:22,color:MUTED})],{align:AlignmentType.CENTER})],{w:110,valign:"center"});}
const lifecycle=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[cwL,110,cwL,110,cwL,110,cwL],borders:NB,
  rows:[new TableRow({children:[
    lc("1","Plan",["Write the DMP first","Create the folder skeleton","Agree naming & licence","Choose the repository"]),arr(),
    lc("2","Collect & describe",["Raw data in, then locked","Log in the ELN < 48 h","Metadata at capture","Controlled vocabulary"]),arr(),
    lc("3","Process by code",["Raw \u2192 primary \u2192 secondary","Numbered to the plan","Versioned in Git","Data never in Git"]),arr(),
    lc("4","Share & publish",["Back up 3-2-1","G1: FAIR + GDPR check","G2: repository, DOI, licence","Never a cloud link"]),
  ]})]});
const gates=P([t("Two gates before data leaves the group.  ",{bold:true,size:15,color:INK}),
  t("G1 \u2014 sharing with anyone: pass the FAIR self-check and the GDPR rules (pseudonymise; patient-identifying data stays at UKW).  "
    +"G2 \u2014 publishing: deposit to a repository with a DOI and a licence, not a cloud link.",{size:15,color:BODY})],
  {before:110,line:238,shading:ACCENTBG,border:{left:{style:BorderStyle.SINGLE,size:22,color:ACCENT,space:10},
    top:{style:BorderStyle.SINGLE,size:4,color:ACCENT},bottom:{style:BorderStyle.SINGLE,size:4,color:ACCENT},
    right:{style:BorderStyle.SINGLE,size:4,color:ACCENT}}});

const tree=[
  ["PROJECT_NAME/",INK,true,""],["\u2502",MUTED,false,""],
  ["\u251c\u2500 README.md",ACCENT,true,"guides the folder \u00b7 install & run \u00b7 full reproducibility"],
  ["\u251c\u2500 DMP.(docx/pdf)",INK,true,"data management plan"],
  ["\u251c\u2500 LICENSE",INK,true,"how others may use code & data"],["\u2502",MUTED,false,""],
  ["\u251c\u2500 data/",INK,true,""],
  ["\u2502   \u251c\u2500 raw_data/",INK,false,"first-generated, unprocessed \u00b7 read-only \u00b7 may be a link to a source"],
  ["\u2502   \u251c\u2500 primary_data/",INK,false,"raw made usable \u2014 cleaned, open, analysis-ready"],
  ["\u2502   \u251c\u2500 secondary_data/",INK,false,"compiled from existing / external sources"],
  ["\u2502   \u2514\u2500 meta_data/",ACCENT,false,"the data model \u00b7 controlled vocabulary \u00b7 linked to the data"],["\u2502",MUTED,false,""],
  ["\u251c\u2500 documents/",INK,true,""],
  ["\u2502   \u251c\u2500 project_plan/",INK,false,"the plan \u00b7 pipeline & workflow flowcharts \u00b7 ELN link"],
  ["\u2502   \u2514\u2500 report/",INK,false,"daily reports \u00b7 intermediate results \u00b7 discussion"],["\u2502",MUTED,false,""],
  ["\u251c\u2500 scripts/",INK,false,"every pipeline step, numbered & named to the plan"],
  ["\u251c\u2500 analysis/",INK,false,"inputs & outputs per step \u00b7 same numbering as scripts/"],
  ["\u251c\u2500 results/",INK,false,"selected results \u00b7 paper figures \u00b7 summaries"],
  ["\u251c\u2500 code/",INK,false,"when scripts grow into an application"],
  ["\u251c\u2500 var/",MUTED,false,"various \u2014 anything that doesn't fit above"],
  ["\u2514\u2500 \u2026",MUTED,false,"optional project-specific folders"],
];
const treeCell=C(tree.map(([path,color,bold,note])=>
  P([t(path.padEnd(22),{mono:true,size:16,color,bold}),
     ...(note?[t("  "+note,{size:13,color:MUTED,italics:true})]:[])],{after:15,line:228})),
  {w:CONTENT,fill:TINT2,mt:150,mb:150,ml:170,mr:170,borders:{...NB,left:{style:BorderStyle.SINGLE,size:16,color:ACCENT}}});
const treeTable=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[CONTENT],borders:NB,
  rows:[new TableRow({children:[treeCell]})]});

const cw3=Math.floor((CONTENT-2*140)/3);
function anchor(head,body){return C([P([t(head,{bold:true,size:14,color:ACCENT,caps:true,spacing:6})],{after:40}),
  P([t(body,{size:13,color:BODY})],{line:216})],{w:cw3,fill:TINT,mt:100,mb:100,ml:130,mr:130});}
const anchorRow=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[cw3,140,cw3,140,cw3],borders:NB,
  rows:[new TableRow({children:[
    anchor("Raw is the ground truth","raw_data/ is read-only, or a link to the source. If it changes, nothing downstream can be trusted."),
    C([],{w:140}),
    anchor("Analysis mirrors the plan","scripts/, analysis/ and results/ share the numbering in documents/project_plan/ \u2014 one map, followed everywhere."),
    C([],{w:140}),
    anchor("Metadata stays connected","A tailored data model linked to the data, controlled vocabulary where it exists \u2014 some auto-collected, some via ontology-DB API."),
  ]})]});

const defBorder={top:{style:BorderStyle.SINGLE,size:4,color:RULE},bottom:{style:BorderStyle.SINGLE,size:4,color:RULE},
  left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE},
  insideHorizontal:{style:BorderStyle.SINGLE,size:4,color:RULE},insideVertical:{style:BorderStyle.NONE}};
function defRow(term,def){return new TableRow({children:[
  C([P([t(term,{bold:true,size:14,color:ACCENT,mono:true})])],{w:CONTENT*0.26,valign:"top",mt:80,mb:80}),
  C([P([t(def,{size:14,color:BODY})],{line:222})],{w:CONTENT*0.74,mt:80,mb:80}),
]});}
const defTable=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[CONTENT*0.26,CONTENT*0.74],
  borders:defBorder,rows:[
    defRow("raw_data/","First-generated, unprocessed data \u2014 measurements, reads, scans, responses. Unseen, uninterpreted. Read-only, or a link to where it lives."),
    defRow("primary_data/","Raw data made usable: cleaned and converted to open, analysis-ready formats \u2014 by code, never by hand."),
    defRow("secondary_data/","Data compiled from existing sources \u2014 external databases, reference sets, corpora. Not generated by us."),
    defRow("meta_data/","The description that makes data reusable: a tailored data model, connected to the data. Technical, biological or clinical; controlled vocabulary where it exists, some fields auto-collected, some via ontology-database API."),
    defRow("scripts/ \u00b7 analysis/","The pipeline and its inputs/outputs, numbered to match the project plan. Delete everything downstream of raw_data/ and this regenerates it."),
    defRow("results/","Selected outputs: paper figures, summaries for discussion. A curated subset, not every intermediate."),
  ]});

const nameCell=C([P([t("YYYYMMDD_project_sample_condition_type_v01.ext",{size:16,bold:true,mono:true,color:INK})],{after:60,line:224}),
  ...["No spaces \u2014 use _ between fields, - within a field.","No special characters ( / \\ : * ? \" < > | & ).",
    "Dates as YYYYMMDD \u2014 sorts chronologically.","Leading zeros: 01, 02 \u2026 so files stay in order.",
    "General field first, specific last. Be consistent."].map(x=>P([t(x,{size:14,color:BODY})],{bullet:true,after:12,line:214}))],
  {w:CONTENT,fill:TINT2,mt:120,mb:120,ml:160,mr:160,borders:{...NB,left:{style:BorderStyle.SINGLE,size:16,color:ACCENT}}});
const nameTable=new Table({width:{size:CONTENT,type:WidthType.DXA},columnWidths:[CONTENT],borders:NB,
  rows:[new TableRow({children:[nameCell]})]});

// ==================== 6. LINKS — the connective tissue ===================
// A table: what to link | where it points | put the link here
const linkBorder={top:{style:BorderStyle.SINGLE,size:4,color:RULE},bottom:{style:BorderStyle.SINGLE,size:4,color:RULE},
  left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE},
  insideHorizontal:{style:BorderStyle.SINGLE,size:4,color:RULE},insideVertical:{style:BorderStyle.NONE}};
function linkHead(){return new TableRow({children:[
  C([P([t("Link to",{bold:true,size:13,color:MUTED,caps:true,spacing:6})])],{w:CONTENT*0.24,mt:60,mb:60}),
  C([P([t("What it connects",{bold:true,size:13,color:MUTED,caps:true,spacing:6})])],{w:CONTENT*0.46,mt:60,mb:60}),
  C([P([t("Recorded in",{bold:true,size:13,color:MUTED,caps:true,spacing:6})])],{w:CONTENT*0.30,mt:60,mb:60}),
]});}
function linkRow(a,b,c){return new TableRow({children:[
  C([P([t(a,{bold:true,size:14,color:ACCENT})])],{w:CONTENT*0.24,mt:55,mb:55}),
  C([P([t(b,{size:14,color:BODY})],{line:220})],{w:CONTENT*0.46,mt:55,mb:55}),
  C([P([t(c,{size:13,color:MUTED,mono:true})],{line:216})],{w:CONTENT*0.30,mt:55,mb:55}),
]});}
const linkTable=new Table({width:{size:CONTENT,type:WidthType.DXA},
  columnWidths:[CONTENT*0.24,CONTENT*0.46,CONTENT*0.30],borders:linkBorder,rows:[
  linkHead(),
  linkRow("ELN","The lab-notebook entry for each run — the same sample ID used in the folder.","README.md · meta_data/"),
  linkRow("Data / cloud","Where the data actually lives if it is not in this folder (Nextcloud, group storage, an archive).","README.md · raw_data/ (as a link)"),
  linkRow("Analysis server","The HPC / JupyterHub location where the pipeline runs, if not local.","README.md · project_plan/"),
  linkRow("Code repository","The Git repository holding scripts/ and code/.","README.md"),
  linkRow("Repository DOI","The published dataset (Zenodo, ArrayExpress, PRIDE …) and the code DOI.","README.md · DMP"),
  linkRow("Publication","The paper the data supports, once it exists.","README.md · DMP"),
]});
const linkNote=P([
  t("Link richly, and both ways.  ",{bold:true,size:15,color:INK}),
  t("Data, its documentation, and its analysis are only one project if they point at each other. A dataset with no link to its ELN entry, its code, or its storage location is an orphan — technically present, practically lost. Use the same identifier everywhere, and keep every external link in the README so nothing has to be hunted for.",
    {size:15,color:BODY}),
],{before:70,line:230,shading:ACCENTBG,
  border:{left:{style:BorderStyle.SINGLE,size:22,color:ACCENT,space:10},
    top:{style:BorderStyle.SINGLE,size:4,color:ACCENT},bottom:{style:BorderStyle.SINGLE,size:4,color:ACCENT},
    right:{style:BorderStyle.SINGLE,size:4,color:ACCENT}}});

const editNote=P([t("Open for discussion.  ",{bold:true,size:14,color:WARN}),
  t("A starting suggestion, not a final rule set. Please add or amend with Word comments; where existing lab regulations differ, they take precedence. Everything folds into one agreed handout.",
    {size:14,color:BODY,italics:true})],{before:80,line:228,shading:TINT,
    border:{left:{style:BorderStyle.SINGLE,size:18,color:WARN,space:10}}});

const doc=new Document({sections:[{
  properties:{page:{size:{width:PAGE_W,height:15840},margin:{top:MARGIN,bottom:MARGIN,left:MARGIN,right:MARGIN}}},
  children:[...title,
    H("1","The principle \u2014 FAIR"),
    sub("Everything below serves these four properties. They are the why; the rest is the how."),fairRow,
    H("2","The lifecycle"),
    sub("Every project moves left to right. Start before you collect anything."),lifecycle,gates,
    H("3","The folder structure"),
    sub("The same skeleton for every project \u2014 3 files or 30,000. Anyone opening it knows where things are."),
    treeTable,P([],{after:70}),anchorRow,
    H("4","What goes where"),defTable,
    H("5","Naming"),nameTable,
    H("6","Links \u2014 the connective tissue"),
    sub("Data, documentation and analysis are one project only if they point at each other. Where something lives outside this folder, link to it \u2014 richly, and in the README."),
    linkNote,
    P([],{after:80}),
    linkTable,
    editNote,
  ],
}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("/home/claude/RDM_handout.docx",b);console.log("written",b.length,"bytes");});

// ---------------------------------------------------------------------------
// NOTE: this is the v2-era generator. It produces a valid, styled handout.
// The shipped v3 handout added: §6 Links (connective tissue), §7 machine-
// readability (eLabFTW export, no-PDF-for-data), and sample-ID-created-first.
// To regenerate an exact v3, re-add those sections here. To just restyle or
// re-word the existing sections, edit this file and run:  node rdm_handout_generator.js
// This file belongs in the GIT REPO (app/ or build/), NOT the download bundle —
// a .js in a downloaded zip trips Windows Defender's MalUri heuristic (a false
// positive on "script + URL"). In git it clones cleanly.
// ---------------------------------------------------------------------------
