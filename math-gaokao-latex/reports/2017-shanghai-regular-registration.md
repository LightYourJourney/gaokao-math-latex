# 2017 上海普通高考卷：source/paper/batch 登记

日期：2026-10-28

## 登记结果

- `source_manifest.py register-papers` dry-run 校验通过；以单一状态事务写入，manifest revision `5273 → 5274`。
- paper：`gk-2017-regular-shanghai`；batch：`phase1-b50`；题量21；`track=none`；状态为 `planned`。
- 固定 source `src-213fecea206481434c7eb8f292fa39ffff3d28572e6080db2429c327529b2bac` 绑定为该 paper 的内部 `canonical` 输入，source 记录保持 `ready`。固定 PDF SHA-256 为 `44501ab771be2e0a625a47e1feb7afc6529e4038f363d238da73362d897c3675`，2页；题面页 `[1,2]`，来源答案页 `null`。
- 登记身份依据源文件自题“2017 普通高等学校招生考试（上海卷）”及已核页面结构；本次内部绑定不证明发布者、出版物、版次、原始来源链或官方身份。`official_answer=null`，所有答案解析仍标为编者独立推导、非官方。
- 尚无矢量图稿，`figure_files=[]`；没有新增 blocker issue。`index_metadata.structure` 覆盖填空1–12、选择13–16、解答17–21。

## 同步与边界

规范题面、答案要点与解析正文的 frontmatter 已写入 `paper_id: gk-2017-regular-shanghai`；随后从规范源重新生成 `_含解析.md`。来源题面、答案稿、解析稿和合并稿均引用同一 source ID 与 SHA-256。

本阶段未生成兼容索引、共享 TeX、四版入口、图稿、PDF 或 build/review receipt；未运行测试套件。下一步初拟制作 Q7、Q12、Q17、Q20 的矢量图稿。后续固定 PDF 高分辨率复核确认 Q20 无源图，因此实际只制作并登记 Q7、Q12、Q17，再进入 TeX 生成、正式构建和逐页视觉验收。该卷仍是 `planned`，尚未完成来源认证或正式版验收，也不代表长期语料库完成。
