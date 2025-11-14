# Larsson Thesis - Processing Notes

## Overview

This directory contains Staffan Larsson's 2002 PhD thesis "Issue-Based Dialogue Management"
split into separate chapter files for easier navigation and reference.

## Original Source

- **Original file**: `../Larsson_Tesis_nopages.md`
- **Size**: 10,237 lines, 474KB
- **Format**: Markdown (converted from PDF, contains OCR artifacts)

## Processing Applied

### 1. Chapter Splitting

The thesis has been split into the following files:

- `00_front_matter.md` - Title page, abstract, acknowledgements
- `00_contents.md` - Full table of contents
- `chapter_1.md` - Introduction
- `chapter_2.md` - Basic issue-based dialogue management
- `chapter_3.md` - Grounding issues
- `chapter_4.md` - Addressing unraised issues
- `chapter_5.md` - Action-oriented and negotiative dialogue
- `chapter_6.md` - Conclusions and future research
- `appendix_a.md` - TrindiKit functionality
- `appendix_b.md` - Rules and classes
- `README.md` - Navigation index and overview

### 2. OCR Error Correction

The following OCR errors have been automatically corrected:

**Character substitutions:**
- `managemen t` → `management`
- `implemen tation` → `implementation`
- `represen ting` → `representing`
- `orien ted` → `oriented`
- `accommo dation` → `accommodation`
- `participan t` → `participant`
- `requiremen ts` → `requirements`
- `negotiativ e` → `negotiative`
- `alternativ es` → `alternatives`
- `successiv e` → `successive`
- `di®erent` → `different`
- `¯` → `fi`
- `±` → `ffi`
- `°` → `fl`
- `®` → `ff`
- `º` → `Å`
- `Ä` → `ö`

**Reference formatting:**
- `Allenetal.` → `Allen et al.`
- `TrindiKit` → `Trindi Kit` (spacing improved)

**Section numbering:**
- Added spaces after section numbers (e.g., `1.1 Title` instead of `1.1Title`)

### 3. Known Remaining Issues

Some OCR artifacts remain that are difficult to fix automatically:

1. **Word spacing**: Some words are run together (e.g., "Thepurposeofstudying" instead of
   "The purpose of studying"). This is pervasive in the original OCR and would require
   dictionary-based splitting or manual correction.

2. **Special formatting**: Some mathematical notation, figures, and tables may not render
   correctly in markdown.

3. **References**: Some citation formatting may be inconsistent.

4. **Ligatures**: Some ligature characters may still be incorrectly rendered.

## Usage Recommendations

### For Reading

Use the `README.md` file as your starting point - it provides:
- Overview of thesis structure
- Links to all chapters
- Summary of key concepts
- Relevance to the IBDM project

### For Development Reference

When implementing IBDM features:

1. **Architecture questions**: See Chapter 2 (Basic issue-based dialogue management)
2. **Grounding/feedback**: See Chapter 3 (Grounding issues)
3. **QUD and accommodation**: See Chapter 4 (Addressing unraised issues)
4. **Actions and negotiation**: See Chapter 5
5. **TrindiKit details**: See Appendix A
6. **Rule definitions**: See Appendix B

### For Citation

Use the citation format from the README:

```
Larsson, S. (2002). Issue-Based Dialogue Management. Doctoral dissertation,
Department of Linguistics, Göteborg University, Sweden. ISBN 91-628-5301-5.
```

## Maintenance

### To regenerate chapters:

```bash
cd /Users/brewc/PycharmProjects/ibdm/docs
python split_thesis.py
python fix_ocr_advanced.py
```

### To add more OCR fixes:

Edit `split_thesis.py` or `fix_ocr_advanced.py` and add patterns to the `OCR_FIXES`
or `ADDITIONAL_FIXES` dictionaries.

## File Sizes

- chapter_1.md: 22KB (Introduction)
- chapter_2.md: 13KB (Basic IBDM)
- chapter_3.md: 130KB (Grounding - largest chapter)
- chapter_4.md: 87KB (Unraised issues)
- chapter_5.md: 47KB (Action-oriented dialogue)
- chapter_6.md: 75KB (Conclusions)
- appendix_a.md: 1KB (TrindiKit)
- appendix_b.md: 2KB (Rules)

## Related Documentation

For IBDM project-specific interpretation and implementation of Larsson's concepts, see:

- `/docs/burr_state_refactoring.md` - Burr state architecture based on Larsson
- `/docs/causation_chain_analysis.md` - Causation relationships in IBDM
- `/CLAUDE.md` - Development policies informed by Larsson's architecture

## Version History

- **2024-11-14**: Initial split and OCR correction applied
  - Split from `Larsson_Tesis_nopages.md`
  - Applied automated OCR fixes
  - Created navigation index
