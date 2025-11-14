# Larsson (2002) - Issue-Based Dialogue Management

**Author**: Staffan Larsson
**Institution**: Department of Linguistics, Göteborg University, Sweden
**Year**: 2002

This doctoral dissertation presents the theoretical foundation for Issue-Based Dialogue Management (IBDM),
an approach that uses questions (modeled semantically as issues) as the primary organizing and motivating
force in dialogue.

## Document Structure

### Front Matter
- [Front Matter & Abstract](00_front_matter.md) - Title, abstract, and acknowledgements
- [Table of Contents](00_contents.md) - Full table of contents

### Main Chapters

1. [Chapter 1: Introduction](chapter_1.md)
   - The aim of this study
   - Rationale
   - The IBiS family of systems
   - TrindiKit

2. [Chapter 2: Basic Issue-Based Dialogue Management](chapter_2.md)
   - Information exchange and inquiry-oriented dialogue
   - Shared and private information in dialogue
   - Overview of IBiS1
   - Semantics, dialogue moves, and plans
   - Update and selection modules

3. [Chapter 3: Grounding Issues](chapter_3.md)
   - Background on grounding theories (Clark, Ginzburg, Allwood)
   - Feedback and grounding strategies
   - Issue-based grounding in IBiS2
   - Interactive Communication Management

4. [Chapter 4: Addressing Unraised Issues](chapter_4.md)
   - The nature(s) of QUD (Questions Under Discussion)
   - Question accommodation
   - IBiS3 extensions
   - Dependent issue accommodation and clarification

5. [Chapter 5: Action-Oriented and Negotiative Dialogue](chapter_5.md)
   - Issues and actions in action-oriented dialogue
   - Interacting with menu-based devices
   - Issues Under Negotiation (IUN)
   - IBiS4 extensions

6. [Chapter 6: Conclusions and Future Research](chapter_6.md)
   - Summary
   - Dialogue typology
   - Dialogue structure
   - Future research areas

### Appendices

- [Appendix A: TrindiKit Functionality](appendix_a.md)
  - Datatypes, methods, and rule definition formats
  - DME-ADL and Control-ADL languages

- [Appendix B: Rules and Classes](appendix_b.md)
  - Complete rule definitions for IBiS1-4
  - Update and selection module rules

## Key Concepts

This thesis introduces and develops several key concepts:

- **Issues/Questions Under Discussion (QUD)**: The central organizing principle for dialogue
- **Information State**: Representation of shared and private information in dialogue
- **Dialogue Moves**: Actions that update the information state
- **Grounding**: How participants establish common ground
- **Accommodation**: Addressing issues not explicitly raised
- **TrindiKit**: A toolkit for building and experimenting with dialogue systems

## Relevance to IBDM Project

This thesis provides the theoretical foundation for the IBDM project. Key architectural elements:

- **Four-phase dialogue processing**: Interpretation → Integration → Selection → Generation
- **Information state architecture**: Separation of shared/private, QUD, plan, issues
- **Domain abstraction layer**: Predicates, sorts, and semantic operations
- **Question-based control flow**: Issues drive dialogue structure

## Citation

Larsson, S. (2002). *Issue-Based Dialogue Management*. Doctoral dissertation,
Department of Linguistics, Göteborg University, Sweden. ISBN 91-628-5301-5.
