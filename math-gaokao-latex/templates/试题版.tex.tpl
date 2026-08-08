% !TeX program = xelatex
% ============================================================
% @@TITLE@@ · @@EDITION@@
% 由 tools/make_editions.py 生成（重跑会覆盖本文件）；
% 题目/解析内容在 questions.tex / answers*.tex，勿在本文件内写内容。
% ============================================================
\documentclass[@@CLASS_OPTIONS@@]{ctexart}
\input{../common/preamble}
\input{../common/macros}
\input{../common/questions_env}
\renewcommand{\gkpaperid}{@@PAPER_ID@@}
\renewcommand{\gkheadL}{@@TITLE@@ · 数学}
\renewcommand{\gkheadR}{@@EDITION@@}
\hypersetup{pdftitle={@@TITLE@@ 数学 · @@EDITION@@}}
\begin{document}
\begin{center}
  {\Large\bfseries @@TITLE@@}\\[4pt]
  {\large 数学 · @@EDITION@@}
\end{center}
\medskip
@@BODY@@\end{document}
