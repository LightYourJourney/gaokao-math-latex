# 2007 上海文科候选卷：paper/batch 登记与问题关联

- 日期：2026-11-03；工作树 `仓库根`，工作分支。
- 固定 source：`src-51aa9840dc7a866be37ded966d4a337c999cacd912ce0118e07b3e6c768c5789`，PDF SHA-256 `1d43489e28ce9c305faa753519800b9184e40cc40fbd8343f7fd287b4ec70212`。
- paper：`gk-2007-regular-shanghai-arts`；batch：`phase1-b83`；内部项目目录：`2007_上海卷_文科`。

## 注册事务

- 使用 `.work/registration/2007-shanghai-arts.json` 先以 `write=False` 校验规格，返回唯一阻断项 `ISSUE-1362`；随后由 `source_manifest.py register-papers --write` 原子登记 paper、batch、来源反向绑定和问题总账。
- manifest revision 从 `6047` 推进到 `6048`；transaction ID `a9e4b010-d1cb-497f-a112-8d5df5c75fbc`。纸卷的 `production_state=blocked`、`blocked_from=planned`；batch 当前 `planned`，等待 provenance 导入推进状态。
- 固定来源与 paper 的关系在本库登记为 `canonical`，只表示该候选 PDF 是当前卷稿的绑定来源。原始出版者、版次、复制链与官方身份仍未核；不据此声称官方原件或答案。

## 阻断项

- `ISSUE-1362`：Q21(3) 的一般果圆参数范围与是否承接（1）等边焦点条件不明确。类型 `answer-convention-ambiguous`，状态 `open`，影响 `blocks_completion`。
- resume action 要求获得可追溯的同版答案、解析或勘误以裁定参数作用域；未取得之前保留两种条件结果及 `U/PENDING`，不将特例写成一般答案。

## Frontmatter 与源清单投影

- 注册后将规范题面、答案要点、解析正文 frontmatter 的 `paper_id` 从 null 绑定为上述内部 paper ID；数学内容未改。按三份当前唯一事实源重新运行 `solution_sources.render_combined()`，更新派生 `_含解析.md`。
- 当前题面、答案、解析、含解析文件的 SHA-256 分别为：
  - `2007/2007_数学真题_上海文_试题.md`：`bbcd8ad5864eabf2f2ffd24ffc2c11bf2b8b730e7025fde6b3841eb19132d225`
  - `2007/2007_数学真题_上海文_答案要点.md`：`2f646079faf5b54878e8d00b0d4a64d10e3d7c13c4f9ef2faebb90f4be914f35`
  - `2007/2007_数学真题_上海文_解析正文.md`：`01b8f561bb483e27235b580a5b4435b75219dbeba88ac3d1b5ea1947ce23172c`
  - `2007/2007_数学真题_上海文_含解析.md`：`b39454ec05d5617277372a64a041bd9af92cf6324e6de2f7b3d5d89b3ca4bc06`
- 使用 `manifest_csv.py --write` 重建 775 行 `manifest.csv`。`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`、题面/答案/解析题号与小问集合对齐校验均通过。

逐题 provenance 与角色证据、`index.json`/TeX 项目生成、题图重绘、正式构建和视觉验收尚未完成。本登记不表示来源认证、整卷闭环或长期语料库完成。
